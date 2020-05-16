import pytest
import argparse
import contextlib
import io
import sys
import src.azbacklog.helpers as helpers

@contextlib.contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

def test_tokenAction():
    parser = argparse.ArgumentParser()
    with captured_output() as (out, err):
        try:
            helpers.TokenAction.validate(parser, None, None)
        except SystemExit as e:
            err.seek(0)
            assert "User access token is required" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.TokenAction.validate(parser, '     ', None)
        except SystemExit as e:
            err.seek(0)
            assert "User access token is required" in str(err.read())

    assert helpers.TokenAction.validate(parser, 'test', None) == True
            
def test_repoAction():
    parser = argparse.ArgumentParser()
    with captured_output() as (out, err):
        try:
            helpers.RepoAction.validate(parser, 'test', None)
        except SystemExit as e:
            err.seek(0)
            assert "Repository type must be either 'azure' or 'github'" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.RepoAction.validate(parser, '     ', None)
        except SystemExit as e:
            err.seek(0)
            assert "Repository type must be either 'azure' or 'github'" in str(err.read())

    assert helpers.RepoAction.validate(parser, 'azure', None) == True            
    assert helpers.RepoAction.validate(parser, 'github', None) == True            

def test_projectAction():
    parser = argparse.ArgumentParser()
    with captured_output() as (out, err):
        try:
            helpers.ProjectAction.validate(parser, None, None)
        except SystemExit as e:
            err.seek(0)
            assert "Project name is required" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.ProjectAction.validate(parser, '     ', None)
        except SystemExit as e:
            err.seek(0)
            assert "Project name is required" in str(err.read())

    assert helpers.ProjectAction.validate(parser, 'test', None) == True
            
def test_backlogAction():
    parser = argparse.ArgumentParser()
    with captured_output() as (out, err):
        try:
            helpers.BacklogAction.validate(parser, 'test', None)
        except SystemExit as e:
            err.seek(0)
            assert "Backlog must be a valid option" in str(err.read())

    with captured_output() as (out, err):
        try:
            helpers.BacklogAction.validate(parser, '     ', None)
        except SystemExit as e:
            err.seek(0)
            assert "Backlog must be a valid option" in str(err.read())

    assert helpers.BacklogAction.validate(parser, 'caf', None) == True            
    assert helpers.BacklogAction.validate(parser, 'tfs', None) == True            
