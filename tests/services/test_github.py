import pytest
import argparse
from mock import Mock, MagicMock, patch, call
from github import Github
from github.Repository import Repository
from github.AuthenticatedUser import AuthenticatedUser
from github.Issue import Issue
from github.Label import Label
from github.Organization import Organization
from azbacklog.services import GitHub
from azbacklog.entities import Task
from azbacklog.helpers import Backlog
from tests.helpers import Noniterable_str
from tests.mockedfiles import MockedFiles


@pytest.fixture
def mock_Github(monkeypatch):
    def mock_get_labels():
        labels = []
        for x in range(5):
            label = Mock(spec=Label)
            label._name = "Test " + str(x)
            labels.append(label)

        return labels

    def mock_create_repo():
        repo = Mock(spec=Repository)
        repo.get_labels.return_value = mock_get_labels()
        return repo

    mock = Mock(spec=Github)
    mock.get_user.return_value.create_repo.return_value = mock_create_repo()
    return mock


@patch('github.Github.__init__')
def test_authenticate(patched):
    patched.return_value = None

    gh = GitHub(username='test', password='test')
    patched.assert_called_with('test', 'test')

    gh = GitHub(hostname='test.com', token='test')
    patched.assert_called_with(base_url='https://test.com/api/v3', login_or_token='test')

    gh = GitHub(token='testToken')
    patched.assert_called_with('testToken')

    with pytest.raises(ValueError) as exc:
        gh = GitHub('something')  # NOQA
    assert "incorrect parameters were passed" in str(exc.value)


