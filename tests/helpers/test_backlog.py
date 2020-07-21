import pytest
import json
import os
from argparse import Namespace
from mock import Mock, MagicMock, PropertyMock, patch
from pyfakefs import fake_filesystem
import azbacklog.helpers as helpers
import azbacklog.entities as entities
import azbacklog.services as services
from azbacklog.services import AzDevOps
from tests.helpers import Lists, StringContains
from tests.mockedfiles import MockedFiles
from tests.services.test_azure import mock_auth


def test_gather_work_items(monkeypatch):
    def mock_gather_work_items_returns_file_list(*args, **kwargs):
        return MockedFiles._mock_file_list()

    monkeypatch.setattr(helpers.FileSystem, "get_files", mock_gather_work_items_returns_file_list)

    backlog = helpers.Backlog()
    assert backlog._gather_work_items('.') == MockedFiles._mock_file_list()


def test_get_config(monkeypatch, fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_file_system_read_file_returns_None(*args, **kwargs):
        return None

    def mock_parser_json_returns_json(*args, **kwargs):
        content = None
        with open('./workitems/correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_validation_validate_config_returns_True(*args, **kwargs):
        return True

    def mock_validation_validate_config_raises_error(*args, **kwargs):
        return (False, "there's an error")

    monkeypatch.setattr(helpers.FileSystem, "read_file", mock_file_system_read_file_returns_None)
    monkeypatch.setattr(helpers.Parser, "parse_json", mock_parser_json_returns_json)

    backlog = helpers.Backlog()

    monkeypatch.setattr(helpers.Validation, "validate_config", mock_validation_validate_config_returns_True)
    assert backlog._get_config('.') == mock_parser_json_returns_json()

    monkeypatch.setattr(helpers.Validation, "validate_config", mock_validation_validate_config_raises_error)
    with pytest.raises(ValueError) as exc:
        backlog._get_config('.')
    assert "configuration file not valid: there's an error" in str(exc.value)


def test_parse_work_items(monkeypatch):
    def mock_parse_work_items_returns_file_list(*args, **kwargs):
        return MockedFiles._mock_parsed_file_list()

    monkeypatch.setattr(helpers.Parser, "parse_file_hierarchy", mock_parse_work_items_returns_file_list)

    backlog = helpers.Backlog()
    assert backlog._parse_work_items('.') == MockedFiles._mock_parsed_file_list()


def test_get_and_validate_json(monkeypatch, fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_file_system_read_file_returns_None(*args, **kwargs):
        return None

    def mock_parser_json_returns_json(*args, **kwargs):
        content = None
        with open('./workitems/correct/01_epic/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_validation_validate_metadata_returns_True(*args, **kwargs):
        return True

    def mock_validation_validate_metadata_returns_False(*args, **kwargs):
        return (False, "there's an error")

    monkeypatch.setattr(helpers.FileSystem, "read_file", mock_file_system_read_file_returns_None)
    monkeypatch.setattr(helpers.Parser, "parse_json", mock_parser_json_returns_json)

    backlog = helpers.Backlog()

    monkeypatch.setattr(helpers.Validation, "validate_metadata", mock_validation_validate_metadata_returns_True)
    assert backlog._get_and_validate_json('.', MockedFiles._mock_config()) == mock_parser_json_returns_json()

    monkeypatch.setattr(helpers.Validation, "validate_metadata", mock_validation_validate_metadata_returns_False)
    with pytest.raises(ValueError) as exc:
        backlog._get_and_validate_json('.', MockedFiles._mock_config())
    assert "metadata not valid: there's an error" in str(exc.value)


def test_build_work_items(fs):

    backlog = helpers.Backlog()
    backlog._build_epic = MagicMock(return_value=None)
    work_items = backlog._build_work_items(MockedFiles._mock_parsed_file_list(), MockedFiles._mock_config())

    backlog._build_epic.assert_any_call(MockedFiles._mock_parsed_file_list()[0], MockedFiles._mock_config())
    backlog._build_epic.assert_any_call(MockedFiles._mock_parsed_file_list()[1], MockedFiles._mock_config())
    backlog._build_epic.assert_any_call(MockedFiles._mock_parsed_file_list()[2], MockedFiles._mock_config())
    assert work_items == []

    epic = entities.Epic()
    epic.title = "Foobar"
    epic.description = "Some Description"
    backlog._build_epic = MagicMock(return_value=epic)
    work_items = backlog._build_work_items([MockedFiles._mock_parsed_file_list()[0]], MockedFiles._mock_config())
    assert len(work_items) == 1
    assert work_items[0] == epic
    assert work_items[0].title == "Foobar"
    assert work_items[0].description == "Some Description"


def test_create_tag(fs):
    backlog = helpers.Backlog()
    tag = backlog._create_tag("foo bar")

    assert isinstance(tag, entities.Tag) is True
    assert tag.title == "foo bar"


def test_build_epic(fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_get_config_returns_config(*args, **kwargs):
        content = None
        with open('./workitems/correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_parser_parse_json_returns_epic_json(*args, **kwargs):
        content = None
        with open('./workitems/correct/01_epic/02_feature/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_backlog_build_feature_returns_feature(*args, **kwargs):
        feature = entities.Feature()
        feature.title = "Some Feature"
        feature.description = "Some Description"

        return feature

    backlog = helpers.Backlog()

    backlog._get_and_validate_json = MagicMock(return_value=False)
    epic = backlog._build_epic(MockedFiles._mock_parsed_file_list()[0], mock_get_config_returns_config())
    assert epic is None

    backlog._get_and_validate_json = MagicMock(return_value=mock_parser_parse_json_returns_epic_json())
    backlog._build_feature = MagicMock(return_value=None)
    epic = backlog._build_epic(MockedFiles._mock_parsed_file_list()[0], mock_get_config_returns_config())
    assert epic.title == "Foo bar"
    assert epic.description == "Lorem Ipsum 01_folder/02_folder"
    assert len(epic.tags) == 3
    assert Lists.contains(epic.tags, lambda tag: tag.title == "01_Folder") is True
    assert Lists.contains(epic.tags, lambda tag: tag.title == "02_Folder") is True
    assert Lists.contains(epic.tags, lambda tag: tag.title == "AppDev") is True
    assert len(epic.features) == 0

    backlog._build_feature = MagicMock(return_value=mock_backlog_build_feature_returns_feature())
    epic = backlog._build_epic(MockedFiles._mock_parsed_file_list()[0], mock_get_config_returns_config())
    assert len(epic.features) == 3  # should return 3 instances of the mocked feature since the mocked epic has 3 features
    assert epic.features[0].title == "Some Feature"
    assert epic.features[0].description == "Some Description"


def test_build_feature(fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_get_config_returns_config(*args, **kwargs):
        content = None
        with open('./workitems/correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_parser_parse_json_returns_feature_json(*args, **kwargs):
        content = None
        with open('./workitems/correct/01_epic/02_feature/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_backlog_build_story_returns_story(*args, **kwargs):
        story = entities.UserStory()
        story.title = "Some Story"
        story.description = "Some Description"

        return story

    def mock_feature(*args, **kwargs):
        return MockedFiles._mock_parsed_file_list()[0]["features"][0]

    backlog = helpers.Backlog()

    backlog._get_and_validate_json = MagicMock(return_value=False)
    feature = backlog._build_feature(mock_feature(), mock_get_config_returns_config())
    assert feature is None

    backlog._get_and_validate_json = MagicMock(return_value=mock_parser_parse_json_returns_feature_json())
    backlog._build_story = MagicMock(return_value=None)
    feature = backlog._build_feature(mock_feature(), mock_get_config_returns_config())
    assert feature.title == "Foo bar"
    assert feature.description == "Lorem Ipsum 01_folder/02_folder"
    assert len(feature.tags) == 3
    assert Lists.contains(feature.tags, lambda tag: tag.title == "01_Folder") is True
    assert Lists.contains(feature.tags, lambda tag: tag.title == "02_Folder") is True
    assert Lists.contains(feature.tags, lambda tag: tag.title == "AppDev") is True
    assert len(feature.userstories) == 0

    backlog._build_story = MagicMock(return_value=mock_backlog_build_story_returns_story())
    feature = backlog._build_feature(mock_feature(), mock_get_config_returns_config())
    assert len(feature.userstories) == 2  # should return 2 instances of the mocked feature since the mocked feature has 2 user stories
    assert feature.userstories[0].title == "Some Story"
    assert feature.userstories[0].description == "Some Description"


def test_build_story(fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_get_config_returns_config(*args, **kwargs):
        content = None
        with open('./workitems/correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_parser_parse_json_returns_userstory_Json(*args, **kwargs):
        content = None
        with open('./workitems/correct/01_epic/02_feature/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_backlog_build_task_returns_task(*args, **kwargs):
        task = entities.Task()
        task.title = "Some Task"
        task.description = "Some Description"

        return task

    def mock_userstory(*args, **kwargs):
        return MockedFiles._mock_parsed_file_list()[0]["features"][0]["stories"][0]

    backlog = helpers.Backlog()

    backlog._get_and_validate_json = MagicMock(return_value=False)
    story = backlog._build_story(mock_userstory(), mock_get_config_returns_config())
    assert story is None

    backlog._get_and_validate_json = MagicMock(return_value=mock_parser_parse_json_returns_userstory_Json())
    backlog._build_task = MagicMock(return_value=None)
    story = backlog._build_story(mock_userstory(), mock_get_config_returns_config())
    assert story.title == "Foo bar"
    assert story.description == "Lorem Ipsum 01_folder/02_folder"
    assert len(story.tags) == 3
    assert Lists.contains(story.tags, lambda tag: tag.title == "01_Folder") is True
    assert Lists.contains(story.tags, lambda tag: tag.title == "02_Folder") is True
    assert Lists.contains(story.tags, lambda tag: tag.title == "AppDev") is True
    assert len(story.tasks) == 0

    backlog._build_task = MagicMock(return_value=mock_backlog_build_task_returns_task())
    story = backlog._build_story(mock_userstory(), mock_get_config_returns_config())
    print(mock_userstory())
    assert len(story.tasks) == 2  # should return 2 instances of the mocked story since the mocked story has 2 tasks
    assert story.tasks[0].title == "Some Task"
    assert story.tasks[0].description == "Some Description"


def test_build_task(fs):
    MockedFiles._mock_correct_file_system(fs)

    def mock_get_config_returns_config(*args, **kwargs):
        content = None
        with open('./workitems/correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_parser_parse_json_returns_task_json(*args, **kwargs):
        content = None
        with open('./workitems/correct/01_epic/02_feature/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mock_task(*args, **kwargs):
        return MockedFiles._mock_parsed_file_list()[0]["features"][0]["stories"][0]["tasks"][0]

    backlog = helpers.Backlog()

    backlog._get_and_validate_json = MagicMock(return_value=False)
    task = backlog._build_task(mock_task(), mock_get_config_returns_config())
    assert task is None

    backlog._get_and_validate_json = MagicMock(return_value=mock_parser_parse_json_returns_task_json())
    task = backlog._build_task(mock_task(), mock_get_config_returns_config())
    assert task.title == "Foo bar"
    assert task.description == "Lorem Ipsum 01_folder/02_folder"
    assert len(task.tags) == 3
    assert Lists.contains(task.tags, lambda tag: tag.title == "01_Folder") is True
    assert Lists.contains(task.tags, lambda tag: tag.title == "02_Folder") is True
    assert Lists.contains(task.tags, lambda tag: tag.title == "AppDev") is True


# TODO: monkeypatch GitHub authentication
@patch('azbacklog.services.github.GitHub.deploy')
@patch('github.Github')
def test_deploy_github(patched_github, patched_deploy, fs):
    patched_github.return_value = MagicMock()
    patched_deploy.return_value = None

    MockedFiles._mock_correct_file_system(fs)

    backlog = helpers.Backlog()
    config = backlog._get_config('workitems/correct')
    work_items = backlog._build_work_items(MockedFiles._mock_parsed_file_list(), config)

    args = Namespace(org='testOrg', repo=None, project='testProject', backlog='correct', token='testToken')

    backlog._deploy_github(args, work_items)
    patched_deploy.assert_called_with(args, work_items)


@patch('azbacklog.services.azure.AzDevOps.deploy')
def test_deploy_azure(patched_deploy, fs, monkeypatch):
    monkeypatch.setattr(services.AzDevOps, "_auth", mock_auth)

    patched_deploy.return_value = None

    MockedFiles._mock_correct_file_system(fs)

    backlog = helpers.Backlog()
    config = backlog._get_config('workitems/correct')
    work_items = backlog._build_work_items(MockedFiles._mock_parsed_file_list(), config)

    args = Namespace(org='testOrg', repo=None, project='testProject', backlog='correct', token='testToken')

    backlog._deploy_azure(args, work_items)
    patched_deploy.assert_called_with(args, work_items)


def test_build():
    def mock_gather_work_items_return_file_list(*args, **kwargs):
        return MockedFiles._mock_file_list()

    def mock_get_config_return_config(*args, **kwargs):
        return MockedFiles._mock_config()

    def mock_parse_work_items_return_parsed_file_list(*args, **kwargs):
        return MockedFiles._mock_parsed_file_list()

    backlog = helpers.Backlog()
    backlog._gather_work_items = MagicMock(return_value=mock_gather_work_items_return_file_list())
    backlog._get_config = MagicMock(return_value=mock_get_config_return_config())
    backlog._parse_work_items = MagicMock(return_value=mock_parse_work_items_return_parsed_file_list())
    backlog._build_work_items = MagicMock(return_value=None)
    backlog._deploy_github = MagicMock(return_value=None)
    backlog._deploy_azure = MagicMock(return_value=None)

    backlog.build(Namespace(backlog='caf', repo='github', validate_only=None))
    backlog._gather_work_items.assert_called_with(StringContains('./workitems/caf'))
    backlog._get_config.assert_called_with(StringContains('/workitems/caf'))
    backlog._parse_work_items.assert_called_with(mock_gather_work_items_return_file_list())
    backlog._build_work_items.assert_called_with(mock_parse_work_items_return_parsed_file_list(), mock_get_config_return_config())
    backlog._deploy_github.assert_called_with(Namespace(backlog='caf', repo='github', validate_only=None), None)

    backlog.build(Namespace(backlog='caf', repo='azure', org='test', validate_only=None))
    backlog._gather_work_items.assert_called_with(StringContains('./workitems/caf'))
    backlog._get_config.assert_called_with(StringContains('/workitems/caf'))
    backlog._parse_work_items.assert_called_with(mock_gather_work_items_return_file_list())
    backlog._build_work_items.assert_called_with(mock_parse_work_items_return_parsed_file_list(), mock_get_config_return_config())
    backlog._deploy_azure.assert_called_with(Namespace(backlog='caf', repo='azure', org='test', validate_only=None), None)

    backlog._deploy_github = MagicMock(return_value=None)
    backlog.build(Namespace(validate_only='./validate/foo'))
    backlog._gather_work_items.assert_called_with('./validate/foo')
    backlog._get_config.assert_called_with('./validate/foo')
    backlog._deploy_github.assert_not_called()
