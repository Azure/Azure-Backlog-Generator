from tests.mockedfiles import MockedFiles
import azbacklog.helpers as helpers


def test_parse_links():
    p = helpers.Parser()
    assert p.parse_links('This is a sample [link](http://google.com).') == 'This is a sample <a href="http://google.com">link</a>.'


def test_parse_json():
    p = helpers.Parser()
    assert p.parse_json('{}') == {}
    assert p.parse_json('{ "test" : "" } ') == {"test": ""}
    assert p.parse_json('{ "test" : "lorem ipsum" } ') == {"test": "lorem ipsum"}
    assert p.parse_json('{ ')[0] is False
    assert len(p.parse_json('{ ')[1]) == 1
    assert ("Expecting property name enclosed in double quotes" in p.parse_json('{ ')[1][0]) is True


def test_isvalid_string():
    p = helpers.Parser()
    assert p.isvalid_string(None) is False
    assert p.isvalid_string("") is False
    assert p.isvalid_string(10) is False
    assert p.isvalid_string("     ") is False
    assert p.isvalid_string("", True) is True
    assert p.isvalid_string("     ", True) is True


def test_parse_file_hierarchy():
    p = helpers.Parser()
    parsed_files = p.parse_file_hierarchy(MockedFiles._mock_file_list())

    assert parsed_files == MockedFiles._mock_parsed_file_list()
