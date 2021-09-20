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

This tool has 3 components.
  1) CLI component, which parses user input and responds appropriately
  2) Github API component, which interacts with the Github API and retrieves the specified number of commits from the 
  target repository.
  3) SQLite database component, which manages the tables as detailed, capability of importing data through JSON files,
  and the capability of querying data based on the `ordered_on` attribute of the `orders` table.
  
 Since these components are logically separate from one another, I decided to structure the project in a similar way, 
 each file containing the code of each component.
 
 In regards to the Github API and SQLite database components, if the tool's functionalities regarding these technologies
 need to be extended, those parts of the code can be refactored into an OOP design. For example, if the tool needs to be
 able to manage git projects, or search repository topics, or bugs, I think it would be best to centralize the functions
 into an interface with corresponding methods to interact with github in the necessary manner.
 
 It's not critically necessary as the code can function fine procedurally but it would be easier to maintain and extend
 functionalities if the tool grows.
 
 This project also contains some basic unit tests that can be run with `pytest` under the `tests` directory. 