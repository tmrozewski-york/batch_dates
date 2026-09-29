# -*- coding: utf-8 -*-
"""
Updated on Tue Sep 29 2026
@author: Tomasz Mrozewski tmrozews@yorku.ca
"""

# import required libraries
import os # need this to run outside of jupyter
import requests # API calls
import json # handle the output

# set the working directory
my_dir = ' ' # wd set here
os.chdir(my_dir)

# create Authorization header
key = "" # INSERT API TOKEN HERE
headers = {"Authorization": f"Bearer {key}"}

# define endpoints
# replace JOURNAL PATH with appropriate path per https://docs.pkp.sfu.ca/dev/api/ojs/3.5#tag/Access
# keep {issueId} and {publicationId} placeholders intact with formatting - these will be populated later
issueList_endpoint = 'JOURNAL PATH/api/v1/issues' # get list of all issues
issue_endpoint = 'JOURNAL PATH/api/v1/issues/{issueId}' # get issue by ID
edit_endpoint = 'JOURNAL PATH/api/v1/submissions/{submissionId}/publications/{publicationId}' # edit by sub & pub ID

# get list of all issues
# use Count and Offset in more than 100 issues, per https://docs.pkp.sfu.ca/dev/api/ojs/3.5#tag/Pagination
issueList_call = requests.get(issueList_endpoint,headers=headers, params={'isPublished':'true','count':'100'})
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
    issue_call = requests.get(ep,headers=headers)
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
        
        # edit the article
        g = edit_endpoint.replace("{submissionId}",e) # replace sub ID placeholder in endpoint url with e
        h = g.replace("{publicationId}",f) # replace pub ID placeholder in endpoint url with f
        # now, make the edit to change datePublished to d
        j = requests.put(h,params={'apiToken':key},data={'datePublished':d})
        
        print(e,f,j,sep=", ") # print sub and pub ids with API response codes for logging
