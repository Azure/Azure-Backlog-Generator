import pytest
import argparse
from mock import Mock, MagicMock, patch, call
from github import Github
from github.Repository import Repository
from github.AuthenticatedUser import AuthenticatedUser
from github.Issue import Issue
from github.Label import Label
from github.Organization import Organization
from src.azbacklog.services import GitHub
from src.azbacklog.entities import Task
from src.azbacklog.helpers import Backlog
from tests.helpers import Noniterable_str
from tests.mockedfiles import MockedFiles


@pytest.fixture
def mockGithub(monkeypatch):
    def mock_getLabels():
        labels = []
        for x in range(5):
            label = Mock(spec=Label)
            label._name = "Test " + str(x)
            labels.append(label)

        return labels

    def mock_createRepo():
        repo = Mock(spec=Repository)
        repo.get_labels.return_value = mock_getLabels()
        return repo

    mock = Mock(spec=Github)
    mock.get_user.return_value.create_repo.return_value = mock_createRepo()
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


def test_getUser(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    gh._getUser()

    mockGithub.get_user.assert_called_with()


def test_getOrg(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    gh._getOrg('test')

    mockGithub.get_organization.assert_called_with('test')


def test_createUserRepo(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    user = gh._getUser()
    gh._createUserRepo('testRepo')

    user.create_repo.assert_called_with(name='testRepo', has_issues=True, auto_init=True, private=True)


def test_createOrgRepo(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    org = gh._getOrg('testOrg')
    gh._createOrgRepo('testOrg', 'testRepo')

    org.create_repo.assert_called_with(name='testRepo', has_issues=True, auto_init=True, private=True)


def test_createProject(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    gh._createProject(repo, 'testOrg', 'testBody')

    repo.create_project.assert_called_with('testOrg', body='testBody')


def test_createMilestone(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    gh._createMilestone(repo, 'testMilestone', 'testDesc')

    repo.create_milestone.assert_called_with('testMilestone', description='testDesc')


def test_createLabel(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    gh._createLabel(repo, 'testLabel')

    repo.create_label.assert_called_with('testLabel')


def test_createLabels(mockGithub):
    def mock_createLabel(*args, **kwargs):
        return Noniterable_str(args[1])

    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    gh._createLabel = MagicMock(side_effect=mock_createLabel)

    names = ['test1', 'test2']
    labels = gh._createLabels(repo, names)

    assert len(labels) == 2
    assert labels[0] == 'test1'
    assert labels[1] == "test2"


def test_getLabels(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    labels = gh._getLabels(repo)

    repo.get_labels.assert_called()
    assert len(labels) == 5


def test_deleteLabel(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    label = gh._createLabel(repo, 'test')
    gh._deleteLabel(label)

    label.delete.assert_called()


def test_deleteLabels(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    labels = gh._getLabels(repo)
    gh._deleteLabels(repo)

    for label in labels:
        label.delete.assert_called()


def test_createColumn(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    project = gh._createProject(repo, 'testOrg', 'testBody')
    gh._createColumn(project, 'test')

    project.create_column.assert_called_with('test')


def test_createColumns(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    project = gh._createProject(repo, 'testOrg', 'testBody')
    gh._createColumns(project)

    assert project.create_column.call_args_list == [call('To Do'), call('In Progress'), call('Completed')]


def test_createCard(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    project = gh._createProject(repo, 'testOrg', 'testBody')
    column = gh._createColumn(project, 'test')
    issue = gh._createIssue(repo, 'testMilestone', 'testTitle', 'testBody', [])
    gh._createCard(column, issue)

    column.create_card.assert_called_with(content_id=issue.id, content_type="Issue")


def test_createIssue(mockGithub):
    gh = GitHub(token='foo')
    gh.github = mockGithub
    repo = gh._getUser().create_repo()
    gh._createIssue(repo, 'testMilestone', 'testTitle', 'testBody', [])

    repo.create_issue.assert_called_with('testTitle', body='testBody', milestone='testMilestone', labels=[])


def test_buildDescription():
    gh = GitHub(token='foo')
    task1 = Task()
    task1.title = "Test 1"
    task1.description = "This is a description 1"

    task2 = Task()
    task2.title = "Test 2"
    task2.description = "This is a description 2"

    tasks = [task1, task2]
    desc = "This is a sample feature description"

    result = gh._buildDescription(desc, tasks)
    assert result == "This is a sample feature description" \
                     "\n" \
                     "\n- [ ] **Test 1**" \
                     "\n      This is a description 1" \
                     "\n" \
                     "\n- [ ] **Test 2**" \
                     "\n      This is a description 2"


def test_deploy_withOrg(fs):
    MockedFiles._mockCorrectFileSystem(fs)

    def mock_returnNone(*args, **kwargs):
        return None

    gh = GitHub(token='foo')
    gh._createOrgRepo = MagicMock(return_value=mock_returnNone)
    gh._createUserRepo = MagicMock(return_value=mock_returnNone)
    gh._deleteLabels = MagicMock(return_value=mock_returnNone)
    gh._createProject = MagicMock(return_value=mock_returnNone)
    gh._createColumns = MagicMock(return_value=mock_returnNone)
    gh._createMilestone = MagicMock(return_value=mock_returnNone)
    gh._createIssue = MagicMock(return_value=mock_returnNone)
    gh._createCard = MagicMock(return_value=mock_returnNone)
    gh._buildDescription = MagicMock(return_value=mock_returnNone)

    backlog = Backlog()
    config = backlog._getConfig('correct')
    workItems = backlog._buildWorkItems(MockedFiles._mockParsedFileList(), config)

    args = argparse.Namespace()
    args.org = 'testOrg'
    args.repo = None
    args.project = 'testProject'
    args.backlog = 'correct'

    gh.deploy(args, workItems)
    gh._createOrgRepo.assert_called_with('testOrg', 'testProject')

    gh._deleteLabels.assert_called()
    assert gh._createProject.call_count == 4
    assert gh._createColumns.call_count == 4
    assert gh._createMilestone.call_count == 6
    assert gh._createIssue.call_count == 4
    assert gh._createCard.call_count == 4


def test_deploy_withRepo(fs):
    MockedFiles._mockCorrectFileSystem(fs)

    def mock_returnNone(*args, **kwargs):
        return None

    gh = GitHub(token='foo')
    gh._createOrgRepo = MagicMock(return_value=mock_returnNone)
    gh._createUserRepo = MagicMock(return_value=mock_returnNone)
    gh._deleteLabels = MagicMock(return_value=mock_returnNone)
    gh._createProject = MagicMock(return_value=mock_returnNone)
    gh._createColumns = MagicMock(return_value=mock_returnNone)
    gh._createMilestone = MagicMock(return_value=mock_returnNone)
    gh._createIssue = MagicMock(return_value=mock_returnNone)
    gh._createCard = MagicMock(return_value=mock_returnNone)
    gh._buildDescription = MagicMock(return_value=mock_returnNone)

    backlog = Backlog()
    config = backlog._getConfig('correct')
    workItems = backlog._buildWorkItems(MockedFiles._mockParsedFileList(), config)

    args = argparse.Namespace()
    args.org = None
    args.repo = 'testUser'
    args.project = 'testProject'
    args.backlog = 'correct'

    gh.deploy(args, workItems)
    gh._createUserRepo.assert_called_with('testProject')

    gh._deleteLabels.assert_called()
    assert gh._createProject.call_count == 4
    assert gh._createColumns.call_count == 4
    assert gh._createMilestone.call_count == 6
    assert gh._createIssue.call_count == 4
    assert gh._createCard.call_count == 4
