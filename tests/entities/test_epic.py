import pytest
from typing import List
import src.azbacklog.entities as entities


def test_initEpic():
    e = entities.Epic()
    assert isinstance(e, entities.Epic)
    assert isinstance(e.features, List)
    assert len(e.features) == 0
    assert isinstance(e.tags, List)
    assert len(e.tags) == 0


def test_setTitleToString():
    e = entities.Epic()
    e.title = "Test"
    assert e.title == "Test"


def test_setTitleToNumber():
    e = entities.Epic()

    with pytest.raises(TypeError) as exc:
        e.title = 42
    assert "value must be a string" in str(exc.value)


def test_setDescriptionToString():
    e = entities.Epic()
    e.description = "Test"
    assert e.description == "Test"


def test_setDescriptionToNumber():
    e = entities.Epic()

    with pytest.raises(TypeError) as exc:
        e.description = 42
    assert "value must be a string" in str(exc.value)


def test_addFeaturesToFeatureList():
    e = entities.Epic()
    for r in range(5):
        f = entities.Feature()
        e.addFeature(f)

    assert len(e.features) == 5
    assert isinstance(e.features, List)
    assert isinstance(e.features[0], entities.Feature)


def test_addGenericsToFeatureList():
    e = entities.Epic()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            e.addFeature(r)
    assert "value must be of type 'Feature'" in str(exc.value)


def test_addTagsToTagList():
    e = entities.Epic()
    for r in range(5):
        t = entities.Tag()
        e.addTag(t)

    assert len(e.tags) == 5
    assert isinstance(e.tags, List)
    assert isinstance(e.tags[0], entities.Tag)


def test_addGenericsToTagList():
    e = entities.Epic()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            e.addTag(r)
    assert "value must be of type 'Tag'" in str(exc.value)
