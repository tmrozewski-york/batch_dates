# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 22:21:32 2022

@author: tomas
"""

import os
import requests
import json
from pprint import pprint as pp


# set the working directory
my_dir = 'C:\\Users\\tomas\\OneDrive\\Documents\\CSCH dates' # wd set here
os.chdir(my_dir)


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IjczOTI1NDI2OTgxMzI2OGJiYTMwYTQ5OWQzMDA0NmU1ODJlYmEyZWIi.tXLaOyy1FZLcjdzGXb2MEkb3zOB3DebD-oNsAd70CHc'
subId = 97

get1 = 'https://jat.journals.yorku.ca/index.php/default/api/v1/submissions/{submissionId}/publications'
get2 = get1.replace('{submissionId}',str(subId))
getting = requests.get(get2,params={'apiToken':token}).text
data = json.loads(getting)
q = data['items'][0]['pages']
print(q)
newpage = '15'
pubId = data['items'][0]['id']

# unpub1 = 'https://jat.journals.yorku.ca/index.php/default/api/v1/submissions/{submissionId}/publications/{publicationId}/unpublish'
# unpub2 = unpub1.replace('{submissionId}',str(subId))
# unpub3 = unpub2.replace('{publicationId}',str(pubId))
# a = requests.put(unpub3,params={'apiToken':token})
# print(a)

# ver1 = 'https://jat.journals.yorku.ca/index.php/default/api/v1/submissions/{submissionId}/publications/{publicationId}/version'
# ver2 = ver1.replace('{submissionId}',str(subId))
# ver3 = ver2.replace('{publicationId}',str(pubId))
# b = requests.post(ver3,params={'apiToken':token})

edit1 = 'https://jat.journals.yorku.ca/index.php/default/api/v1/submissions/{submissionId}/publications/{publicationId}'
edit2 = edit1.replace('{submissionId}',str(subId))
edit3 = edit2.replace('{publicationId}','141')
c = requests.put(edit3,params={'apiToken':token,'pages':newpage})
print(c)
