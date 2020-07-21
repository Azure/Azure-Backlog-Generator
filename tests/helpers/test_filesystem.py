import os
import pytest
from pyfakefs import fake_filesystem
from tests.mockedfiles import MockedFiles
import azbacklog.helpers as helpers


def test_get_files_correct_file_system(fs):
    MockedFiles._mock_correct_file_system(fs)

    f = helpers.FileSystem()
    files = f.get_files('./workitems/correct')
    assert len(files) == 20


def test_get_files_parent_path_has_file_file_system(fs):
    MockedFiles._mock_parent_path_has_file_file_system(fs)

    f = helpers.FileSystem()
    with pytest.raises(FileExistsError) as exc:
        files = f.get_files('./parentPathHasFile')  # NOQA
    assert "parent path should not contain any files" in str(exc.value)


def test_get_files_path_has_no_metadata(fs):
    MockedFiles._mock_path_has_no_metadata_file_system(fs)

    f = helpers.FileSystem()
    with pytest.raises(FileNotFoundError) as exc:
        files = f.get_files('./pathHasNoMetadata')  # NOQA
    assert "'metadata.json' does not exist in path './pathHasNoMetadata/01_folder'" in str(exc.value)


def test_read_file(fs):
    test_content = '{ "foo": "bar" }'
    fs.create_file('./testFilePath/testfile.json', contents=test_content)

    f = helpers.FileSystem()
    read_content = f.read_file('./testFilePath/testfile.json')

    assert read_content == test_content

    with pytest.raises(FileNotFoundError) as exc:
        content = f.read_file('./testFilePath/notexist.json')  # NOQA
    assert "'./testFilePath/notexist.json' does not exist" in str(exc.value)
