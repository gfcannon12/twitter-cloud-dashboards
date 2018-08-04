# Twitter Cloud Dashboards

## Accounts Needed
- Twitter Developer Premium (Free) https://developer.twitter.com/
- IBM Cloud Lite (Free) https://console.ng.bluemix.net/dashboard/apps/
  - Watson Studio https://dataplatform.cloud.ibm.com/
  - IBM Cloud Functions https://console.bluemix.net/openwhisk/
  - Db2 on Cloud https://console.bluemix.net/catalog/services/db2

## Process
#### Python 3.6 Script
1. Pull data from Twitter API
2. Store data in database (Db2)

#### IBM Cloud Functions
1. Schedule the script to run every minute for new data

#### Watson Studio
1. Display the data in various chart forms
2. Schedule the dashboard to refresh every few seconds