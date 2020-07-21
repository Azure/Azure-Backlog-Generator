import pytest
from typing import List
import azbacklog.entities as entities


def test_init_UserStory():
    s = entities.UserStory()
    assert isinstance(s, entities.UserStory)
    assert isinstance(s.tasks, List)
    assert len(s.tasks) == 0
    assert isinstance(s.tags, List)
    assert len(s.tags) == 0


def test_set_title_to_string():
    s = entities.UserStory()
    s.title = "Test"
    assert s.title == "Test"


def test_set_title_to_number():
    s = entities.UserStory()

    with pytest.raises(TypeError) as exc:
        s.title = 42
    assert "value must be a string" in str(exc.value)


def test_set_description_to_string():
    s = entities.UserStory()
    s.description = "Test"
    assert s.description == "Test"


def test_set_description_to_number():
    s = entities.UserStory()

    with pytest.raises(TypeError) as exc:
        s.description = 42
    assert "value must be a string" in str(exc.value)


def test_add_tasks_to_task_list():
    s = entities.UserStory()
    for r in range(5):
        t = entities.Task()
        s.add_task(t)

    assert len(s.tasks) == 5
    assert isinstance(s.tasks, List)
    assert isinstance(s.tasks[0], entities.Task)


def test_add_generics_to_feature_list():
    s = entities.UserStory()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            s.add_task(r)
    assert "value must be of type 'Task'" in str(exc.value)


def test_add_tags_to_tag_list():
    s = entities.UserStory()
    for r in range(5):
        t = entities.Tag()
        s.add_tag(t)

    assert len(s.tags) == 5
    assert isinstance(s.tags, List)
    assert isinstance(s.tags[0], entities.Tag)


def test_add_generics_to_tag_list():
    s = entities.UserStory()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            s.add_tag(r)
    assert "value must be of type 'Tag'" in str(exc.value)
