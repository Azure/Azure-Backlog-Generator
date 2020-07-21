import pytest
from typing import List
import azbacklog.entities as entities


def test_init_epic():
    task = entities.Task()
    assert isinstance(task, entities.Task)
    assert isinstance(task.tags, List)
    assert len(task.tags) == 0


def test_set_title_to_string():
    task = entities.Task()
    task.title = "Test"
    assert task.title == "Test"


def test_set_title_to_number():
    task = entities.Task()

    with pytest.raises(TypeError) as exc:
        task.title = 42
    assert "value must be a string" in str(exc.value)


def test_set_description_to_string():
    task = entities.Task()
    task.description = "Test"
    assert task.description == "Test"


def test_set_description_to_number():
    task = entities.Task()

    with pytest.raises(TypeError) as exc:
        task.description = 42
    assert "value must be a string" in str(exc.value)


def test_add_tags_to_tag_list():
    task = entities.Task()
    for r in range(5):
        t = entities.Tag()
        task.add_tag(t)

    assert len(task.tags) == 5
    assert isinstance(task.tags, List)
    assert isinstance(task.tags[0], entities.Tag)


def test_add_generics_to_tag_list():
    task = entities.Task()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            task.add_tag(r)
    assert "value must be of type 'Tag'" in str(exc.value)
