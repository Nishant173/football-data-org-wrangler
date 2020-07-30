import numpy as np
import pandas as pd
import api_endpoints
import extract
import settings
import transform
import utils

def get_competition_matches_data(api_endpoint):
    dict_response = extract.get_raw_data(api_endpoint=api_endpoint)
    data_competition_matches = transform.transform_data(dict_response=dict_response,
                                                        resource='competitions')
    return data_competition_matches


def get_competition_scorers_data(api_endpoint):
    dict_response = extract.get_raw_data(api_endpoint=api_endpoint)
    data_competition_scorers = transform.transform_scorer_data(dict_response=dict_response)
    return data_competition_scorers


def get_player_matches_data(api_endpoint):
    dict_response = extract.get_raw_data(api_endpoint=api_endpoint)
    data_player_matches = transform.transform_data(dict_response=dict_response,
                                                   resource='players')
    return data_player_matches


def get_team_data(api_endpoint):
    dict_response = extract.get_raw_data(api_endpoint=api_endpoint)
    data_by_team = transform.transform_team_data(dict_response=dict_response)
    return data_by_team


def execute_pipeline():
    """
    Pipeline that extracts raw data and transforms it into human readable format.
    """
    utils.create_global_results_folder()
    endpoints = api_endpoints.API_ENDPOINTS
    num_files_wrangled = 0
    valid_resources = ['competitions', 'teams', 'players', 'scorers']
    for endpoint in endpoints:
        print(f"\nProcessing endpoint: '{endpoint}'")
        endpoint_components = endpoint.split('/')
        endpoint_components = list(filter(None, endpoint_components))
        endpoint_components.remove('v2')
        if 'scorers' in endpoint:
            resource = 'scorers'
        else:
            resource = endpoint_components[0]
        print(f"Resource: '{resource}'")
        if resource in valid_resources:
            if resource == 'competitions':
                dataframe_results = get_competition_matches_data(api_endpoint=endpoint)
            elif resource == 'teams':
                dataframe_results = get_team_data(api_endpoint=endpoint)
            elif resource == 'players':
                dataframe_results = get_player_matches_data(api_endpoint=endpoint)
            elif resource == 'scorers':
                dataframe_results = get_competition_scorers_data(api_endpoint=endpoint)
            try:
                filename_results = utils.get_filename_from_endpoint(api_endpoint=endpoint)
                dataframe_results.to_csv(f"../{settings.GLOBAL_RESULTS_FOLDERNAME}/{filename_results}.csv", index=False)
                num_files_wrangled += 1
                print(f"Transformed and saved '{endpoint}' data to CSV")
            except Exception as e:
                print(f"Failed to transform '{endpoint}' data. ErrorMsg: {e}")
        else:
            print(f"Error ---> '{endpoint}' has an invalid resource: '{resource}'")
    print(f"\nSuccessfully wrangled data into {num_files_wrangled} CSV files")
    return None