def test_get_user(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    gh._get_user()

    mock_Github.get_user.assert_called_with()


def test_get_org(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    gh._get_org('test')

    mock_Github.get_organization.assert_called_with('test')


def test_create_user_repo(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    user = gh._get_user()
    gh._create_user_repo('testRepo', 'foobar')

    user.create_repo.assert_called_with(name='testRepo', description='foobar', has_issues=True, auto_init=True, private=True)


def test_create_org_repo(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    org = gh._get_org('testOrg')
    gh._create_org_repo('testOrg', 'testRepo', 'foobar')

    org.create_repo.assert_called_with(name='testRepo', description='foobar', has_issues=True, auto_init=True, private=True)


def test_create_project(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    gh._create_project(repo, 'testOrg', 'testBody')

    repo.create_project.assert_called_with('testOrg', body='testBody')


def test_create_milestone(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    gh._create_milestone(repo, 'testMilestone', 'testDesc')

    repo.create_milestone.assert_called_with('testMilestone', description='testDesc')


def test_create_label(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    gh._create_label(repo, 'testLabel', '000000')

    repo.create_label.assert_called_with('testLabel', '000000')


def test_create_labels(mock_Github):
    def mock_create_label(*args, **kwargs):
        return Noniterable_str(args[1])

    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    gh._create_label = MagicMock(side_effect=mock_create_label)

    names = ['test1', 'test2']
    colors = ['000000', '111111']
    labels = gh._create_labels(repo, names, colors)

    assert len(labels) == 2
    assert labels[0] == 'test1'
    assert labels[1] == "test2"


def test_get_labels(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    labels = gh._get_labels(repo)

    repo.get_labels.assert_called()
    assert len(labels) == 5


def test_delete_label(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    label = gh._create_label(repo, 'test', '000000')
    gh._delete_label(label)

    label.delete.assert_called()


def test_delete_labels(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    labels = gh._get_labels(repo)
    gh._delete_labels(repo)

    for label in labels:
        label.delete.assert_called()


def test_create_column(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    project = gh._create_project(repo, 'testOrg', 'testBody')
    gh._create_column(project, 'test')

    project.create_column.assert_called_with('test')


def test_create_columns(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    project = gh._create_project(repo, 'testOrg', 'testBody')
    gh._create_columns(project)

    assert project.create_column.call_args_list == [call('To Do'), call('In Progress'), call('Completed')]


def test_create_card(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    project = gh._create_project(repo, 'testOrg', 'testBody')
    column = gh._create_column(project, 'test')
    issue = gh._create_issue(repo, 'testMilestone', 'testTitle', 'testBody', [])
    gh._create_card(column, issue)

    column.create_card.assert_called_with(content_id=issue.id, content_type="Issue")


def test_create_issue(mock_Github):
    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()
    gh._create_issue(repo, 'testMilestone', 'testTitle', 'testBody', [])

    repo.create_issue.assert_called_with('testTitle', body='testBody', milestone='testMilestone', labels=[])


def test_build_description():
    gh = GitHub(token='foo')
    task1 = Task()
    task1.title = "Test 1"
    task1.description = "This is a description 1"

    task2 = Task()
    task2.title = "Test 2"
    task2.description = "This is a description 2"

    tasks = [task1, task2]
    desc = "This is a sample feature description"

    result = gh._build_description(desc, tasks)
    assert result == "This is a sample feature description" \
                     "\n" \
                     "\n- [ ] **Test 1**" \
                     "\n      This is a description 1" \
                     "\n" \
                     "\n- [ ] **Test 2**" \
                     "\n      This is a description 2"


def test_build_initialize_repo(fs, mock_Github):
    MockedFiles._mock_correct_file_system(fs)

    gh = GitHub(token='foo')
    gh.github = mock_Github
    repo = gh._get_user().create_repo()

    gh._initialize_repo(repo, './workitems/correct', ['./workitems/correct/README.md', './workitems/correct/feature_01/attachment.doc'])


def test_deploy_with_org(fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_return_None(*args, **kwargs):
        return None

    gh = GitHub(token='foo')
    gh._create_org_repo = MagicMock(return_value=mock_return_None)
    gh._create_user_repo = MagicMock(return_value=mock_return_None)
    gh._initialize_repo = MagicMock(return_value=mock_return_None)
    gh._create_labels = MagicMock(return_value=mock_return_None)
    gh._delete_labels = MagicMock(return_value=mock_return_None)
    gh._create_project = MagicMock(return_value=mock_return_None)
    gh._create_columns = MagicMock(return_value=mock_return_None)
    gh._create_milestone = MagicMock(return_value=mock_return_None)
    gh._create_issue = MagicMock(return_value=mock_return_None)
    gh._create_card = MagicMock(return_value=mock_return_None)
    gh._build_description = MagicMock(return_value=mock_return_None)

    backlog = Backlog()
    config = backlog._get_config('workitems/correct', 'github')
    config["_repository_path"] = 'workitems/correct'
    work_items = backlog._build_work_items(MockedFiles._mock_parsed_file_list(), config)

    args = argparse.Namespace()
    args.org = 'testOrg'
    args.repo = None
    args.project = 'testProject'
    args.backlog = 'correct'

    gh.deploy(args, work_items, config, [])
    gh._create_org_repo.assert_called_with('testOrg', 'testProject', 'Sample description')

    gh._delete_labels.assert_called()
    assert gh._create_project.call_count == 4
    assert gh._create_columns.call_count == 4
    assert gh._create_milestone.call_count == 6
    assert gh._create_issue.call_count == 4
    assert gh._create_card.call_count == 4


def test_deploy_with_repo(fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_return_None(*args, **kwargs):
        return None

    gh = GitHub(token='foo')
    gh._create_org_repo = MagicMock(return_value=mock_return_None)
    gh._create_user_repo = MagicMock(return_value=mock_return_None)
    gh._initialize_repo = MagicMock(return_value=mock_return_None)
    gh._create_labels = MagicMock(return_value=mock_return_None)
    gh._delete_labels = MagicMock(return_value=mock_return_None)
    gh._create_project = MagicMock(return_value=mock_return_None)
    gh._create_columns = MagicMock(return_value=mock_return_None)
    gh._create_milestone = MagicMock(return_value=mock_return_None)
    gh._create_issue = MagicMock(return_value=mock_return_None)
    gh._create_card = MagicMock(return_value=mock_return_None)
    gh._build_description = MagicMock(return_value=mock_return_None)

    backlog = Backlog()
    config = backlog._get_config('workitems/correct', 'github')
    config["_repository_path"] = 'workitems/correct'
    work_items = backlog._build_work_items(MockedFiles._mock_parsed_file_list(), config)

    args = argparse.Namespace()
    args.org = None
    args.repo = 'testUser'
    args.project = 'testProject'
    args.backlog = 'correct'

    gh.deploy(args, work_items, config, [])
    gh._create_user_repo.assert_called_with('testProject', 'Sample description')

    gh._delete_labels.assert_called()
    assert gh._create_project.call_count == 4
    assert gh._create_columns.call_count == 4
    assert gh._create_milestone.call_count == 6
    assert gh._create_issue.call_count == 4
    assert gh._create_card.call_count == 4
