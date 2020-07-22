from mock import Mock, MagicMock
from tests.mockedfiles import MockedFiles
import azbacklog.helpers as helpers


def test_validate_metadata():
    v = helpers.Validation()

    assert v.validate_metadata('./somepath/metadata.json', None, MockedFiles._mock_config()) == (False, "metadata in './somepath/metadata.json' is empty")

    v._validate_title = MagicMock(return_value=(False, "no title"))
    assert v.validate_metadata('./somepath/metadata.json', {
        'description': 'lorem desc',
        'tags': ['01_Folder'],
        'roles': []
    }, MockedFiles._mock_config()) == (False, "no title")

    v._validate_title = MagicMock(return_value=True)
    v._validate_description = MagicMock(return_value=(False, "no description"))
    assert v.validate_metadata('./somepath/metadata.json', {
        'title': 'lorem ipsum',
        'tags': ['01_Folder'],
        'roles': []
    }, MockedFiles._mock_config()) == (False, "no description")

    v._validate_title = MagicMock(return_value=True)
    v._validate_description = MagicMock(return_value=True)
    v._validate_tags = MagicMock(return_value=(False, "no tags"))
    assert v.validate_metadata('./somepath/metadata.json', {
        'title': 'lorem ipsum',
        'description': 'lorem desc',
        'roles': []
    }, MockedFiles._mock_config()) == (False, "no tags")

    v._validate_title = MagicMock(return_value=True)
    v._validate_description = MagicMock(return_value=True)
    v._validate_tags = MagicMock(return_value=True)
    v._validate_roles = MagicMock(return_value=(False, "no roles"))
    assert v.validate_metadata('./somepath/metadata.json', {
        'title': 'lorem ipsum',
        'description': 'lorem desc',
        'tags': ['01_Folder']
    }, MockedFiles._mock_config()) == (False, "no roles")

    v._validate_title = MagicMock(return_value=True)
    v._validate_description = MagicMock(return_value=True)
    v._validate_tags = MagicMock(return_value=True)
    v._validate_roles = MagicMock(return_value=True)
    assert v.validate_metadata('./somepath/metadata.json', {
        'title': 'lorem ipsum',
        'description': 'lorem desc',
        'tags': ['01_Folder'],
        'roles': []
    }, MockedFiles._mock_config()) is True


def test_validate_title():
    v = helpers.Validation()
    assert v._validate_title('./somepath/metadata.json', {}) == (False, "'title' property not found in metadata './somepath/metadata.json'")
    assert v._validate_title('./somepath/metadata.json', {'title': ''}) == (False, "'title' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validate_title('./somepath/metadata.json', {'title': 10}) == (False, "'title' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validate_title('./somepath/metadata.json', {'title': '     '}) == (False, "'title' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validate_title('./somepath/metadata.json', {'title': 'lorem ipsum'}) == (True)


def test_validate_description():
    v = helpers.Validation()
    assert v._validate_description('./somepath/metadata.json', {}) == (False, "'description' property not found in metadata './somepath/metadata.json'")
    assert v._validate_description('./somepath/metadata.json', {'description': ''}) == (True)
    assert v._validate_description('./somepath/metadata.json', {'description': 10}) == (False, "'description' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validate_description('./somepath/metadata.json', {'description': '     '}) == (True)
    assert v._validate_description('./somepath/metadata.json', {'description': 'lorem ipsum'}) == (True)


def test_validate_tags():
    v = helpers.Validation()
    assert v._validate_tags('./somepath/metadata.json', {}, MockedFiles._mock_config()) == (False, "'tags' property not found in metadata './somepath/metadata.json'")
    assert v._validate_tags('./somepath/metadata.json', {'tags': 'lorem ipsum'}, MockedFiles._mock_config()) == (False, "'tags' property is not in correct format in metadata './somepath/metadata.json'")
    assert v._validate_tags('./somepath/metadata.json', {'tags': ['lorem ipsum']}, MockedFiles._mock_config()) == (False, "invalid tag 'lorem ipsum' in metadata './somepath/metadata.json'")
    assert v._validate_tags('./somepath/metadata.json', {'tags': ['01_Folder']}, MockedFiles._mock_config()) is True


def test_validate_roles():
    v = helpers.Validation()
    assert v._validate_roles('./somepath/metadata.json', {}, MockedFiles._mock_config()) == (False, "'roles' property not found in metadata './somepath/metadata.json'")
    assert v._validate_roles('./somepath/metadata.json', {'roles': 'lorem ipsum'}, MockedFiles._mock_config()) == (False, "'roles' property is not in correct format in metadata './somepath/metadata.json'")
    assert v._validate_roles('./somepath/metadata.json', {'roles': ['lorem ipsum']}, MockedFiles._mock_config()) == (False, "invalid role 'lorem ipsum' in metadata './somepath/metadata.json'")
    assert v._validate_roles('./somepath/metadata.json', {'roles': ['AppDev']}, MockedFiles._mock_config()) is True


def test_validate_config():
    v = helpers.Validation()
    assert v.validate_config('./somepath/config.json', None) == (False, "configuration in './somepath/config.json' is empty")
    assert v.validate_config('./somepath/config.json', {'foo': 'bar'}) == (False, "value 'foo' not allowed in configuration './somepath/config.json'")
    assert v.validate_config('./somepath/config.json', {'description': 'Sample description', 'roles': ['AppDev']}) == (False, "expected value 'tags' not found in configuration './somepath/config.json'")
    assert v.validate_config('./somepath/config.json', {'description': 'Sample description', 'tags': ['0f_Folder'], 'roles': ['AppDev']}, 'github') == (False, "GitHub requires value 'tagcolors' in configuration './somepath/config.json'")
    assert v.validate_config('./somepath/config.json', {'description': 'Sample description', 'tags': ['0f_Folder'], 'roles': ['AppDev'], 'tagcolors': ["d73a4a", "0075ca", "cfd3d7"]}, 'validate') == (False, "length of 'tagcolors' should equal the combined number of tags and roles")
    assert v.validate_config('./somepath/config.json', {'description': 'Sample description', 'tags': ['0f_Folder'], 'roles': ['AppDev'], 'tagcolors': ["d73a4a", "0075ca", "cfd3d7"]}) is True      # will pass even though 'tagcolors' is different length since repo_type has not been set to 'github' or 'validate'
    assert v.validate_config('./somepath/config.json', {'description': 'Sample description', 'tags': ['0f_Folder'], 'roles': ['AppDev']}) is True                                                   # will pass since 'tagcolors' is optional when repo_type has not been set to 'github' or 'validate'
    assert v.validate_config('./somepath/config.json', {'description': 'Sample description', 'tags': ['0f_Folder'], 'roles': ['AppDev'], 'tagcolors': ["d73a4a", "0075ca"]}) is True
