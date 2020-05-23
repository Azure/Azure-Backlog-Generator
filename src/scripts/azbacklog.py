#!/usr/bin/env python3

import argparse
import src.azbacklog.helpers as helpers
import src.azbacklog.services as services


def run(args):
    bl = helpers.Backlog()
    bl.build(args)


def main():
    parser = argparse.ArgumentParser(prog='azbacklog', description="Generate a backlog of work items.", allow_abbrev=False)
    parser.add_argument('-t', '--token', action=helpers.TokenAction, help="GitHub or Azure DevOps token")
    parser.add_argument('-r', '--repo', choices=['azure', 'github'], action=helpers.RepoAction, help="targetted repository type")
    parser.add_argument('-p', '--project', action=helpers.ProjectAction, help="project (repository) name to create")
    parser.add_argument('-o', '--org', help="Optional. If the target is a GitHub organization, specify the organization's name.")
    parser.add_argument('-b', '--backlog', choices=['caf', 'tfs'], action=helpers.BacklogAction, help="type of backlog to create")
    parser.add_argument('--validate-only', help=argparse.SUPPRESS)
    parser.set_defaults(func=run)
    args = parser.parse_args()

    if args.validate_only is None:
        if args.token is None:
            args.token = input('Enter access token: ')
            helpers.TokenAction.validate(parser, args.token, args)

        if args.repo is None:
            args.repo = input('Enter repository type [azure, github]: ')
            helpers.RepoAction.validate(parser, args.repo, args)

        if args.project is None:
            args.project = input('Enter project name: ')
            helpers.ProjectAction.validate(parser, args.project, args)

        if args.backlog is None:
            args.backlog = input('Choose backlog type to create (see docs): ')
            helpers.BacklogAction.validate(parser, args.backlog, args)

    args.func(args)


if __name__ == "__main__":
    main()
