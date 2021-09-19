import click
import json
import yaml
from GitHubApi import get_commits

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cmd():
    """Juniper CLI Tool for github commits and SQLite DB datastore and query
    """
    pass


@cmd.command(name='commits')
@click.argument('repo_identifier')
@click.option('-n', '--number', default=5, type=click.IntRange(1, 20, clamp=True))
@click.option('-f', '--format', default="YAML", type=click.Choice(['YAML', 'JSON'], case_sensitive=False))
def commit(repo_identifier, number, format):
    """Query a GitHub REST API for commit history on a git repo, process API results and, finally, print the filtered
    down result in YAML, or JSON, format
    """
    print("commit", repo_identifier, number, format)
    subset_commits = []
    response = get_commits(repo_identifier=repo_identifier, num_of_commits=number)

    for git_commit in response.json():
        commit_data = {
            'date': git_commit['commit']['author']['date'],
            'email': git_commit['commit']['author']['email'],
            'message': git_commit['commit']['message'],
            'sha': git_commit['sha'],
        }

        subset_commits.append(commit_data)

    if format == 'JSON':
        print(json.dumps(subset_commits, indent=4))
    elif format == 'YAML':
        print(yaml.dump(subset_commits))


@cmd.group(name='datastore')
def datastore():
    """Create SQLite DB, populate it with the provided JSON data, perform SQL queries on the DB
    """
    pass


@datastore.command(name='import')
@click.option('-f', '--file', required=True)
def datastore_import(file):
    """Create SQLite DB, populate it with the provided JSON data
    """
    print("datastore import", file)


@datastore.command(name='query')
@click.option('-d', '--date', required=True)
def datastore_query(date):
    """Perform SQL queries on the DB
    """
    print("datastore query", date)


if __name__ == '__main__':
    cmd()
