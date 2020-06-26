from github import Github


class GitHub():

    def __init__(self, username=None, password=None, hostname=None, token=None):
        self.github = self._auth(username=username, password=password, hostname=hostname, token=token)

    def _auth(self, username=None, password=None, hostname=None, token=None):
        if username is not None and password is not None:
            return Github(username, password)
        elif hostname is not None and token is not None:
            return Github(base_url=f'https://{hostname}/api/v3', login_or_token=f'{token}')
        elif token is not None:
            return Github(token)
        else:
            raise ValueError("incorrect parameters were passed")

    def _getUser(self):
        return self.github.get_user()

    def _getOrg(self, orgName):
        return self.github.get_organization(orgName)

    def _createUserRepo(self, name):
        return self._getUser().create_repo(name=f'{name}', has_issues=True, auto_init=True, private=True)

    def _createOrgRepo(self, orgName, name):
        return self._getOrg(orgName).create_repo(name=f'{name}', has_issues=True, auto_init=True, private=True)

    def _createProject(self, repo, name, body):
        return repo.create_project(name, body=body)

    def _createMilestone(self, repo, title, desc):
        return repo.create_milestone(title, description=desc)

    def _createLabel(self, repo, name):
        return repo.create_label(name)

    def _createLabels(self, repo, names):
        labels = []
        for name in names:
            labels.extend(self._createLabel(repo, name))

        return labels

    def _getLabels(self, repo):
        return repo.get_labels()

    def _deleteLabel(self, label):
        return label.delete()

    def _deleteLabels(self, repo):
        labels = self._getLabels(repo)

        for label in labels:
            self._deleteLabel(label)

    def _createColumn(self, project, name):
        return project.create_column(name)

    def _createColumns(self, project):
        todo = self._createColumn(project, "To Do")
        self._createColumn(project, "In Progress")
        self._createColumn(project, "Completed")

        return todo

    def _createCard(self, column, issue):
        return column.create_card(content_id=issue.id, content_type="Issue")

    def _createIssue(self, repo, milestone, title, body, labels):
        return repo.create_issue(title, body=body, milestone=milestone, labels=labels)

    def _buildDescription(self, desc, tasks):
        for task in tasks:
            desc += "\n"
            desc += f"\n- [ ] **{task.title}**"
            desc += f"\n      {task.description}"

        return desc

    def deploy(self, config, workitems):
        if config.org is not None:
            print("┌── Creating repo (" + config.org + "/" + config.project + ")...")
            repo = self._createOrgRepo(config.org, config.project)
        else:
            print("┌── Creating repo (" + config.repo + "/" + config.project + ")...")
            repo = self._createUserRepo(config.project)

        print("├── Deleting default labels...")
        self._deleteLabels(repo)

        print("├── Creating custom labels...")
        # TODO: Create custom tags

        projCnt = 1
        featCnt = 1
        for epic in workitems:
            if projCnt < len(workitems):
                print("├── Creating project: " + epic.title + " ({:02d}".format(projCnt) + "_" + epic.title + ")...")
                folderStr = "│   "
            else:
                print("└── Creating project: " + epic.title + " ({:02d}".format(projCnt) + "_" + epic.title + ")...")
                folderStr = "    "

            project = self._createProject(repo, "{:02d}".format(projCnt) + "_" + epic.title, epic.description)

            if len(epic.features) == 0:
                print(folderStr + "└── Creating columns...")
            else:
                print(folderStr + "├── Creating columns...")
            todoCol = self._createColumns(project)

            projFeatCnt = 1
            issues = []
            for feature in epic.features:
                print(folderStr + "├── Creating milestone: " + feature.title + " ({:02d}".format(featCnt) + "_" + feature.title + ")...")
                milestone = self._createMilestone(repo, "{:02d}".format(featCnt) + "_" + feature.title, feature.description)

                storyCnt = 1
                for story in feature.userStories:

                    if storyCnt == len(feature.userStories):
                        print(folderStr + "│   └── Creating issue: " + story.title + "...")
                    else:
                        print(folderStr + "│   ├── Creating issue: " + story.title + "...")

                    issue = self._createIssue(repo, milestone, story.title, self._buildDescription(story.description, story.tasks), [])
                    issues.append(issue)

                    storyCnt += 1
                projFeatCnt += 1
                featCnt += 1

            if len(issues) > 1:
                print(folderStr + "└── Adding issues to project...")
                for issue in reversed(issues):
                    self._createCard(todoCol, issue)

            projCnt += 1
