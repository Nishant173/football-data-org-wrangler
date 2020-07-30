# football-data-org-wrangler
Data wrangler that wrangles data obtained via API calls to https://www.football-data.org/

## Metadata
- Link to [football-data.org documentation](https://www.football-data.org/documentation/quickstart)
- Here are certain relevant competition codes
```
competition_codes = {
    'ChampionsLeague': 'CL',
    'DutchLeague': 'DED',
    'EnglishLeague': 'PL',
    'EnglishLeagueTwo': 'ELC',
    'FrenchLeague': 'FL1',
    'GermanLeague': 'BL1',
    'PortugueseLeague': 'PD',
    'SpanishLeague': 'SA',
    'WorldCup': 'WC',
}
```
- API [Resources available](https://www.football-data.org/docs/v1/index.html#_resources)
`['competitions', 'matches', 'players', 'scorers', 'teams']`
- Information about [API usage](https://www.football-data.org/documentation/quickstart)
- Information about [filtering data](www.football-data.org/documentation/quickstart#filtering)

## Usage
- Create an account on [football-data.org](https://www.football-data.org/) and get [your unique API token](https://www.football-data.org/client/home).
- Open `credentials.py` and add your unique API token in between the quotes. `API_TOKEN = 'enter-your-api-token-here'`
- Open `api_endpoints.py` and alter the list of API endpoints you'd like to get data from (check docs for details about structuring the API endpoint call).
- cd into /src and run `python run.py`
- Results will be generated in the root directory.

## Limitations
- Limited API resources are available, unless you have a premium account.

## Known issues
- Dynamic naming of CSV files of results **might** need a fix. Not tested thoroughly.