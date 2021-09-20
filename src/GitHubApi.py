import requests

GITHUB_API = 'https://api.github.com/'


def get_commits(repo_identifier: str, num_of_commits: int):
    """

    :param repo_identifier:
    :param num_of_commits:
    :return:
    """
    try:
        url = GITHUB_API + F'repos/{repo_identifier}/commits'
        params = {'per_page': num_of_commits}

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)




