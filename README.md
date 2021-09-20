# juniper
To create the command-line tool, navigate to the root directory level (under /juniper/)
and use `pip install .`. This will create the `jnpr` console command.

Example usage includes but not are restricted to:
```
jnpr --help
jnpr commits -n 5 -f JSON willhuang93/juniper
jnpr datastore import -f src/db_records.json
jnpr datastore query -d 2021-02-09
```

