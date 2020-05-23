import pytest
from typing import List
import azbacklog.entities as entities


def test_initTag():
    t = entities.Tag()
    assert isinstance(t, entities.Tag)


def test_setTitleToString():
    t = entities.Tag()
    t.title = "Test"
    assert t.title == "Test"


def test_setTitleToNumber():
    t = entities.Tag()

    with pytest.raises(TypeError) as exc:
        t.title = 42
    assert "value must be a string" in str(exc.value)
