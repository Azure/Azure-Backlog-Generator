import pytest
from typing import List
import azbacklog.entities as entities


def test_initEpic():
    task = entities.Task()
    assert isinstance(task, entities.Task)
    assert isinstance(task.tags, List)
    assert len(task.tags) == 0


def test_setTitleToString():
    task = entities.Task()
    task.title = "Test"
    assert task.title == "Test"


def test_setTitleToNumber():
    task = entities.Task()

    with pytest.raises(TypeError) as exc:
        task.title = 42
    assert "value must be a string" in str(exc.value)


def test_setDescriptionToString():
    task = entities.Task()
    task.description = "Test"
    assert task.description == "Test"


def test_setDescriptionToNumber():
    task = entities.Task()

    with pytest.raises(TypeError) as exc:
        task.description = 42
    assert "value must be a string" in str(exc.value)


def test_addTagsToTagList():
    task = entities.Task()
    for r in range(5):
        t = entities.Tag()
        task.addTag(t)

    assert len(task.tags) == 5
    assert isinstance(task.tags, List)
    assert isinstance(task.tags[0], entities.Tag)


def test_addGenericsToTagList():
    task = entities.Task()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            task.addTag(r)
    assert "value must be of type 'Tag'" in str(exc.value)
