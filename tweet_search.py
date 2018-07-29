import os
import requests
import json
import numpy as np

def get_token():
    url = "https://api.twitter.com/oauth2/token"
    body = {"grant_type": "client_credentials"}
    headers = {
        'Authorization': f'Basic {os.environ["auth"]}',
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
    }
    response = requests.request("POST", url, data=body, headers=headers)
    response_dict = json.loads(response.text)
    token = response_dict['access_token']
    return token

def search_query(query, token, the_next=None):
    url = "https://api.twitter.com/1.1/tweets/search/30day/dev.json"
    body = {"query": f'{query}', "fromDate": "201807280514", "toDate": "201807280515"}

    # next is needed if you return >100 results
    if the_next != None:
        body['next'] = the_next

    body2  = json.dumps(body)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, data=body2, headers=headers)
    response_dict = json.loads(response.text)
    result = {}

    if 'results' in response_dict:
        response_count = len(response_dict['results'])
        result = {"response_count": response_count}
        if 'next' in response_dict:
            result['next'] = response_dict['the_next']
    else:
        print('No result in response_dict')
        print('ERROR', response_dict['error'])

    return result

# For >100 results, you can make an additional request to get more data
# Beware - you are rate-limited to 30 requests per min AND 250 per month
# You get an additional 50 for the fullarchive label

def get_count(player):
    count = np.array([])
    count_finished = False
    api_count = 0
    the_next = None
    
    while count_finished == False:
        api_count += 1
        if api_count ==3:
            return
    
        auth = get_token()
        search_result = search_query(player, auth, the_next)
        if 'response_count' not in search_result:
            return
        
        result_count = search_result['response_count']
        count = np.append(count, result_count)
        print(f'{result_count} in count #{len(count)} for {player}')

        if 'next' not in search_result:
            count_finished = True
        else:
            the_next = search_result['next']

    return count.sum()

data_count = get_count('jordan spieth')
print(f'Total count for data is {data_count}')