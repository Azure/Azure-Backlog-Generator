import pytest
import argparse
from argparse import Namespace
import contextlib
import io
import sys
import azbacklog.helpers as helpers


@contextlib.contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def test_TokenAction():
    parser = argparse.ArgumentParser()
    with captured_output() as (out, err):
        try:
            helpers.TokenAction.validate(parser, None, None)
        except SystemExit:
            err.seek(0)
            assert "User access token is required" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.TokenAction.validate(parser, '     ', None)
        except SystemExit:
            err.seek(0)
            assert "User access token is required" in str(err.read())

    assert helpers.TokenAction.validate(parser, 'test', None) is True


def test_RepoAction():
    parser = argparse.ArgumentParser()
    with captured_output() as (out, err):
        try:
            helpers.RepoAction.validate(parser, 'test', None)
        except SystemExit:
            err.seek(0)
            assert "Repository type must be either 'azure' or 'github'" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.RepoAction.validate(parser, '     ', None)
        except SystemExit:
            err.seek(0)
            assert "Repository type must be either 'azure' or 'github'" in str(err.read())

    assert helpers.RepoAction.validate(parser, 'azure', None) is True
    assert helpers.RepoAction.validate(parser, 'github', None) is True


def test_ProjectAction():
    parser = argparse.ArgumentParser()
    with captured_output() as (out, err):
        try:
            helpers.ProjectAction.validate(parser, None, None)
        except SystemExit:
            err.seek(0)
            assert "Project name is required" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.ProjectAction.validate(parser, '     ', None)
        except SystemExit:
            err.seek(0)
            assert "Project name is required" in str(err.read())

    assert helpers.ProjectAction.validate(parser, 'test', None) is True


def test_OrgAction():
    parser = argparse.ArgumentParser()
    azure_args = Namespace(repo='azure', project='testProject', backlog='correct', token='testToken')
    with captured_output() as (out, err):
        try:
            helpers.OrgAction.validate(parser, None, azure_args)
        except SystemExit:
            err.seek(0)
            assert "Organization name is required" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.OrgAction.validate(parser, '     ', azure_args)
        except SystemExit:
            err.seek(0)
            assert "Organization name is required" in str(err.read())

    github_args = Namespace(repo='github', project='testProject', backlog='correct', token='testToken')
    assert helpers.OrgAction.validate(parser, None, github_args) is True
    assert helpers.OrgAction.validate(parser, '     ', github_args) is True
    assert helpers.OrgAction.validate(parser, 'test', github_args) is True


def test_BacklogAction():
    parser = argparse.ArgumentParser()
    with captured_output() as (out, err):
        try:
            helpers.BacklogAction.validate(parser, 'test', None)
        except SystemExit:
            err.seek(0)
            assert "Backlog must be a valid option" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.BacklogAction.validate(parser, '     ', None)
        except SystemExit:
            err.seek(0)
            assert "Backlog must be a valid option" in str(err.read())

    assert helpers.BacklogAction.validate(parser, 'caf', None) is True
    assert helpers.BacklogAction.validate(parser, 'tfs', None) is True
