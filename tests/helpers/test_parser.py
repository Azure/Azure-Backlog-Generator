from tests.mockedfiles import MockedFiles
import src.azbacklog.helpers as helpers


def test_parse():
    p = helpers.Parser()
    assert p.links('This is a sample [link](http://google.com).') == 'This is a sample <a href="http://google.com">link</a>.'


def test_json():
    p = helpers.Parser()
    assert p.json('{}') == {}
    assert p.json('{ "test" : "" } ') == {"test": ""}
    assert p.json('{ "test" : "lorem ipsum" } ') == {"test": "lorem ipsum"}
    assert p.json('{ ')[0] is False
    assert len(p.json('{ ')[1]) == 1
    assert ("Expecting property name enclosed in double quotes" in p.json('{ ')[1][0]) is True


def test_validString():
    p = helpers.Parser()
    assert p.validString(None) is False
    assert p.validString("") is False
    assert p.validString(10) is False
    assert p.validString("     ") is False


def test_fileHierarchy():
    p = helpers.Parser()
    parsedFiles = p.fileHierarchy(MockedFiles._mockFileList())

    assert parsedFiles == MockedFiles._mockParsedFileList()
