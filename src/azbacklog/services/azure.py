from azure.devops.connection import Connection
from azure.devops.v5_1.core import TeamProject
from msrest.authentication import BasicAuthentication
from types import SimpleNamespace
import time

class AzDevOps():

    def __init__(self, org=None, token=None):
        if org is not None and token is not None:
            self.clients = self._auth(org, token)
        else:
            raise ValueError("incorrect parameters were passed")

    def _auth(self, org, token):
        credentials = BasicAuthentication('', token)
        connection = Connection(base_url=f'https://dev.azure.com/{org}', creds=credentials)

        return connection.clients

    def _getProject(self, name):
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

    def _createProject(self, name):
        core_client = self.clients.get_core_client()
        capabilities = { 'versioncontrol' : { 'sourceControlType' : 'Git' }, 
                         'processTemplate' : { 'templateTypeId' : 'adcc42ab-9882-485e-a3ed-7678f01f66bc' }}
        project = TeamProject(name=name, description=None, visibility='private', capabilities=capabilities)
        ops_ref = core_client.queue_create_project(project)
        ops_client = self.clients.get_operations_client()
        done = False
        while (not done):
            ops_status = ops_client.get_operation(ops_ref.id)
            if ops_status.status == 'cancelled' or ops_status.status == 'failed':
                raise RuntimeError('failed creating project')
            done = ops_status.status == 'succeeded'

    def _getTeam(self, project, name):
        core_client = self.clients.get_core_client()
        teams = core_client.get_teams(project.id)
        for team in teams:
            if team.name == name + " Team":
                return team

        return None

    def _enableEpics(self, project, name):
        work_client = self.clients.get_work_client()
        team = self._getTeam(project, name)

        patch =  {
            "backlogVisibilities": {
                "Microsoft.EpicCategory": 'true',
                "Microsoft.FeatureCategory": 'true',
                "Microsoft.RequirementCategory": 'true'
            }
        }
        team_context = SimpleNamespace(**dict(
            team_id = team.id,
            project_id = team.project_id
        ))
        return work_client.update_team_settings(patch, team_context)

    def _createTags(self, tags):
        tagList = []
        if len(tags) == 0:
            return None

        for tag in tags:
            tagList.append(tag.title)

        return "; ".join(tagList)

    def _createWorkItem(self, project, witType, title, description, tags=None, parent=None):
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
                        "rel" : "System.LinkTypes.Hierarchy-Reverse",
                        "url" : parent.url
                    }
                }
            )
        
        return wit_client.create_work_item(patch, project, witType)

    def deploy(self, config, workitems):
        print("┌── Creating project (" + config.org + "/" + config.project + ")...")
        self._createProject(config.project)
        project = self._getProject(config.project)

        print("├── Enabling epics visibility in backlog...")
        team = self._enableEpics(project, config.project)

        epicCnt = 1
        featCnt = 1
        for epic in workitems:
            if epicCnt < len(workitems):
                print("├── Creating epic: " + epic.title + "...")
                epicStr = "│   "
            else:
                print("└── Creating epic: " + epic.title + "...")
                epicStr = "    "
            witEpic = self._createWorkItem(project.id, 'epic', epic.title, epic.description, tags=self._createTags(epic.tags))

            epicFeatCnt = 1
            for feature in epic.features:
                if (epicFeatCnt == len(epic.features)):
                    print(epicStr + "└── Creating feature: " + feature.title + "...")
                    featureStr = epicStr + "    "
                else:
                    print(epicStr + "├── Creating feature: " + feature.title + "...")
                    featureStr = epicStr + "│   "
                witFeature = self._createWorkItem(project.id, 'feature', feature.title, feature.description, tags=self._createTags(feature.tags), parent=witEpic)

                storyCnt = 1
                for story in feature.userStories:
                    if storyCnt == len(feature.userStories):
                        print(featureStr + "└── Creating user story: " + story.title + "...")
                        storyStr = featureStr + "    "
                    else:
                        print(featureStr + "├── Creating user story: " + story.title + "...")
                        storyStr = featureStr + "│   "
                    witUserStory = self._createWorkItem(project.id, 'user story', story.title, story.description, tags=self._createTags(story.tags), parent=witFeature)

                    taskCnt = 1
                    for task in story.tasks:
                        if taskCnt == len(story.tasks):
                            print(storyStr + "    └── Creating task: " + task.title + "...")
                        else:
                            print(storyStr + "    ├── Creating task: " + task.title + "...")
                        witTask = self._createWorkItem(project.id, 'task', task.title, task.description, tags=self._createTags(task.tags), parent=witUserStory)

                        taskCnt += 1

                    storyCnt += 1

                epicFeatCnt += 1
                featCnt += 1

            epicCnt += 1       

