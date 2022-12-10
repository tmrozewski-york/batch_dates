# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 21:08:13 2022

@author: Tomasz Mrozewski
"""

# import required libraries
import os # need this to run outside of jupyter
import pandas as pd # used to manage CSV files instead of CSV library
import requests # API calls
import json # handle the output

# set the working directory
my_dir = 'C:\\Users\\tomas\\OneDrive\\Documents\\CSCH dates' # wd set here
os.chdir(my_dir)

# open the CSV files with credentials and endpoints
my_keys = pd.read_csv("CSCH_creds.csv")

# assign values using cell index location in CSV
key = my_keys.iat[0,0] # API token
issueList_endpoint = my_keys.iat[0,1] # get list of all issues
issue_endpoint = my_keys.iat[0,2] # get issue by ID
unpub_endpoint = my_keys.iat[0,3] # unpub by sub & pub ID
edit_endpoint = my_keys.iat[0,4] # edit by sub & pub ID
pub_endpoint = my_keys.iat[0,5] # repub by sub & pub ID

# get list of all issues
# set 'count' to get all published issues (default 20)
issueList_call = requests.get(
issueList_endpoint,
params={'apiToken':key,'isPublished':'true','count':'100'}
)
# assign the json output of the call to variable z
y = json.dumps(issueList_call.json())
z = json.loads(y)

# loops through the issue ids to do calls for each issue's contents
for item in z['items']:
    # convert id from integer to string
    q = str(item['id'])
    # replace the placeholder in endpoint url with id string
    ep = issue_endpoint.replace("{issueId}",q)
    # call for the full issue contents
    issue_call = requests.get(ep,params={'apiToken':key})
    # assign the json output of the call to variable a, load it as b
    a = json.dumps(issue_call.json())
    b = json.loads(a)
    # assign the date (in YYYY-MM-DD HH:MM:SS format) to variable c as string
    c = b["datePublished"]
    # substring to YYYY-MM-DD. The date we want to enter is stored as d
    d = c[0:10]
    # loops through each article in the issue, assigning sub and pub IDs
    for article in b["articles"]:
        e = str(article['id'])
        f = str(article['currentPublicationId'])   
        
        '''
        # This is the part that hasn't worked properly
        # Now we run the calls to unpublish, edit, and republish the articles
        
        # UNPUBLISH
        # replace placeholders in the endpoint, in two moves
        g = unpub_endpoint.replace("{submissionId}",e)
        h = g.replace("{publicationId}",f)
        # now make the call to upublish
        requests.put(h,params={'apiToken':key})
        
        # EDIT
        # reusing variables from previous call because I'm lazy
        g = edit_endpoint.replace("{submissionId}",e)
        h = g.replace("{publicationId}",f)
        # now, make the edit to change datePublished to d
        requests.put(h,params={'apiToken':key,'datePublished':d})
        
        # REPUBLISH
        # reusing variables from previous call because I'm lazy
        g = edit_endpoint.replace("{submissionId}",e)
        h = g.replace("{publicationId}",f)
        '''