from typing import List
from .userstory import UserStory
from .tag import Tag


class Feature():

    def __init__(self):
        self._userStories = []
        self._tags = []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        self._title = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        self._description = value

    @property
    def userStories(self) -> List[UserStory]:
        return self._userStories

    def addUserStory(self, value: UserStory):
        if not isinstance(value, UserStory):
            raise TypeError("value must be of type 'UserStory'")
        self._userStories.append(value)

    @property
    def tags(self) -> List[Tag]:
        return self._tags

    def addTag(self, value: Tag):
        if not isinstance(value, Tag):
            raise TypeError("value must be of type 'Tag'")
        self._tags.append(value)
