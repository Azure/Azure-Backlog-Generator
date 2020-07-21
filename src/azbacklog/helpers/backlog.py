from .filesystem import FileSystem
from .parser import Parser
from .validation import Validation
from .. import entities
from .. import services


class Backlog():

    def _gatherWorkItems(self, path):
        fs = FileSystem()
        files = fs.getFiles(path)

        return files

    def _get_config(self, path):
        fs = FileSystem()
        content = fs.readFile(path + '/config.json')

        parser = Parser()
        json = parser.parse_json(content)

        val = Validation()
        valid_config = val.validate_config(path, json)
        if valid_config is True:
            return json
        else:
            raise ValueError(f"configuration file not valid: {valid_config[1]}")

    def _parseWorkItems(self, files):
        parser = Parser()
        parsed_files = parser.parse_file_hierarchy(files)

        return parsed_files

    def _getAndValidateJson(self, path, config):
        fs = FileSystem()
        content = fs.readFile(path)

        parser = Parser()
        json = parser.parse_json(content)

        val = Validation()
        validation_result = val.validate_metadata(path, json, config)
        if validation_result is True:
            return json
        else:
            raise ValueError(f"metadata not valid: {validation_result[1]}")

    def _build_work_items(self, parsed_files, config):
        epics = []
        for epic in parsed_files:
            built_epic = self._buildEpic(epic, config)
            if built_epic is not None:
                epics.append(built_epic)

        return epics

    def _createTag(self, title):
        tag = entities.Tag()
        tag.title = title

        return tag

    def _buildEpic(self, item, config):
        json = self._getAndValidateJson(item["epic"], config)
        if json is not False:
            epic = entities.Epic()
            epic.title = json["title"]
            epic.description = json["description"]
            for tag in json["tags"]:
                epic.add_tag(self._createTag(tag))
            for role in json["roles"]:
                epic.add_tag(self._createTag(role))

            if "features" in item.keys() and len(item["features"]) > 0:
                for feature in item["features"]:
                    builtFeature = self._buildFeature(feature, config)
                    if builtFeature is not None:
                        epic.add_feature(builtFeature)

            return epic
        else:
            return None

    def _buildFeature(self, item, config):
        json = self._getAndValidateJson(item["feature"], config)
        if json is not False:
            feature = entities.Feature()
            feature.title = json["title"]
            feature.description = json["description"]
            for tag in json["tags"]:
                feature.add_tag(self._createTag(tag))
            for role in json["roles"]:
                feature.add_tag(self._createTag(role))

            if "stories" in item.keys() and len(item["stories"]) > 0:
                for story in item["stories"]:
                    builtStory = self._buildStory(story, config)
                    if builtStory is not None:
                        feature.add_userstory(builtStory)

            return feature
        else:
            return None

    def _buildStory(self, item, config):
        json = self._getAndValidateJson(item["story"], config)
        if json is not False:
            story = entities.UserStory()
            story.title = json["title"]
            story.description = json["description"]
            for tag in json["tags"]:
                story.add_tag(self._createTag(tag))
            for role in json["roles"]:
                story.add_tag(self._createTag(role))

            if "tasks" in item.keys() and len(item["tasks"]) > 0:
                for task in item["tasks"]:
                    builtTask = self._buildTask(task, config)
                    if builtTask is not None:
                        story.add_task(builtTask)

            return story
        else:
            return None

    def _buildTask(self, item, config):
        json = self._getAndValidateJson(item["task"], config)
        if json is not False:
            task = entities.Task()
            task.title = json["title"]
            task.description = json["description"]
            for tag in json["tags"]:
                task.add_tag(self._createTag(tag))
            for role in json["roles"]:
                task.add_tag(self._createTag(role))

            return task
        else:
            return None

    def _deployGitHub(self, args, workitems):
        github = services.GitHub(token=args.token)
        github.deploy(args, workitems)

    def _deployAzure(self, args, workitems):
        azure = services.AzDevOps(org=args.org, token=args.token)
        azure.deploy(args, workitems)

    def build(self, args):
        if args.validate_only is not None:
            path = args.validate_only
            print(f"Validating metadata ({path})...")
        else:
            path = FileSystem.findWorkitems() + args.backlog

        files = self._gatherWorkItems(path)
        config = self._getConfig(path)
        parsedFiles = self._parseWorkItems(files)
        workItems = self._buildWorkItems(parsedFiles, config)

        if args.validate_only is None:
            if args.repo.lower() == 'github':
                self._deployGitHub(args, workItems)
            elif args.repo.lower() == 'azure':
                self._deployAzure(args, workItems)
