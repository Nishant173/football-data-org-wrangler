import pandas as pd

def get_key_from_dictionary(obj, key):
    if not isinstance(obj, dict):
        return obj
    return obj.get(key)


def get_refereeing_team(data):
    """
    [Helper function]
    Takes in dictionary of data about the referees involved per match, and returns string of
    the entire refereeing team.
    """
    referee_team = ""
    for data_obj in data:
        if data_obj['name']:            
            referee_team += str(data_obj['name'])
            referee_team += ', '
    num_chars = len(referee_team)
    return referee_team[:num_chars-2]


def get_scoreline(data):
    """
    [Helper function]
    Takes in dictionary of data about the scoreline for particular match, and returns the
    scoreline (str)
    NOTE: The scoreline might include penalty scoreline in brackets
    NOTE: Format of scoreline returned is `HomeGoals-AwayGoals (HomePens-AwayPens pens)`
    Eg 1) '2-1' (indicating home team wins 2-1)
    Eg 2) '3-5' (indicating home team loses 3-5)
    Eg 3) '4-4' (indicating 4-4 draw)
    Eg 4) '1-1 (4-5 pens)' (indicating that the game was drawn 1-1, and the home team lost 4-5 on penalties)
    """
    score_pens = data['penalties']
    score_ft = data['fullTime']
    home_goals = score_ft['homeTeam']
    away_goals = score_ft['awayTeam']
    if type(score_pens['homeTeam']) is int:
        home_pens = score_pens['homeTeam']
        away_pens = score_pens['awayTeam']
        return f"{home_goals}-{away_goals} ({home_pens}-{away_pens} pens)"
    return f"{home_goals}-{away_goals}"


def get_goals_scored_from_scoreline(scoreline, by):
    """
    [Helper function]
    Takes in scoreline (str) and returns goals scored by either the 'home' or 'away' team.
    Parameters:
        - scoreline (str): String of scoreline
        - by (str): Options: ['home', 'away']
    """
    if type(scoreline) is str:
        scoreline = scoreline.replace(' ', '')[:3]
        if '-' not in scoreline:
            return None
        home_goals, away_goals = scoreline.split('-')
        if by == 'home':
            return int(home_goals)
        elif by == 'away':
            return int(away_goals)
    return None


def drop_columns(data, columns_to_drop):
    """
    [Helper function]
    Takes in DataFrame and list of columns to drop, and returns DataFrame with the mentioned
    columns dropped (if they exist in the given DataFrame)
    """
    columns_in_dframe = data.columns.tolist()
    for column in columns_to_drop:
        if column in columns_in_dframe:
            data.drop(labels=column, axis=1, inplace=True)
    return data


def clean_scorelines(data):
    """
    Definition:
        Adds 'homeGoals' and 'awayGoals' columns generated from the scoreline present in raw data.
    """
    data['homeGoals'] = data['score'].apply(get_goals_scored_from_scoreline, by='home')
    data['awayGoals'] = data['score'].apply(get_goals_scored_from_scoreline, by='away')
    return data


def transform_team_data(dict_response):
    """
    Takes in dictionary of response from API call, and returns Pandas DataFrame of transformed data.
    Parameters:
        - dict_response (dict): Dictionary object of response from API (containing 'teams' data)
    """
    dframe = pd.DataFrame(data=dict_response['squad'])
    dframe['team'] = dict_response['name']
    return dframe


def transform_scorer_data(dict_response):
    """
    Takes in dictionary of response from API call, and returns Pandas DataFrame of transformed data.
    Parameters:
        - dict_response (dict): Dictionary object of response from API (containing 'scorers' data)
    """
    dframe_scorers = pd.DataFrame(data=dict_response['scorers'])
    dframe_scorers['playerId'] = dframe_scorers['player'].apply(get_key_from_dictionary, key='id')
    dframe_scorers['playerName'] = dframe_scorers['player'].apply(get_key_from_dictionary, key='name')
    dframe_scorers['playerDob'] = dframe_scorers['player'].apply(get_key_from_dictionary, key='dateOfBirth')
    dframe_scorers['playerNationality'] = dframe_scorers['player'].apply(get_key_from_dictionary, key='nationality')
    dframe_scorers['playerPosition'] = dframe_scorers['player'].apply(get_key_from_dictionary, key='position')

    dframe_scorers['teamId'] = dframe_scorers['team'].apply(get_key_from_dictionary, key='id')
    dframe_scorers['teamName'] = dframe_scorers['team'].apply(get_key_from_dictionary, key='name')

    dframe_scorers['playerDob'] = pd.to_datetime(arg=dframe_scorers['playerDob'])
    dframe_scorers.drop(labels=['player', 'team'], axis=1, inplace=True)
    return dframe_scorers


def transform_data(dict_response, resource):
    """
    Takes in dictionary of response from API call, and returns Pandas DataFrame of transformed data.
    Parameters:
        - dict_response (dict): Dictionary object of response from API
        - resource (str): Name of primary resource.
          Options: ['competitions', 'matches', 'players']
    """
    dict_resource_trimmer = {
        'competitions': 'competition',
        'matches': 'match',
        'players': 'player',
    }
    resource_trimmed = dict_resource_trimmer[resource]
    dframe = pd.DataFrame(data=dict_response['matches'])
    dframe[resource_trimmed] = dict_response[resource_trimmed]['name']
    # Get 'key' from dictionary data object
    columns_to_get_name_from = [resource_trimmed, 'homeTeam', 'awayTeam']
    columns_in_dataframe = dframe.columns.tolist()
    for column in columns_to_get_name_from:
        if column in columns_in_dataframe:
            dframe[column] = dframe[column].apply(get_key_from_dictionary, key='name')
    # Add scoreline, referee, date info
    dframe['score'] = dframe['score'].apply(get_scoreline)
    dframe = clean_scorelines(data=dframe)
    dframe['referees'] = dframe['referees'].apply(get_refereeing_team)
    dframe['utcDate'] = pd.to_datetime(arg=dframe['utcDate'])
    dframe = dframe.sort_values(by='utcDate', ascending=True).reset_index(drop=True)
    # Drop/re-order columns
    dframe = drop_columns(data=dframe, columns_to_drop=['lastUpdated', 'season', 'odds'])
    column_order = [
        'id', 'utcDate', resource_trimmed, 'matchday', 'homeTeam', 'homeGoals', 'awayGoals', 'awayTeam',
        'score', 'group', 'stage', 'referees', 'status'
    ]
    columns_in_dataframe = dframe.columns.tolist()
    for column in column_order:
        if column not in columns_in_dataframe:
            column_order.remove(column)
    dframe = dframe.loc[:, column_order]    
    return dframe