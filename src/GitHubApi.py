import requests

GITHUB_API = 'https://api.github.com/'


def get_commits(repo_identifier: str, num_of_commits: int = 5) -> requests.Response:
    """
    Gets the commits from a github repo using the github API.

    :param repo_identifier: github repo specification. Is a string in the format of "username/repo_name"
    :param num_of_commits: number of commits to retrieve from github, defaults to 5 if not provided
    :return: requests.Response, returns the HTTP Response that contains the git commits
    """
    try:
        url = GITHUB_API + F'repos/{repo_identifier}/commits'
        params = {'per_page': num_of_commits}

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
        raise
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        raise
    except requests.exceptions.Timeout as errt:
        print(errt)
        raise
    except requests.exceptions.RequestException as err:
        print(err)
        raise



