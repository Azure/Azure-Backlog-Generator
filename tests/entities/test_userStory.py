import pytest
from typing import List
import azbacklog.entities as entities


def test_initUserStory():
    s = entities.UserStory()
    assert isinstance(s, entities.UserStory)
    assert isinstance(s.tasks, List)
    assert len(s.tasks) == 0
    assert isinstance(s.tags, List)
    assert len(s.tags) == 0


def test_setTitleToString():
    s = entities.UserStory()
    s.title = "Test"
    assert s.title == "Test"


def test_setTitleToNumber():
    s = entities.UserStory()

    with pytest.raises(TypeError) as exc:
        s.title = 42
    assert "value must be a string" in str(exc.value)


def test_setDescriptionToString():
    s = entities.UserStory()
    s.description = "Test"
    assert s.description == "Test"


def test_setDescriptionToNumber():
    s = entities.UserStory()

    with pytest.raises(TypeError) as exc:
        s.description = 42
    assert "value must be a string" in str(exc.value)


def test_addTasksToTaskList():
    s = entities.UserStory()
    for r in range(5):
        t = entities.Task()
        s.addTask(t)

    assert len(s.tasks) == 5
    assert isinstance(s.tasks, List)
    assert isinstance(s.tasks[0], entities.Task)


def test_addGenericsToFeatureList():
    s = entities.UserStory()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            s.addTask(r)
    assert "value must be of type 'Task'" in str(exc.value)


def test_addTagsToTagList():
    s = entities.UserStory()
    for r in range(5):
        t = entities.Tag()
        s.addTag(t)

    assert len(s.tags) == 5
    assert isinstance(s.tags, List)
    assert isinstance(s.tags[0], entities.Tag)


def test_addGenericsToTagList():
    s = entities.UserStory()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            s.addTag(r)
    assert "value must be of type 'Tag'" in str(exc.value)
