## Description
This program collects the publicly available list of ranked games on the website boardgamegeek.com and data about each game available through the [BoardGameGeek public API](https://boardgamegeek.com/wiki/page/XML_API_Terms_of_Use#). The collected information is written to a `csv` file and archived locally before being copied to a PostgreSQL database table.

The following information is collected about every game:

| **column** | **description** |
| --- | -- |
| rank | *proprietary BoardGameGeek ranking* |
| name | *name of board game* |
| publisher | *most recent publisher as listed on the API* |
| year_pub | *most recent year published* |
| game_type | *board game type* |
| rating | *board game rating* |
| weight | *board game difficulty* |
| min_players | *minimum recommended players* |
| max_players | *maximum recommended players* |
| best_players | *best amount of players per community poll* |
| play_time | *publisher estimated play time* |
| min_age | *minimum recommended age* |
| game_pg_url | *url to BoardGameGeek game information page* |
| game_img | *url to box art image* |

Windows Task Scheduler is utilized with a batch script that runs the program once a week in order to make sure the database information is up to date.


## Modules
[main.py](main.py): Iterates through the list of ranked board games on BoardGameGeek.com, collects and saves data about each game to a csv file, copies final csv file to a PostgreSQL database. 

[data_handler.py](data_handler.py): Contains functions that locate and return game ids on a BGG page, request from the BGG public API specific information about each game id, write returned data to a new csv file.

[gamepage_parser.py](gamepage_parser.py): Contains functions that search the parsed API page data for specific information about a game and return it.

[db_connector.py](db_connector.py): Contains functions that connect to a PostgreSQL database and copy the data from a csv file to a predefined table in the database.

![img](https://cf.geekdo-images.com/HZy35cmzmmyV9BarSuk6ug__thumb/img/gbE7sulIurZE_Tx8EQJXnZSKI6w=/fit-in/200x150/filters:strip_icc()/pic7779581.png)