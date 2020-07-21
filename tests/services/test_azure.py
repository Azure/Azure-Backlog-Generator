import pytest
import argparse
import time
from types import SimpleNamespace
from mock import Mock, MagicMock, patch
from azure.devops.connection import Connection
from azure.devops.released.client_factory import ClientFactory
from msrest.authentication import BasicAuthentication
import azbacklog.services as services
from azbacklog.services import AzDevOps
from azbacklog.entities import Tag
from azbacklog.helpers import Backlog
from tests.mockedfiles import MockedFiles


def mock_auth(*args, **kwargs):
    def mock_get_projects(*args, **kwargs):
        return SimpleNamespace(value=[
            SimpleNamespace(id=1, name='foo'),
            SimpleNamespace(id=2, name='bar')
        ])

    def mock_get_teams(*args, **kwargs):
        return [
            SimpleNamespace(id=1, name='foo Team'),
            SimpleNamespace(id=2, name='bar Team')
        ]

    def mock_queue_create_project(*args, **kwargs):
        return SimpleNamespace(id=1)

    def mock_get_core_client(*args, **kwargs):
        mock = MagicMock()
        mock.get_projects.return_value = mock_get_projects()
        mock.get_teams.return_value = mock_get_teams()
        mock.queue_crate_project.return_value = mock_queue_create_project()
        return mock

    def mock_get_operations_client(*args, **kwargs):
        mock = MagicMock()
        return mock

    def mock_get_work_client(*args, **kwargs):
        mock = MagicMock()
        mock.update_team_settings.return_value = None
        return mock

    def mock_get_work_item_tracking_client(*args, **kwargs):
        mock = MagicMock()
        mock.create_work_item.return_value = None
        return mock

    mock = MagicMock(spec=ClientFactory)
    mock.get_core_client.return_value = mock_get_core_client()
    mock.get_operations_client.return_value = mock_get_operations_client()
    mock.get_work_client.return_value = mock_get_work_client()
    mock.get_work_item_tracking_client = mock_get_work_item_tracking_client()
    return mock


@pytest.fixture(autouse=True)
def mock_auth_fixture(monkeypatch):
    monkeypatch.setattr(services.AzDevOps, "_auth", mock_auth)


def test_auth(monkeypatch):
    monkeypatch.undo()
    with pytest.raises(ValueError) as exc:
        az = AzDevOps(org='foo')  # NOQA
    assert "incorrect parameters were passed" in str(exc.value)

    with pytest.raises(ValueError) as exc:
        az = AzDevOps(token='bar')  # NOQA
    assert "incorrect parameters were passed" in str(exc.value)


@patch('time.sleep', return_value=None)
def test_get_project(patched_sleep):
    az = AzDevOps(org='foo', token='bar')

    result = az._get_project('foo')
    assert result.id == 1

    az.clients.reset_mock()
    assert az._get_project('something') is None
    assert az.clients.get_core_client.return_value.get_projects.call_count == 20


def test_check_status():
    az = AzDevOps(org='foo', token='bar')

    az.clients.get_operations_client.return_value.get_operation.return_value = SimpleNamespace(status='succeeded')
    result = az._check_status(0)
    assert result is True

    az.clients.get_operations_client.return_value.get_operation.return_value = SimpleNamespace(status='cancelled')
    result = az._check_status(0)
    assert result is False

    az.clients.get_operations_client.return_value.get_operation.return_value = SimpleNamespace(status='failed')
    result = az._check_status(0)
    assert result is False


def test_create_project(monkeypatch):
    az = AzDevOps(org='foo', token='bar')

    az._check_status = MagicMock(return_value=True)
    assert az._create_project('foo', 'bar') is True

    az._check_status = MagicMock(return_value=False)
    with pytest.raises(RuntimeError) as exc:
        az._create_project('foo', 'bar')
    assert "failed creating project" in str(exc.value)


def test_get_team():
    az = AzDevOps(org='foo', token='bar')
    project = SimpleNamespace(id=1)

    result = az._get_team(project, 'foo')

    assert result.id == 1
    assert az._get_team(project, 'something') is None


def test_enable_epics():
    az = AzDevOps(org='foo', token='bar')
    az._get_team = MagicMock(return_value=SimpleNamespace(id=1, project_id=1, name='foo'))
    project = SimpleNamespace(id=1)

    az._enable_epics(project, 'foo')

    assert az.clients.get_work_client.return_value.update_team_settings.called_with({
        "backlogVisibilities": {
            "Microsoft.EpicCategory": 'true',
            "Microsoft.FeatureCategory": 'true',
            "Microsoft.RequirementCategory": 'true'
        }
    }, SimpleNamespace(team_id=1, project_id=1))


def test_create_tags():
    az = AzDevOps(org='foo', token='bar')

    tags = []
    assert az._create_tags(tags) is None

    tag = Tag()
    tag.title = 'tag1'
    tags.append(tag)
    tag = Tag()
    tag.title = 'tag2'
    tags.append(tag)
    tag = Tag()
    tag.title = 'tag3'
    tags.append(tag)

    result = az._create_tags(tags)

    assert result == 'tag1; tag2; tag3'


def test_create_work_item():
    az = AzDevOps(org='foo', token='bar')
    project = SimpleNamespace(id=1)

    patch = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": 'foo'
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": 'bar'
        }
    ]
    az._create_work_item(project, 'test', 'foo', 'bar')
    assert az.clients.get_work_item_tracking_client.return_value.create_work_item.called_with(patch, project, 'test')

    tags_patch = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": 'foo'
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": 'bar'
        },
        {
            "op": "add",
            "path": "/fields/System.Tags",
            "value": 'foo; bar; baz'
        }
    ]
    az._create_work_item(project, 'test', 'foo', 'bar', tags='foo; bar; baz')
    assert az.clients.get_work_item_tracking_client.return_value.create_work_item.called_with(tags_patch, project, 'test')

    parent_patch = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": 'foo'
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": 'bar'
        },
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": 'http://foobar.com'
            }
        }
    ]
    az._create_work_item(project, 'test', 'foo', 'bar', parent=SimpleNamespace(url="http://foobar.com"))
    assert az.clients.get_work_item_tracking_client.return_value.create_work_item.called_with(parent_patch, project, 'test')


def test_deploy(fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_return_None(*args, **kwargs):
        return None

    az = AzDevOps(org='foo', token='bar')
    az._create_project = MagicMock(return_value=mock_return_None)
    az._get_project = MagicMock(return_value=SimpleNamespace(id=1))
    az._enable_epics = MagicMock(return_value=mock_return_None)
    az._create_work_item = MagicMock(return_value=mock_return_None)

    backlog = Backlog()
    config = backlog._get_config('workitems/correct')
    work_items = backlog._build_work_items(MockedFiles._mock_parsed_file_list(), config)

    args = argparse.Namespace()
    args.org = 'foo'
    args.repo = 'testUser'
    args.project = 'testProject'
    args.backlog = 'correct'

    az.deploy(args, work_items, config)

    az._create_project.assert_called_with('testProject', 'Sample description')
    az._enable_epics.assert_called()

    assert az._create_work_item.call_count == 20
