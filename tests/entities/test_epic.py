import pytest
from typing import List
import azbacklog.entities as entities


def test_initEpic():
    e = entities.Epic()
    assert isinstance(e, entities.Epic)
    assert isinstance(e.features, List)
    assert len(e.features) == 0
    assert isinstance(e.tags, List)
    assert len(e.tags) == 0


def test_set_title_to_string():
    e = entities.Epic()
    e.title = "Test"
    assert e.title == "Test"


def test_set_title_to_number():
    e = entities.Epic()

    with pytest.raises(TypeError) as exc:
        e.title = 42
    assert "value must be a string" in str(exc.value)


def test_set_description_to_string():
    e = entities.Epic()
    e.description = "Test"
    assert e.description == "Test"


def test_set_description_to_number():
    e = entities.Epic()

    with pytest.raises(TypeError) as exc:
        e.description = 42
    assert "value must be a string" in str(exc.value)


def test_add_features_to_feature_list():
    e = entities.Epic()
    for r in range(5):
        f = entities.Feature()
        e.add_feature(f)

    assert len(e.features) == 5
    assert isinstance(e.features, List)
    assert isinstance(e.features[0], entities.Feature)


def test_add_generics_to_feature_list():
    e = entities.Epic()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            e.add_feature(r)
    assert "value must be of type 'Feature'" in str(exc.value)


def test_add_tags_to_tag_list():
    e = entities.Epic()
    for r in range(5):
        t = entities.Tag()
        e.add_tag(t)

    assert len(e.tags) == 5
    assert isinstance(e.tags, List)
    assert isinstance(e.tags[0], entities.Tag)


def test_add_generics_to_tag_list():
    e = entities.Epic()
    with pytest.raises(TypeError) as exc:
        for r in range(5):
            e.add_tag(r)
    assert "value must be of type 'Tag'" in str(exc.value)
