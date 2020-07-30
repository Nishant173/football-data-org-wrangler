import os
import re
import string
import time
import warnings
import numpy as np
import settings

def identify_primary_resource(api_endpoint):
    if 'scorers' in api_endpoint:
        primary_resource = 'scorers'
    else:
        endpoint_components = api_endpoint.split('/')
        endpoint_components = list(filter(None, endpoint_components))
        endpoint_components.remove('v2')
        primary_resource = endpoint_components[0]
    return primary_resource


def get_competition_code(api_endpoint):
    endpoint_components = api_endpoint.split('/')
    endpoint_components = list(filter(None, endpoint_components))
    endpoint_components.remove('v2')
    if endpoint_components[0] in ['competitions']:
        competition_code = endpoint_components[1]
        return competition_code
    return ''


def get_team_or_player_id(api_endpoint):
    endpoint_components = api_endpoint.split('/')
    endpoint_components = list(filter(None, endpoint_components))
    endpoint_components.remove('v2')
    if endpoint_components[0] in ['players', 'teams']:
        id_required = endpoint_components[1]
        return id_required
    return ''


def remove_special_chars(string):
    return ''.join(char for char in string if char.isalnum())


def get_querystring_parameters(api_endpoint):
    """ Gets list of querystring parameters from the API endpoint """
    qs_parameters = []
    api_endpoint = api_endpoint.lower().strip()
    qs_search_index = re.search(pattern=r'\?', string=api_endpoint)
    if qs_search_index:
        qs = api_endpoint[qs_search_index.span()[1]:]
        if '&' in qs:
            qs_components = qs.split('&')
            for qs_component in qs_components:
                qs_parameters.append(remove_special_chars(string=qs_component))
        else:
            qs_parameters.append(remove_special_chars(string=qs))
    return qs_parameters


def get_filename_from_endpoint(api_endpoint):
    api_endpoint = api_endpoint.lower().strip()
    resources_found = []
    for resource in settings.VALID_API_RESOURCES:
        resource = resource.lower().strip()
        resource_exists = re.search(pattern=resource, string=api_endpoint)
        if resource_exists:
            resources_found.append(resource)
    
    if 'competitions' in resources_found:
        additional_identifier = get_competition_code(api_endpoint=api_endpoint)
    elif 'teams' in resources_found:
        additional_identifier = get_team_or_player_id(api_endpoint=api_endpoint)
    elif 'players' in resources_found:
        additional_identifier = get_team_or_player_id(api_endpoint=api_endpoint)
    
    qs_params = get_querystring_parameters(api_endpoint=api_endpoint)
    
    api_endpoint_keywords = resources_found + [additional_identifier] + qs_params
    filename_for_results = "_".join(api_endpoint_keywords)
    return filename_for_results


def run_and_timeit(func):
    """
    Takes in function-name; then runs it, times it, and prints out the time taken.
    Parameters:
        - func (object): Object of the function you want to execute.
    """
    start = time.time()
    warnings.filterwarnings(action='ignore')
    func()
    end = time.time()
    time_taken_in_secs = int(round((end - start), 2))
    if time_taken_in_secs < 60:
        secs = time_taken_in_secs
        time_taken = f"{secs}s"
    elif 60 < time_taken_in_secs < 3600: # 1 - 59.99 mins
        mins = int(np.floor(time_taken_in_secs / 60))
        secs = time_taken_in_secs % 60
        time_taken = f"{mins}m {secs}s"
    elif 3600 < time_taken_in_secs < 86400: # 1 - 23.99 hrs
        hrs = int(np.floor(time_taken_in_secs / 3600))
        mins = int(np.floor((time_taken_in_secs - 3600*hrs) / 60))
        secs = time_taken_in_secs % 60
        time_taken = f"{hrs}h {mins}m {secs}s"
    else:
        time_taken = "Longer than a day!"
    print(f"\nDone! Time taken: {time_taken}")
    return None


def create_global_results_folder():    
    try:
        os.mkdir('../{}'.format(settings.GLOBAL_RESULTS_FOLDERNAME))
    except FileExistsError:
        pass
    return None