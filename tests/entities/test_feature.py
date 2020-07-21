import pytest
from typing import List
import azbacklog.entities as entities


def test_init_feature():
    f = entities.Feature()
    assert isinstance(f, entities.Feature)
    assert isinstance(f.userstories, List)
    assert len(f.userstories) == 0
    assert isinstance(f.tags, List)
    assert len(f.tags) == 0


def test_set_title_to_string():
    f = entities.Feature()
    f.title = "Test"
    assert f.title == "Test"


def test_set_title_to_number():
    f = entities.Feature()

    with pytest.raises(TypeError) as exc:
        f.title = 42
    assert "value must be a string" in str(exc.value)


def test_set_description_to_string():
    f = entities.Feature()
    f.description = "Test"
    assert f.description == "Test"


def test_set_description_to_number():
    f = entities.Feature()

    with pytest.raises(TypeError) as exc:
        f.description = 42
    assert "value must be a string" in str(exc.value)


def test_add_stories_to_userstory_list():
    f = entities.Feature()
    for r in range(5):
        s = entities.UserStory()
        f.add_userstory(s)

    assert len(f.userstories) == 5
    assert isinstance(f.userstories, List)
    assert isinstance(f.userstories[0], entities.UserStory)


def test_add_generics_to_userstory_list():
    f = entities.Feature()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            f.add_userstory(r)
    assert "value must be of type 'UserStory'" in str(exc.value)


def test_add_tags_to_tag_list():
    f = entities.Feature()
    for r in range(5):
        t = entities.Tag()
        f.add_tag(t)

    assert len(f.tags) == 5
    assert isinstance(f.tags, List)
    assert isinstance(f.tags[0], entities.Tag)


def test_add_generics_to_tag_list():
    f = entities.Feature()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            f.add_tag(r)
    assert "value must be of type 'Tag'" in str(exc.value)
