import click
import datetime
import json
import sqlite3
import sys
import yaml
from src.Database import initialize_tables, import_data, query_data
from src.GitHubApi import get_commits

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DB_FILE = r'juniper.db'


@click.group(context_settings=CONTEXT_SETTINGS)
def cmd() -> None:
    """Juniper CLI Tool for displaying github commits and SQLite DB datastore and query
    """
    pass


@cmd.command(name='commits')
@click.argument('repo_identifier')
@click.option('-n', '--number', default=5, type=click.IntRange(1, 20, clamp=True))
@click.option('-f', '--format', default="YAML", type=click.Choice(['YAML', 'JSON'], case_sensitive=False))
def commit(repo_identifier, number, format) -> None:
    """Query a GitHub REST API for commit history on a git repo, process API results and, finally, print the filtered
    down result in YAML, or JSON format
    """
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
def datastore() -> None:
    """Create SQLite DB, populate it with the provided JSON data, perform SQL queries on the DB
    """
    pass


@datastore.command(name='import')
@click.option('-f', '--file', type=click.Path(exists=True), required=True)
def datastore_import(file) -> None:
    """Create SQLite DB (if it doesn't already exist), populate it with the provided JSON data
    """
    with sqlite3.connect(DB_FILE) as connection:

        initialize_tables(connection)

        with open(file, 'r') as f:
            data = json.load(f)
            import_data(data, connection)


@datastore.command(name='query')
@click.option('-d', '--date', required=True, type=click.DateTime(formats=["%Y-%m-%d"]))
def datastore_query(date) -> None:
    """Perform SQL queries on the DB
    """
    with sqlite3.connect(DB_FILE) as connection:
        on_or_before_data, after_data = query_data(date, connection)

        for item_count, first_name, last_name, ordered_on in on_or_before_data:
            print(f'{first_name} {last_name} ordered {item_count} item(s) ' 
                  f'before or on {datetime.datetime.strftime(date, "%Y-%m-%d")}')

        print()

        for item_count, first_name, last_name, ordered_on in after_data:
            print(f'{first_name} {last_name} ordered {item_count} item(s) ' 
                  f'after {datetime.datetime.strftime(date, "%Y-%m-%d")}')


if __name__ == '__main__':
    cmd()
