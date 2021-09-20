import pytest
import requests
from src.GitHubApi import get_commits


@pytest.fixture()
def valid_git_repo():
    return "willhuang93/juniper"


@pytest.fixture()
def invalid_git_repo():
    return "asdf"


def test_number_of_commits_happy_path_1(valid_git_repo):
    n = 1
    result = get_commits(valid_git_repo, n)
    assert len(result.json()) == 1


def test_number_of_commits_happy_path_20(valid_git_repo):
    """
    I chose >= because the repo fixture may or may not have more than 1 commit
    """
    n = 1
    result = get_commits(valid_git_repo, n)
    assert len(result.json()) >= 1


def test_number_of_commits_negative_num_(valid_git_repo):
    n = -1
    result = get_commits(valid_git_repo, n)
    assert result.status_code == 200


def test_invalid_git_repo(invalid_git_repo):
    with pytest.raises(requests.HTTPError):
        get_commits(invalid_git_repo)


def test_invalid_git_repo_with_commit_number(invalid_git_repo):
    with pytest.raises(requests.HTTPError):
        n = 5
        get_commits(invalid_git_repo, n)
