import os
import string
import time
import warnings
import numpy as np
import settings

def truncate_after_special_char(endpoint_component):
    special_chars = list(string.punctuation)
    endpoint_component = str(endpoint_component).strip()
    endpoint_component_truncated = ""
    for char in endpoint_component:
        if char not in special_chars:
            endpoint_component_truncated += char
        else:
            break
    return endpoint_component_truncated


def get_filename_from_endpoint(api_endpoint):
    endpoint_components = api_endpoint.split('/')
    endpoint_components = list(filter(None, endpoint_components))
    endpoint_components.remove('v2')
    cleaned_endpoint_components = []
    for endpoint_component in endpoint_components:
        truncated = truncate_after_special_char(endpoint_component=endpoint_component)
        cleaned_endpoint_components.append(truncated)
    filename_for_results = "_".join(cleaned_endpoint_components)
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
    time_taken_in_secs = round((end - start), 2)
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