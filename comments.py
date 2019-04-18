# -*- coding: utf-8 -*-
"""

author: Chris Brasnett, University of Bristol, christopher.brasnett@bristol.ac.uk

"""

page = 'http://www.dailymail.co.uk/reader-comments/p/asset/readcomments/6935919?max=1000&order=desc&rcCache=shout'

import requests

resp = requests.get(page,headers={'User-Agent':'Mozilla/5.0'})
data = resp.json()

comments = data['payload']

#this is a list of comment
comments_list = comments['page']

for i in range(len(comments_list)):
    if len(comments_list[i]['replies']['comments'])>0:
        print('\n',comments_list[i]['message'])
        replies = comments_list[i]['replies']
        for j in range(len(replies['comments'])):
        
            print('\nnew sub comment:\t', replies['comments'][j]['message'])