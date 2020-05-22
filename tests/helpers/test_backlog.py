import pytest
import json
import os
from argparse import Namespace
from mock import Mock, MagicMock, patch
from pyfakefs import fake_filesystem
import src.azbacklog.helpers as helpers
import src.azbacklog.entities as entities
import src.azbacklog.services as services
from tests.helpers import Lists
from tests.mockedfiles import MockedFiles


def test_gatherWorkItems(monkeypatch):
    def mockGatherWorkItemsReturnFileList(*args, **kwargs):
        return MockedFiles._mockFileList()

    monkeypatch.setattr(helpers.FileSystem, "getFiles", mockGatherWorkItemsReturnFileList)

    backlog = helpers.Backlog()
    assert backlog._gatherWorkItems('.') == MockedFiles._mockFileList()


def test_getConfig(monkeypatch, fs):
    MockedFiles._mockCorrectFileSystem(fs)

    def mockFileSystemReadFileReturnNone(*args, **kwargs):
        return None

    def mockParserJsonReturnJson(*args, **kwargs):
        content = None
        with open('./correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockValidationValidateConfigReturnTrue(*args, **kwargs):
        return True

    def mockValidationValidateConfigRaiseError(*args, **kwargs):
        return (False, "there's an error")

    monkeypatch.setattr(helpers.FileSystem, "readFile", mockFileSystemReadFileReturnNone)
    monkeypatch.setattr(helpers.Parser, "json", mockParserJsonReturnJson)

    backlog = helpers.Backlog()

    monkeypatch.setattr(helpers.Validation, "validateConfig", mockValidationValidateConfigReturnTrue)
    assert backlog._getConfig('.') == mockParserJsonReturnJson()

    monkeypatch.setattr(helpers.Validation, "validateConfig", mockValidationValidateConfigRaiseError)
    with pytest.raises(ValueError) as exc:
        backlog._getConfig('.')
    assert "configuration file not valid: there's an error" in str(exc.value)


def test_parseWorkItems(monkeypatch):
    def mockParseWorkItemsReturnFileList(*args, **kwargs):
        return MockedFiles._mockParsedFileList()

    monkeypatch.setattr(helpers.Parser, "fileHierarchy", mockParseWorkItemsReturnFileList)

    backlog = helpers.Backlog()
    assert backlog._parseWorkItems('.') == MockedFiles._mockParsedFileList()


def test_getAndValidateJson(monkeypatch, fs):
    MockedFiles._mockCorrectFileSystem(fs)

    def mockFileSystemReadFileReturnNone(*args, **kwargs):
        return None

    def mockParserJsonReturnJson(*args, **kwargs):
        content = None
        with open('./correct/01_epic/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockValidationValidateMetadataReturnTrue(*args, **kwargs):
        return True

    def mockValidationValidateMetadataReturnFalse(*args, **kwargs):
        return (False, "there's an error")

    monkeypatch.setattr(helpers.FileSystem, "readFile", mockFileSystemReadFileReturnNone)
    monkeypatch.setattr(helpers.Parser, "json", mockParserJsonReturnJson)

    backlog = helpers.Backlog()

    monkeypatch.setattr(helpers.Validation, "validateMetadata", mockValidationValidateMetadataReturnTrue)
    assert backlog._getAndValidateJson('.', MockedFiles._mockConfig()) == mockParserJsonReturnJson()

    monkeypatch.setattr(helpers.Validation, "validateMetadata", mockValidationValidateMetadataReturnFalse)
    with pytest.raises(ValueError) as exc:
        backlog._getAndValidateJson('.', MockedFiles._mockConfig())
    assert "metadata not valid: there's an error" in str(exc.value)


def test_buildWorkItems(fs):

    backlog = helpers.Backlog()
    backlog._buildEpic = MagicMock(return_value=None)
    workitems = backlog._buildWorkItems(MockedFiles._mockParsedFileList(), MockedFiles._mockConfig())

    backlog._buildEpic.assert_any_call(MockedFiles._mockParsedFileList()[0], MockedFiles._mockConfig())
    backlog._buildEpic.assert_any_call(MockedFiles._mockParsedFileList()[1], MockedFiles._mockConfig())
    backlog._buildEpic.assert_any_call(MockedFiles._mockParsedFileList()[2], MockedFiles._mockConfig())
    assert workitems == []

    epic = entities.Epic()
    epic.title = "Foobar"
    epic.description = "Some Description"
    backlog._buildEpic = MagicMock(return_value=epic)
    workitems = backlog._buildWorkItems([MockedFiles._mockParsedFileList()[0]], MockedFiles._mockConfig())
    assert len(workitems) == 1
    assert workitems[0] == epic
    assert workitems[0].title == "Foobar"
    assert workitems[0].description == "Some Description"


def test_createTag(fs):
    backlog = helpers.Backlog()
    tag = backlog._createTag("foo bar")

    assert isinstance(tag, entities.Tag) is True
    assert tag.title == "foo bar"


def test_buildEpic(fs):
    MockedFiles._mockCorrectFileSystem(fs)

    def mockGetConfigReturnConfig(*args, **kwargs):
        content = None
        with open('./correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockParserJsonReturnEpicJson(*args, **kwargs):
        content = None
        with open('./correct/01_epic/02_feature/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockBacklogBuildFeatureReturnFeature(*args, **kwargs):
        feature = entities.Feature()
        feature.title = "Some Feature"
        feature.description = "Some Description"

        return feature

    backlog = helpers.Backlog()

    backlog._getAndValidateJson = MagicMock(return_value=False)
    epic = backlog._buildEpic(MockedFiles._mockParsedFileList()[0], mockGetConfigReturnConfig())
    assert epic is None

    backlog._getAndValidateJson = MagicMock(return_value=mockParserJsonReturnEpicJson())
    backlog._buildFeature = MagicMock(return_value=None)
    epic = backlog._buildEpic(MockedFiles._mockParsedFileList()[0], mockGetConfigReturnConfig())
    assert epic.title == "Foo bar"
    assert epic.description == "Lorem Ipsum 01_folder/02_folder"
    assert len(epic.tags) == 3
    assert Lists.contains(epic.tags, lambda tag: tag.title == "01_Folder") is True
    assert Lists.contains(epic.tags, lambda tag: tag.title == "02_Folder") is True
    assert Lists.contains(epic.tags, lambda tag: tag.title == "AppDev") is True
    assert len(epic.features) == 0

    backlog._buildFeature = MagicMock(return_value=mockBacklogBuildFeatureReturnFeature())
    epic = backlog._buildEpic(MockedFiles._mockParsedFileList()[0], mockGetConfigReturnConfig())
    assert len(epic.features) == 3  # should return 3 instances of the mocked feature since the mocked epic has 3 features
    assert epic.features[0].title == "Some Feature"
    assert epic.features[0].description == "Some Description"


def test_buildFeature(fs):
    MockedFiles._mockCorrectFileSystem(fs)

    def mockGetConfigReturnConfig(*args, **kwargs):
        content = None
        with open('./correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockParserJsonReturnFeatureJson(*args, **kwargs):
        content = None
        with open('./correct/01_epic/02_feature/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockBacklogBuildStoryReturnStory(*args, **kwargs):
        story = entities.UserStory()
        story.title = "Some Story"
        story.description = "Some Description"

        return story

    def mockFeature(*args, **kwargs):
        return MockedFiles._mockParsedFileList()[0]["features"][0]

    backlog = helpers.Backlog()

    backlog._getAndValidateJson = MagicMock(return_value=False)
    feature = backlog._buildFeature(mockFeature(), mockGetConfigReturnConfig())
    assert feature is None

    backlog._getAndValidateJson = MagicMock(return_value=mockParserJsonReturnFeatureJson())
    backlog._buildStory = MagicMock(return_value=None)
    feature = backlog._buildFeature(mockFeature(), mockGetConfigReturnConfig())
    assert feature.title == "Foo bar"
    assert feature.description == "Lorem Ipsum 01_folder/02_folder"
    assert len(feature.tags) == 3
    assert Lists.contains(feature.tags, lambda tag: tag.title == "01_Folder") is True
    assert Lists.contains(feature.tags, lambda tag: tag.title == "02_Folder") is True
    assert Lists.contains(feature.tags, lambda tag: tag.title == "AppDev") is True
    assert len(feature.userStories) == 0

    backlog._buildStory = MagicMock(return_value=mockBacklogBuildStoryReturnStory())
    feature = backlog._buildFeature(mockFeature(), mockGetConfigReturnConfig())
    assert len(feature.userStories) == 2  # should return 2 instances of the mocked feature since the mocked feature has 2 user stories
    assert feature.userStories[0].title == "Some Story"
    assert feature.userStories[0].description == "Some Description"


def test_buildStory(fs):
    MockedFiles._mockCorrectFileSystem(fs)

    def mockGetConfigReturnConfig(*args, **kwargs):
        content = None
        with open('./correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockParserJsonReturnUserStoryJson(*args, **kwargs):
        content = None
        with open('./correct/01_epic/02_feature/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockBacklogBuildTaskReturnTask(*args, **kwargs):
        task = entities.Task()
        task.title = "Some Task"
        task.description = "Some Description"

        return task

    def mockUserStory(*args, **kwargs):
        return MockedFiles._mockParsedFileList()[0]["features"][0]["stories"][0]

    backlog = helpers.Backlog()

    backlog._getAndValidateJson = MagicMock(return_value=False)
    story = backlog._buildStory(mockUserStory(), mockGetConfigReturnConfig())
    assert story is None

    backlog._getAndValidateJson = MagicMock(return_value=mockParserJsonReturnUserStoryJson())
    backlog._buildTask = MagicMock(return_value=None)
    story = backlog._buildStory(mockUserStory(), mockGetConfigReturnConfig())
    assert story.title == "Foo bar"
    assert story.description == "Lorem Ipsum 01_folder/02_folder"
    assert len(story.tags) == 3
    assert Lists.contains(story.tags, lambda tag: tag.title == "01_Folder") is True
    assert Lists.contains(story.tags, lambda tag: tag.title == "02_Folder") is True
    assert Lists.contains(story.tags, lambda tag: tag.title == "AppDev") is True
    assert len(story.tasks) == 0

    backlog._buildTask = MagicMock(return_value=mockBacklogBuildTaskReturnTask())
    story = backlog._buildStory(mockUserStory(), mockGetConfigReturnConfig())
    print(mockUserStory())
    assert len(story.tasks) == 2  # should return 2 instances of the mocked story since the mocked story has 2 tasks
    assert story.tasks[0].title == "Some Task"
    assert story.tasks[0].description == "Some Description"


def test_buildTask(fs):
    MockedFiles._mockCorrectFileSystem(fs)

    def mockGetConfigReturnConfig(*args, **kwargs):
        content = None
        with open('./correct/config.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockParserJsonReturnTaskJson(*args, **kwargs):
        content = None
        with open('./correct/01_epic/02_feature/metadata.json', 'r') as reader:
            content = reader.read()
            reader.close()

        return json.loads(content)

    def mockTask(*args, **kwargs):
        return MockedFiles._mockParsedFileList()[0]["features"][0]["stories"][0]["tasks"][0]

    backlog = helpers.Backlog()

    backlog._getAndValidateJson = MagicMock(return_value=False)
    task = backlog._buildTask(mockTask(), mockGetConfigReturnConfig())
    assert task is None

    backlog._getAndValidateJson = MagicMock(return_value=mockParserJsonReturnTaskJson())
    task = backlog._buildTask(mockTask(), mockGetConfigReturnConfig())
    assert task.title == "Foo bar"
    assert task.description == "Lorem Ipsum 01_folder/02_folder"
    assert len(task.tags) == 3
    assert Lists.contains(task.tags, lambda tag: tag.title == "01_Folder") is True
    assert Lists.contains(task.tags, lambda tag: tag.title == "02_Folder") is True
    assert Lists.contains(task.tags, lambda tag: tag.title == "AppDev") is True


@patch('src.azbacklog.services.github.GitHub.deploy')
@patch('src.azbacklog.services.github.Github.__init__')
def test_deployGitHub(patchedInit, patchedDeploy, fs):
    patchedInit.return_value = None
    patchedDeploy.return_value = None

    MockedFiles._mockCorrectFileSystem(fs)

    backlog = helpers.Backlog()
    config = backlog._getConfig('correct')
    workItems = backlog._buildWorkItems(MockedFiles._mockParsedFileList(), config)

    args = Namespace(org='testOrg', repo=None, project='testProject', backlog='correct', token='testToken')

    backlog._deployGitHub(args, workItems)
    patchedInit.assert_called_with(args.token)
    patchedDeploy.assert_called_with(args, workItems)


# TODO: Unit test call to deployAzure
# @patch('src.azbacklog.services.github.GitHub.deploy')
# @patch('src.azbacklog.services.github.Github.__init__')
# def test_deployGitHub(patchedInit, patchedDeploy, fs):
def test_deployAzure(fs):
    # patchedInit.return_value = None
    # patchedDeploy.return_value = None

    MockedFiles._mockCorrectFileSystem(fs)

    backlog = helpers.Backlog()
    config = backlog._getConfig('correct')
    workItems = backlog._buildWorkItems(MockedFiles._mockParsedFileList(), config)

    args = Namespace(org='testOrg', repo=None, project='testProject', backlog='correct', token='testToken')

    backlog._deployAzure(args, workItems)
    # patchedInit.assert_called_with(args.token)
    # patchedDeploy.assert_called_with(args, workItems)


def test_build():
    def mockGatherWorkItemsReturnFileList(*args, **kwargs):
        return MockedFiles._mockFileList()

    def mockGetConfigReturnConfig(*args, **kwargs):
        return MockedFiles._mockConfig()

    def mockParseWorkItemsReturnParsedFileList(*args, **kwargs):
        return MockedFiles._mockParsedFileList()

    backlog = helpers.Backlog()
    backlog._gatherWorkItems = MagicMock(return_value=mockGatherWorkItemsReturnFileList())
    backlog._getConfig = MagicMock(return_value=mockGetConfigReturnConfig())
    backlog._parseWorkItems = MagicMock(return_value=mockParseWorkItemsReturnParsedFileList())
    backlog._buildWorkItems = MagicMock(return_value=None)
    backlog._deployGitHub = MagicMock(return_value=None)
    backlog._deployAzure = MagicMock(return_value=None)

    backlog.build(Namespace(backlog='caf', repo='github', validate_only=None))
    backlog._gatherWorkItems.assert_called_with('./workitems/caf')
    backlog._getConfig.assert_called_with('./workitems/caf')
    backlog._parseWorkItems.assert_called_with(mockGatherWorkItemsReturnFileList())
    backlog._buildWorkItems.assert_called_with(mockParseWorkItemsReturnParsedFileList(), mockGetConfigReturnConfig())
    backlog._deployGitHub.assert_called_with(Namespace(backlog='caf', repo='github', validate_only=None), None)

    backlog._deployGitHub = MagicMock(return_value=None)
    backlog.build(Namespace(validate_only='./validate/foo'))
    backlog._gatherWorkItems.assert_called_with('./validate/foo')
    backlog._getConfig.assert_called_with('./validate/foo')
    backlog._deployGitHub.assert_not_called()
