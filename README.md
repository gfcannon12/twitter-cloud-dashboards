# Twitter Cloud Dashboards

Demo created by Gray Cannon to share with the Data Science Study Group of South Florida  
https://www.meetup.com/Data-Science-Study-Group-South-Florida/events/253495098/

## Accounts Needed
#### Demo created using only free plans
- Twitter API https://developer.twitter.com/
- IBM Cloud https://console.bluemix.net/catalog/
  - Watson Studio https://dataplatform.cloud.ibm.com/
  - IBM Cloud Functions https://console.bluemix.net/openwhisk/
  - Db2 on Cloud https://console.bluemix.net/catalog/services/db2

#### Notes about Twitter API
This demo uses the free package of the "Premium" API.  You can see your usage versus your monthly cap here  
https://developer.twitter.com/en/dashboard

The paid package for the Twitter API includes a counts endpoint.  This is more convenient way to count tweets than the method used in this demo  
https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search#CountsEndpoint

## Process
#### Python 3.6 Script
1. Pull data from Twitter API
2. Store data in database (Db2)

#### IBM Cloud Functions
1. Schedule the script to run every minute for new data

#### Watson Studio
1. Display the data in various chart forms
2. Schedule the dashboard to refresh every few seconds