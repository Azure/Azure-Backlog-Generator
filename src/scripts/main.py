#!/usr/bin/env python3

import argparse
import azbacklog.helpers as helpers
import azbacklog.services as services

def run(args):
    #gh = GitHub()
    #gh.authenticate(token="2fcaf1dd14b3cdde106b43e859ef4b2b20ee682b")

    bl = helpers.Backlog()
    if (args.validate_only != None):
        bl.build(args.validate_only, True)
    else:
        bl.build('./workitems/caf')

def main():
    parser = argparse.ArgumentParser(prog='azbacklog', description="Generate a backlog of work items.", allow_abbrev=False)
    parser.add_argument('-t', '--token', required=True, help="GitHub or Azure DevOps token")
    parser.add_argument('-r', '--repo', choices=['azure', 'github'], help="targetted repository type")
    parser.add_argument('-p', '--project', help="project name to create")
    parser.add_argument('-o', '--org', help="Optional. If the target is a GitHub organization, specify the organization's name.")
    parser.add_argument('-b', '--backlog', choices=['caf', 'tfs'], help="type of backlog to create")
    parser.add_argument('--validate-only', help=argparse.SUPPRESS)
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
