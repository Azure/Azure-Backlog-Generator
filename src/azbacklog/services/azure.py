from azure.devops.connection import Connection
from azure.devops.v5_1.core import TeamProject
from msrest.authentication import BasicAuthentication
from types import SimpleNamespace
import time


class AzDevOps():

    def __init__(self, org=None, token=None):
        self.clients = self._auth(org, token)

    def _auth(self, org, token):
        if org is None or token is None:
            raise ValueError("incorrect parameters were passed")

        credentials = BasicAuthentication('', token)
        print(credentials.header)
        connection = Connection(base_url=f'https://dev.azure.com/{org}', creds=credentials)

        return connection.clients

    def _get_project(self, name):
        core_client = self.clients.get_core_client()

        attempts = 0
        while (attempts < 20):
            projects = core_client.get_projects()
            for project in projects.value:
                if project.name == name:
                    return project

            time.sleep(3)
            attempts += 1

        return None

    def _check_status(self, ops_id):
        ops_client = self.clients.get_operations_client()

        while (True):
            ops_status = ops_client.get_operation(ops_id)
            if ops_status.status == 'cancelled' or ops_status.status == 'failed':
                return False
            elif ops_status.status == 'succeeded':
                return True
            else:
                time.sleep(3)

    def _create_project(self, name):
        core_client = self.clients.get_core_client()
        capabilities = {'versioncontrol': {'sourceControlType': 'Git'},
                        'processTemplate': {'templateTypeId': 'adcc42ab-9882-485e-a3ed-7678f01f66bc'}}
        project = TeamProject(name=name, description=None, visibility='private', capabilities=capabilities)
        ops_ref = core_client.queue_create_project(project)
        ops_result = self._check_status(ops_ref.id)

        if ops_result is False:
            raise RuntimeError('failed creating project')
        else:
            return True

    def _get_team(self, project, name):
        core_client = self.clients.get_core_client()
        teams = core_client.get_teams(project.id)
        for team in teams:
            if team.name == name + " Team":
                return team

        return None

    def _enable_epics(self, project, name):
        work_client = self.clients.get_work_client()
        team = self._get_team(project, name)

        patch = {
            "backlogVisibilities": {
                "Microsoft.EpicCategory": 'true',
                "Microsoft.FeatureCategory": 'true',
                "Microsoft.RequirementCategory": 'true'
            }
        }

        team_context = SimpleNamespace(**dict(
            team_id=team.id,
            project_id=team.project_id
        ))

        return work_client.update_team_settings(patch, team_context)

    def _create_tags(self, tags):
        tagList = []
        if len(tags) == 0:
            return None

        for tag in tags:
            tagList.append(tag.title)

        return "; ".join(tagList)

    def _create_work_item(self, project, wit_type, title, description, tags=None, parent=None):
        wit_client = self.clients.get_work_item_tracking_client()
        patch = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": title
            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": description
            }
        ]

        if tags is not None:
            patch.append(
                {
                    "op": "add",
                    "path": "/fields/System.Tags",
                    "value": tags
                }
            )

        if parent is not None:
            patch.append(
                {
                    "op": "add",
                    "path": "/relations/-",
                    "value": {
                        "rel": "System.LinkTypes.Hierarchy-Reverse",
                        "url": parent.url
                    }
                }
            )

        return wit_client.create_work_item(patch, project, wit_type)

    def deploy(self, config, work_items):
        print("┌── Creating project (" + config.org + "/" + config.project + ")...")
        self._create_project(config.project)
        project = self._get_project(config.project)

        print("├── Enabling epics visibility in backlog...")
        self._enable_epics(project, config.project)

        epic_count = 1
        for epic in work_items:
            if epic_count < len(work_items):
                print("├── Creating epic: " + epic.title + "...")
                epic_string = "│   "
            else:
                print("└── Creating epic: " + epic.title + "...")
                epic_string = "    "
            created_epic = self._create_work_item(project.id, 'epic', epic.title, epic.description, tags=self._create_tags(epic.tags))

            feature_count = 1
            for feature in epic.features:
                if (feature_count == len(epic.features)):
                    print(epic_string + "└── Creating feature: " + feature.title + "...")
                    feature_string = epic_string + "    "
                else:
                    print(epic_string + "├── Creating feature: " + feature.title + "...")
                    feature_string = epic_string + "│   "
                created_feature = self._create_work_item(project.id, 'feature', feature.title, feature.description, tags=self._create_tags(feature.tags), parent=created_epic)

                story_count = 1
                for story in feature.userStories:
                    if story_count == len(feature.userStories):
                        print(feature_string + "└── Creating user story: " + story.title + "...")
                        story_string = feature_string + "    "
                    else:
                        print(feature_string + "├── Creating user story: " + story.title + "...")
                        story_string = feature_string + "│   "
                    created_story = self._create_work_item(project.id, 'user story', story.title, story.description, tags=self._create_tags(story.tags), parent=created_feature)

                    task_count = 1
                    for task in story.tasks:
                        if task_count == len(story.tasks):
                            print(story_string + "    └── Creating task: " + task.title + "...")
                        else:
                            print(story_string + "    ├── Creating task: " + task.title + "...")
                        self._create_work_item(project.id, 'task', task.title, task.description, tags=self._create_tags(task.tags), parent=created_story)

                        task_count += 1

                    story_count += 1

                feature_count += 1

            epic_count += 1
