import http.client
import json
import credentials

def get_raw_data(api_endpoint):
    """
    Definition:
        Takes in an API endpoint (str) obtained via 'football-data.org', and returns Python
        data object (list/dictionary) containing football-related data.
    Parameters:
        - api_endpoint (str): API endpoint
    Returns:
        Python data object (list/dictionary) containing football-related data.
    Usage:
        get_raw_data(api_endpoint="/v2/competitions/CL/matches?status=SCHEDULED")
    """
    headers = {'X-Auth-Token': credentials.API_TOKEN}
    connection = http.client.HTTPConnection(host='api.football-data.org')
    connection.request(method='GET',
                       url=api_endpoint,
                       body=None,
                       headers=headers)
    response_obj = json.loads(connection.getresponse().read().decode())
    return response_obj