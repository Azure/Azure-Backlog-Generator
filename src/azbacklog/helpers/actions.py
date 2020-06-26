import argparse


class TokenAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        self.validate(parser, value, namespace)
        setattr(namespace, self.dest, value)

    @staticmethod
    def validate(parser, value, namespace):
        if value is None or value.strip() == '':
            parser.error('User access token is required')
        return True


class RepoAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        self.validate(parser, value, namespace)
        setattr(namespace, self.dest, value)

    @staticmethod
    def validate(parser, value, namespace):
        if value.strip() not in ('azure', 'github'):
            parser.error('Repository type must be either \'azure\' or \'github\'')
        return True


class ProjectAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        self.validate(parser, value, namespace)
        setattr(namespace, self.dest, value)

    @staticmethod
    def validate(parser, value, namespace):
        if value is None or value.strip() == '':
            parser.error('Project name is required')
        return True


class OrgAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        self.validate(parser, value, namespace)
        setattr(namespace, self.dest, value)

    @staticmethod
    def validate(parser, value, namespace):
        if (value is None or value.strip() == '') and namespace.repo == 'azure':
            parser.error('Organization name is required')
        return True


class BacklogAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        self.validate(parser, value, namespace)
        setattr(namespace, self.dest, value)

    @staticmethod
    def validate(parser, value, namespace):
        if value.strip() not in ('caf', 'tfs'):
            parser.error('Backlog must be a valid option')
        return True
