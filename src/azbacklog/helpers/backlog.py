from .filesystem import FileSystem
from .parser import Parser
from .validation import Validation
from .. import entities
from .. import services


class Backlog():

    def _gather_work_items(self, path):
        fs = FileSystem()
        files = fs.get_files(path)

        return files

    def _get_config(self, path):
        fs = FileSystem()
        content = fs.read_file(path + '/config.json')

        parser = Parser()
        json = parser.parse_json(content)

        val = Validation()
        valid_config = val.validate_config(path, json)
        if valid_config is True:
            return json
        else:
            raise ValueError(f"configuration file not valid: {valid_config[1]}")

    def _parse_work_items(self, files):
        parser = Parser()
        parsed_files = parser.parse_file_hierarchy(files)

        return parsed_files

    def _get_and_validate_json(self, path, config):
        fs = FileSystem()
        content = fs.read_file(path)

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
            built_epic = self._build_epic(epic, config)
            if built_epic is not None:
                epics.append(built_epic)

        return epics

    def _create_tag(self, title):
        tag = entities.Tag()
        tag.title = title

        return tag

    def _build_epic(self, item, config):
        json = self._get_and_validate_json(item["epic"], config)
        if json is not False:
            epic = entities.Epic()
            epic.title = json["title"]
            epic.description = json["description"]
            for tag in json["tags"]:
                epic.add_tag(self._create_tag(tag))
            for role in json["roles"]:
                epic.add_tag(self._create_tag(role))

            if "features" in item.keys() and len(item["features"]) > 0:
                for feature in item["features"]:
                    built_feature = self._build_feature(feature, config)
                    if built_feature is not None:
                        epic.add_feature(built_feature)

            return epic
        else:
            return None

    def _build_feature(self, item, config):
        json = self._get_and_validate_json(item["feature"], config)
        if json is not False:
            feature = entities.Feature()
            feature.title = json["title"]
            feature.description = json["description"]
            for tag in json["tags"]:
                feature.add_tag(self._create_tag(tag))
            for role in json["roles"]:
                feature.add_tag(self._create_tag(role))

            if "stories" in item.keys() and len(item["stories"]) > 0:
                for story in item["stories"]:
                    built_story = self._build_story(story, config)
                    if built_story is not None:
                        feature.add_userstory(built_story)

            return feature
        else:
            return None

    def _build_story(self, item, config):
        json = self._get_and_validate_json(item["story"], config)
        if json is not False:
            story = entities.UserStory()
            story.title = json["title"]
            story.description = json["description"]
            for tag in json["tags"]:
                story.add_tag(self._create_tag(tag))
            for role in json["roles"]:
                story.add_tag(self._create_tag(role))

            if "tasks" in item.keys() and len(item["tasks"]) > 0:
                for task in item["tasks"]:
                    built_task = self._build_task(task, config)
                    if built_task is not None:
                        story.add_task(built_task)

            return story
        else:
            return None

    def _build_task(self, item, config):
        json = self._get_and_validate_json(item["task"], config)
        if json is not False:
            task = entities.Task()
            task.title = json["title"]
            task.description = json["description"]
            for tag in json["tags"]:
                task.add_tag(self._create_tag(tag))
            for role in json["roles"]:
                task.add_tag(self._create_tag(role))

            return task
        else:
            return None

    def _deploy_github(self, args, workitems):
        github = services.GitHub(token=args.token)
        github.deploy(args, workitems)

    def _deploy_azure(self, args, workitems):
        azure = services.AzDevOps(org=args.org, token=args.token)
        azure.deploy(args, workitems)

    def build(self, args):
        if args.validate_only is not None:
            path = args.validate_only
            print(f"Validating metadata ({path})...")
        else:
            path = FileSystem.find_work_items() + args.backlog

        files = self._gather_work_items(path)
        config = self._get_config(path)
        parsed_files = self._parse_work_items(files)
        work_items = self._build_work_items(parsed_files, config)

        if args.validate_only is None:
            if args.repo.lower() == 'github':
                self._deploy_github(args, work_items)
            elif args.repo.lower() == 'azure':
                self._deploy_azure(args, work_items)
