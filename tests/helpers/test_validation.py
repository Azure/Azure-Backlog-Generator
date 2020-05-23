from mock import Mock, MagicMock
from tests.mockedfiles import MockedFiles
import azbacklog.helpers as helpers


def test_validateMetadata():
    v = helpers.Validation()

    assert v.validateMetadata('./somepath/metadata.json', None, MockedFiles._mockConfig()) == (False, "metadata in './somepath/metadata.json' is empty")

    v._validateTitle = MagicMock(return_value=(False, "no title"))
    assert v.validateMetadata('./somepath/metadata.json', {
        'description': 'lorem desc',
        'tags': ['01_Folder'],
        'roles': []
    }, MockedFiles._mockConfig()) == (False, "no title")

    v._validateTitle = MagicMock(return_value=True)
    v._validateDescription = MagicMock(return_value=(False, "no description"))
    assert v.validateMetadata('./somepath/metadata.json', {
        'title': 'lorem ipsum',
        'tags': ['01_Folder'],
        'roles': []
    }, MockedFiles._mockConfig()) == (False, "no description")

    v._validateTitle = MagicMock(return_value=True)
    v._validateDescription = MagicMock(return_value=True)
    v._validateTags = MagicMock(return_value=(False, "no tags"))
    assert v.validateMetadata('./somepath/metadata.json', {
        'title': 'lorem ipsum',
        'description': 'lorem desc',
        'roles': []
    }, MockedFiles._mockConfig()) == (False, "no tags")

    v._validateTitle = MagicMock(return_value=True)
    v._validateDescription = MagicMock(return_value=True)
    v._validateTags = MagicMock(return_value=True)
    v._validateRoles = MagicMock(return_value=(False, "no roles"))
    assert v.validateMetadata('./somepath/metadata.json', {
        'title': 'lorem ipsum',
        'description': 'lorem desc',
        'tags': ['01_Folder']
    }, MockedFiles._mockConfig()) == (False, "no roles")

    v._validateTitle = MagicMock(return_value=True)
    v._validateDescription = MagicMock(return_value=True)
    v._validateTags = MagicMock(return_value=True)
    v._validateRoles = MagicMock(return_value=True)
    assert v.validateMetadata('./somepath/metadata.json', {
        'title': 'lorem ipsum',
        'description': 'lorem desc',
        'tags': ['01_Folder'],
        'roles': []
    }, MockedFiles._mockConfig()) is True


def test_validateTitle():
    v = helpers.Validation()
    assert v._validateTitle('./somepath/metadata.json', {}) == (False, "'title' property not found in metadata './somepath/metadata.json'")
    assert v._validateTitle('./somepath/metadata.json', {'title': ''}) == (False, "'title' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validateTitle('./somepath/metadata.json', {'title': 10}) == (False, "'title' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validateTitle('./somepath/metadata.json', {'title': '     '}) == (False, "'title' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validateTitle('./somepath/metadata.json', {'title': 'lorem ipsum'}) == (True)


def test_validateDescription():
    v = helpers.Validation()
    assert v._validateDescription('./somepath/metadata.json', {}) == (False, "'description' property not found in metadata './somepath/metadata.json'")
    assert v._validateDescription('./somepath/metadata.json', {'description': ''}) == (False, "'description' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validateDescription('./somepath/metadata.json', {'description': 10}) == (False, "'description' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validateDescription('./somepath/metadata.json', {'description': '     '}) == (False, "'description' property not formatted correctly in metadata './somepath/metadata.json'")
    assert v._validateDescription('./somepath/metadata.json', {'description': 'lorem ipsum'}) == (True)


def test_validateTags():
    v = helpers.Validation()
    assert v._validateTags('./somepath/metadata.json', {}, MockedFiles._mockConfig()) == (False, "'tags' property not found in metadata './somepath/metadata.json'")
    assert v._validateTags('./somepath/metadata.json', {'tags': 'lorem ipsum'}, MockedFiles._mockConfig()) == (False, "'tags' property is not in correct format in metadata './somepath/metadata.json'")
    assert v._validateTags('./somepath/metadata.json', {'tags': ['lorem ipsum']}, MockedFiles._mockConfig()) == (False, "invalid tag 'lorem ipsum' in metadata './somepath/metadata.json'")
    assert v._validateTags('./somepath/metadata.json', {'tags': ['01_Folder']}, MockedFiles._mockConfig()) is True


def test_validateRoles():
    v = helpers.Validation()
    assert v._validateRoles('./somepath/metadata.json', {}, MockedFiles._mockConfig()) == (False, "'roles' property not found in metadata './somepath/metadata.json'")
    assert v._validateRoles('./somepath/metadata.json', {'roles': 'lorem ipsum'}, MockedFiles._mockConfig()) == (False, "'roles' property is not in correct format in metadata './somepath/metadata.json'")
    assert v._validateRoles('./somepath/metadata.json', {'roles': ['lorem ipsum']}, MockedFiles._mockConfig()) == (False, "invalid role 'lorem ipsum' in metadata './somepath/metadata.json'")
    assert v._validateRoles('./somepath/metadata.json', {'roles': ['AppDev']}, MockedFiles._mockConfig()) is True


def test_validateConfig():
    v = helpers.Validation()
    assert v.validateConfig('./somepath/config.json', None) == (False, "configuration in './somepath/config.json' is empty")
    assert v.validateConfig('./somepath/config.json', {'foo': 'bar'}) == (False, "value 'foo' not allowed in configuration './somepath/config.json'")
    assert v.validateConfig('./somepath/config.json', {'roles': ['AppDev']}) == (False, "expected value 'tags' not found in configuration './somepath/config.json'")
    assert v.validateConfig('./somepath/config.json', {'tags': ['0f_Folder'], 'roles': ['AppDev']}) is True
