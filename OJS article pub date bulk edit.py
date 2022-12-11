# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 21:08:13 2022
@author: Tomasz Mrozewski tmrozews@yorku.ca
"""

# import required libraries
import os # need this to run outside of jupyter
import pandas as pd # used to manage CSV files instead of CSV library
import requests # API calls
import json # handle the output

# set the working directory
my_dir = ' ' # wd set here
os.chdir(my_dir)

# open the CSV files with credentials and endpoints
my_keys = pd.read_csv(" ") # filename here

# assign values using cell index location in CSV
key = my_keys.iat[0,0] # API token
issueList_endpoint = my_keys.iat[0,1] # get list of all issues
issue_endpoint = my_keys.iat[0,2] # get issue by ID
unpub_endpoint = my_keys.iat[0,3] # unpub by sub & pub ID
edit_endpoint = my_keys.iat[0,4] # edit by sub & pub ID
pub_endpoint = my_keys.iat[0,5] # repub by sub & pub ID

# get list of all issues
issueList_call = requests.get(issueList_endpoint,params={'apiToken':key,'isPublished':'true','count':'100'}) # set 'count' to get all published issues
# assign the json output of the call to variable y, load it as z
y = json.dumps(issueList_call.json())
z = json.loads(y)

# loops through the issue ids to do calls for each issue's contents
for item in z['items']:
    # convert  issue id from integer to string
    q = str(item['id'])
    # replace the placeholder in endpoint url with issue id string
    ep = issue_endpoint.replace("{issueId}",q)
    # call for the full metadata and contents of the issue
    issue_call = requests.get(ep,params={'apiToken':key})
    # assign the json output of the call to variable a, load it as b
    a = json.dumps(issue_call.json())
    b = json.loads(a)
    
    # assign the issue's publication date (in YYYY-MM-DD HH:MM:SS format) to variable c as string
    c = b["datePublished"]
    # substring publication date to get YYYY-MM-DD format. The date we want to enter is stored as d
    d = c[0:10]
    print(d) # printing this to monitor progress in the console
    
    # loops through each article in the issue, assigning sub and pub IDs to variables e and f
    for article in b["articles"]:
        e = str(article['id'])
        f = str(article['currentPublicationId'])  
        
        # unpublish the article
        g = unpub_endpoint.replace("{submissionId}",e) # replace sub ID placeholder in endpoint url with e
        h = g.replace("{publicationId}",f) # replace pub ID placeholder in endpoint url with f
        # now make the call to upublish
        i = requests.put(h,params={'apiToken':key})
        
        # edit the article
        g = edit_endpoint.replace("{submissionId}",e) # replace sub ID placeholder in endpoint url with e
        h = g.replace("{publicationId}",f) # replace pub ID placeholder in endpoint url with f
        # now, make the edit to change datePublished to d
        j = requests.put(h,params={'apiToken':key},data={'datePublished':d})
        
        # repubblish the article
        g = pub_endpoint.replace("{submissionId}",e) # replace sub ID placeholder in endpoint url with e
        h = g.replace("{publicationId}",f) # replace pub ID placeholder in endpoint url with f
        k = requests.put(h,params={'apiToken':key})
        
        print(e,f,i,j,k,sep=",") # print sub and pub ids with API response codes for logging
