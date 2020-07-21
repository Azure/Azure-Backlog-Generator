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

    def _get_user(self):
        return self.github.get_user()

    def _get_org(self, orgName):
        return self.github.get_organization(orgName)

    def _create_user_repo(self, name, desc):
        return self._get_user().create_repo(name=name, description=desc, has_issues=True, auto_init=True, private=True)

    def _create_org_repo(self, org, name, desc):
        return self._get_org(org).create_repo(name=name, description=desc, has_issues=True, auto_init=True, private=True)

    def _create_project(self, repo, name, body):
        return repo.create_project(name, body=body)

    def _create_milestone(self, repo, title, desc):
        return repo.create_milestone(title, description=desc)

    def _create_label(self, repo, name):
        return repo.create_label(name)

    def _create_labels(self, repo, names):
        labels = []
        for name in names:
            labels.extend(self._create_label(repo, name))

        return labels

    def _get_labels(self, repo):
        return repo.get_labels()

    def _delete_label(self, label):
        return label.delete()

    def _delete_labels(self, repo):
        labels = self._get_labels(repo)

        for label in labels:
            self._delete_label(label)

    def _create_column(self, project, name):
        return project.create_column(name)

    def _create_columns(self, project):
        todo = self._create_column(project, "To Do")
        self._create_column(project, "In Progress")
        self._create_column(project, "Completed")

        return todo

    def _create_card(self, column, issue):
        return column.create_card(content_id=issue.id, content_type="Issue")

    def _create_issue(self, repo, milestone, title, body, labels):
        return repo.create_issue(title, body=body, milestone=milestone, labels=labels)

    def _build_description(self, desc, tasks):
        for task in tasks:
            desc += "\n"
            desc += f"\n- [ ] **{task.title}**"
            desc += f"\n      {task.description}"

        return desc

    def deploy(self, args, workitems, config):
        if args.org is not None:
            print("┌── Creating repo (" + args.org + "/" + args.project + ")...")
            repo = self._create_org_repo(args.org, args.project, config["description"])
        else:
            print("┌── Creating repo (" + args.repo + "/" + args.project + ")...")
            repo = self._create_user_repo(args.project, config["description"])

        print("├── Deleting default labels...")
        self._delete_labels(repo)

        print("├── Creating custom labels...")
        # TODO: Create custom tags

        project_count = 1
        feature_count = 1
        for epic in workitems:
            if project_count < len(workitems):
                print("├── Creating project: " + epic.title + " ({:02d}".format(project_count) + "_" + epic.title + ")...")
                folder_string = "│   "
            else:
                print("└── Creating project: " + epic.title + " ({:02d}".format(project_count) + "_" + epic.title + ")...")
                folder_string = "    "

            project = self._create_project(repo, "{:02d}".format(project_count) + "_" + epic.title, epic.description)

            if len(epic.features) == 0:
                print(folder_string + "└── Creating columns...")
            else:
                print(folder_string + "├── Creating columns...")
            todo_column = self._create_columns(project)

            project_feature_count = 1
            issues = []
            for feature in epic.features:
                print(folder_string + "├── Creating milestone: " + feature.title + " ({:02d}".format(feature_count) + "_" + feature.title + ")...")
                milestone = self._create_milestone(repo, "{:02d}".format(feature_count) + "_" + feature.title, feature.description)

                story_count = 1
                for story in feature.userstories:

                    if story_count == len(feature.userstories):
                        print(folder_string + "│   └── Creating issue: " + story.title + "...")
                    else:
                        print(folder_string + "│   ├── Creating issue: " + story.title + "...")

                    issue = self._create_issue(repo, milestone, story.title, self._build_description(story.description, story.tasks), [])
                    issues.append(issue)

                    story_count += 1
                project_feature_count += 1
                feature_count += 1

            if len(issues) > 1:
                print(folder_string + "└── Adding issues to project...")
                for issue in reversed(issues):
                    self._create_card(todo_column, issue)

            project_count += 1
