import os
import requests
import json
import numpy as np
import random
import ibm_db

# Populated by trigger parameters
query_terms = ['tiger woods', 'jordan spieth', 'rory mcilroy', 'francesco molinari'] # List of strings
date = '20170722' # String yyyymmdd
end_time = '1710' # String hhmm 24 hr clock
interval = '10' # String minutes
dbName = os.environ['dbName']
dbHost = os.environ['dbHost']
dbPort = os.environ['dbPort']
dbUser = os.environ['dbUser']
dbPass = os.environ['dbPass']

# Time Calculations
start_time = str(int(end_time) - int(interval))
end_period = date + end_time
start_period = date + start_time

hour = end_time[:2]
minute = end_time[2:]

if int(hour) < 12:
    time_text = 'AM'
elif int(hour) == 12:
    time_text = 'PM'
else:
    time_text = 'PM'
    hour = str(int(hour) - 12)

datetime_int = int(end_period)
time_string = hour + ':' + minute + ' ' + time_text

def get_token():
    url = "https://api.twitter.com/oauth2/token"
    body = {"grant_type": "client_credentials"}
    headers = {
        'Authorization': f'Basic {os.environ["auth2"]}',
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
    }
    response = requests.request("POST", url, data=body, headers=headers)
    response_dict = json.loads(response.text)
    token = response_dict['access_token']
    return token

def search_query(query, token, the_next=None):
    url = "https://api.twitter.com/1.1/tweets/search/30day/dev.json"
    body = {"query": query, "fromDate": start_period, "toDate": end_period}

    # next is needed if you return >100 results
    if the_next != None:
        body['next'] = the_next

    body2 = json.dumps(body)
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
            result['the_next'] = response_dict['next']
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
    '''
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

        if 'the_next' not in search_result:
            count_finished = True
        else:
            the_next = search_result['the_next']

    return count.sum()
    '''
    return random.randint(0, 200)

db2_connect_info = f"DATABASE={dbName};HOSTNAME={dbHost};PORT={dbPort};PROTOCOL=TCPIP;UID={dbUser};PWD={dbPass};"
conn = ibm_db.connect(db2_connect_info, "", "")

x = ibm_db.exec_immediate(conn, 'select * from tweet_counts')
result = ibm_db.fetch_assoc(x)
print(result)

for query_term in query_terms:
    data_count = int(get_count(query_term))
    print(f'Total count for {query_term} is {data_count}')
