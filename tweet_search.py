#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import os
import requests
import json
import numpy as np
import random
import ibm_db
import datetime

def main(dict):

    def get_terms():
        terms = []
        for key in dict.keys():
            if "_term" in key:
                terms.append(dict[key])

        return terms
    
    def get_job_runs(terms):
        # Calculate how many jobs have run so far
        sql = ibm_db.exec_immediate(conn, 'select count(*) from tweet_counts')
        row_counts = int(ibm_db.fetch_assoc(sql)['1'])
        job_runs = row_counts / len(query_terms)
        return job_runs
    
    def get_token():
        url = "https://api.twitter.com/oauth2/token"
        body = {"grant_type": "client_credentials"}
        headers = {
            'Authorization': f'Basic {dict["auth2"]}',
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        response = requests.request("POST", url, data=body, headers=headers)
        response_dict = json.loads(response.text)
        token = response_dict['access_token']
        return token
    
    def search_twitter(query, token, the_next=None):
        url = "https://api.twitter.com/1.1/tweets/search/30day/dev.json"
        body = {"query": query, "fromDate": start_dt_str, "toDate": end_dt_str}
    
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
    
    def get_count(term):
        count = np.array([])
        count_finished = False
        the_next = None
        # api_count = 0
        
        while count_finished == False:
            '''
            # For limiting API use - also uncomment api_count above
            api_count += 1
            if api_count ==3:
                return '0'
            '''
            auth = get_token()
            search_result = search_twitter(term, auth, the_next)
            if 'response_count' not in search_result:
                return '0'
            
            result_count = search_result['response_count']
            count = np.append(count, result_count)
            print(f'{result_count} in count #{len(count)} for {term}')
    
            if 'the_next' not in search_result:
                count_finished = True
            else:
                the_next = search_result['the_next']
    
        return count.sum()
        #return random.randint(0, 200)
    
    # Connect to database
    db2_connect_info = f"DATABASE={dict['dbName']};HOSTNAME={dict['dbHost']};PORT={dict['dbPort']};PROTOCOL=TCPIP;UID={dict['dbUser']};PWD={dict['dbPass']};"
    conn = ibm_db.connect(db2_connect_info, "", "")
    
    query_terms = get_terms()
    job_runs = get_job_runs(query_terms)
    
    # Time Calculations
    dt_str = dict['date'] + dict['time']
    dt = datetime.datetime.strptime(dt_str, '%Y%m%d%H%M')
    time_since_job1 = datetime.timedelta(minutes=(int(dict['interval']) * job_runs))
    end_dt = dt + time_since_job1
    end_dt_str = datetime.datetime.strftime(end_dt, '%Y%m%d%H%M')
    interval_td = datetime.timedelta(minutes=int(dict['interval']))
    start_dt = end_dt - interval_td
    start_dt_str = datetime.datetime.strftime(start_dt, '%Y%m%d%H%M')

    datetime_int = int(end_dt_str)
    time_string = datetime.datetime.strftime(end_dt, '%I:%M %p')
    
    for query_term in query_terms:
        print(time_string)
        data_count = int(get_count(query_term))
        print(f'{data_count} in PERIOD COUNT for {query_term}')
        sql_query = f"insert into tweet_counts (time, end_time, player, tweets) values ('{time_string}', {datetime_int}, '{query_term}', {data_count})"
        ibm_db.exec_immediate(conn, sql_query)

    ibm_db.close(conn)
    return {'message': 'job has run'}

# To run this locally, you need to create a dict of all your params and pass that to the main function
# main(the_dict)