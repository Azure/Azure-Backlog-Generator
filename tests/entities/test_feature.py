import pytest
from typing import List
import azbacklog.entities as entities


def test_initFeature():
    f = entities.Feature()
    assert isinstance(f, entities.Feature)
    assert isinstance(f.userStories, List)
    assert len(f.userStories) == 0
    assert isinstance(f.tags, List)
    assert len(f.tags) == 0


def test_setTitleToString():
    f = entities.Feature()
    f.title = "Test"
    assert f.title == "Test"


def test_setTitleToNumber():
    f = entities.Feature()

    with pytest.raises(TypeError) as exc:
        f.title = 42
    assert "value must be a string" in str(exc.value)


def test_setDescriptionToString():
    f = entities.Feature()
    f.description = "Test"
    assert f.description == "Test"


def test_setDescriptionToNumber():
    f = entities.Feature()

    with pytest.raises(TypeError) as exc:
        f.description = 42
    assert "value must be a string" in str(exc.value)


def test_addStoriesToUserStoryList():
    f = entities.Feature()
    for r in range(5):
        s = entities.UserStory()
        f.addUserStory(s)

    assert len(f.userStories) == 5
    assert isinstance(f.userStories, List)
    assert isinstance(f.userStories[0], entities.UserStory)


def test_addGenericsToUserStoryList():
    f = entities.Feature()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            f.addUserStory(r)
    assert "value must be of type 'UserStory'" in str(exc.value)


def test_addTagsToTagList():
    f = entities.Feature()
    for r in range(5):
        t = entities.Tag()
        f.addTag(t)

    assert len(f.tags) == 5
    assert isinstance(f.tags, List)
    assert isinstance(f.tags[0], entities.Tag)


def test_addGenericsToTagList():
    f = entities.Feature()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            f.addTag(r)
    assert "value must be of type 'Tag'" in str(exc.value)
