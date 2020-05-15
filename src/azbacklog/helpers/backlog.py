import json
from .filesystem import FileSystem
from .parser import Parser
from .validation import Validation
from .. import entities

class Backlog():

    def _gatherWorkItems(self, path):
        fs = FileSystem()
        files = fs.getFiles(path)
        
        return files

    def _getConfig(self, path):
        fs = FileSystem()
        content = fs.readFile(path + '/config.json')

        parser = Parser()
        json = parser.json(content)

        val = Validation()
        validConfig = val.validateConfig(path, json)
        if validConfig == True:
            return json
        else:
            raise ValueError(f"configuration file not valid: {validConfig[1]}")

    def _parseWorkItems(self, files):
        parser = Parser()
        parsedFiles = parser.fileHierarchy(files)

        return parsedFiles

    def _getAndValidateJson(self, path, config):
        fs = FileSystem()
        content = fs.readFile(path)

        parser = Parser()
        json = parser.json(content)

        val = Validation()
        if val.validateMetadata(path, json, config):
            return json
        else:
            return False

    def _buildWorkItems(self, parsedFiles, config):
        epics = []
        for epic in parsedFiles:
            builtEpic = self._buildEpic(epic, config)
            if builtEpic != None:
                epics.append(builtEpic)

        return epics

    def _createTag(self, title):
        tag = entities.Tag()
        tag.title = title

        return tag

    def _buildEpic(self, item, config):
        json = self._getAndValidateJson(item["epic"], config)
        if json != False:
            epic = entities.Epic()
            epic.title = json["title"]
            epic.description = json["description"]
            for tag in json["tags"]:
                epic.addTag(self._createTag(tag))
            for role in json["roles"]:
                epic.addTag(self._createTag(role))
            
            if "features" in item.keys() and len(item["features"]) > 0:
                for feature in item["features"]:
                    builtFeature = self._buildFeature(feature, config)
                    if builtFeature != None:
                        epic.addFeature(builtFeature)

            return epic
        else:
            return None

    def _buildFeature(self, item, config):
        json = self._getAndValidateJson(item["feature"], config)
        if json != False:
            feature = entities.Feature()
            feature.title = json["title"]
            feature.description = json["description"]
            for tag in json["tags"]:
                feature.addTag(self._createTag(tag))
            for role in json["roles"]:
                feature.addTag(self._createTag(role))
            
            if "stories" in item.keys() and len(item["stories"]) > 0:
                for story in item["stories"]:
                    builtStory = self._buildStory(story, config)
                    if builtStory != None:
                        feature.addUserStory(builtStory)

            return feature
        else:
            return None

    def _buildStory(self, item, config):
        json = self._getAndValidateJson(item["story"], config)
        if json != False:
            story = entities.UserStory()
            story.title = json["title"]
            story.description = json["description"]
            for tag in json["tags"]:
                story.addTag(self._createTag(tag))
            for role in json["roles"]:
                story.addTag(self._createTag(role))
            
            if "tasks" in item.keys() and len(item["tasks"]) > 0:
                for task in item["tasks"]:
                    builtTask = self._buildTask(task, config)
                    if builtTask != None:
                        story.addTask(builtTask)

            return story
        else:
            return None

    def _buildTask(self, item, config):
        json = self._getAndValidateJson(item["task"], config)
        if json != False:
            task = entities.Task()
            task.title = json["title"]
            task.description = json["description"]
            for tag in json["tags"]:
                task.addTag(self._createTag(tag))
            for role in json["roles"]:
                task.addTag(self._createTag(role))
 
            return task
        else:
            return None

    def build(self, path, validateOnly=False):
        if validateOnly: print(f"Validating metadata ({path})...")

        files = self._gatherWorkItems(path)
        config = self._getConfig(path)
        parsedFiles = self._parseWorkItems(files)
        workItems = self._buildWorkItems(parsedFiles, config)       