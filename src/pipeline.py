import numpy as np
import pandas as pd
import traceback
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
    for endpoint in endpoints:
        resource = utils.identify_primary_resource(api_endpoint=endpoint)
        print(
            f"\nProcessing endpoint: '{endpoint}'",
            f"\nResource: '{resource}'"
        )
        if resource in settings.VALID_API_RESOURCES:
            try:
                if resource == 'competitions':
                    dataframe_results = get_competition_matches_data(api_endpoint=endpoint)
                elif resource == 'teams':
                    dataframe_results = get_team_data(api_endpoint=endpoint)
                elif resource == 'players':
                    dataframe_results = get_player_matches_data(api_endpoint=endpoint)
                elif resource == 'scorers':
                    dataframe_results = get_competition_scorers_data(api_endpoint=endpoint)
                filename_results = utils.get_filename_from_endpoint(api_endpoint=endpoint)
                dataframe_results.to_csv(f"../{settings.GLOBAL_RESULTS_FOLDERNAME}/{filename_results}.csv", index=False)
                num_files_wrangled += 1
                print(f"Transformed and saved '{endpoint}' data to CSV")
            except Exception as e:
                print(f"Failed to transform '{endpoint}' data. ErrorMsg: {e}")
                if settings.PRINT_ERROR_TRACEBACK:
                    print(f"ErrorTraceback: {traceback.print_exc()}\n\n\n\n")
        else:
            print(f"Error ---> '{endpoint}' has an invalid resource: '{resource}'")
    print(f"\nSuccessfully wrangled data into {num_files_wrangled} CSV files")
    return None