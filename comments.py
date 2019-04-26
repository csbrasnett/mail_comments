# -*- coding: utf-8 -*-
"""

author: Chris Brasnett, University of Bristol, christopher.brasnett@bristol.ac.uk

"""


import requests
import re
import time
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

plt.rc('text',usetex=True)
plt.rcParams['savefig.dpi'] = 300
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
plt.rcParams.update({'font.size':15})


def articles(url):
    r = requests.get(url)
    
    f = 'dailymail.co.uk/news/article'
    
    #find the articles listed
    k = [m.start() for m in re.finditer(f, r.text)]
    
    arts = []
    
    for i in range(len(k)):
    
        #find links
        a = r.text[k[i]:k[i]+37]
        
        #append links
        arts.append(a)
        
    articles = list(set(arts))
    
    return articles

def comments_list(number):

    #create the page for getting the comment data
    page = 'http://www.dailymail.co.uk/reader-comments/p/asset/readcomments/' + str(number) + '?max=2000&order=desc&rcCache=shout'

    #make the request
    resp = requests.get(page,headers={'User-Agent':'Mozilla/5.0'})
    try:
        data = resp.json()
        try:
            comments = data['payload']
            
            #this is a list of comment
            comments_list = comments['page']
                    
            comments_text = []
            
            #append each comment and reply to a list
            for i in range(len(comments_list)):
                m = comments_list[i]['message']
                comments_text.append(m)

                if len(comments_list[i]['replies']['comments'])>0:                    
                    replies = comments_list[i]['replies']
                    for j in range(len(replies['comments'])):
                        m1 = replies['comments'][j]['message']
                        comments_text.append(m1)
            return comments_text
        except TypeError:
            pass
    except ValueError:
        pass
    
    return 0

'''
use this to iteratively scrape from the homepage
'''
##url to page
#url = 'http://dailymail.co.uk'
#
##get articles list
#t = articles(url)
#
##get some more articles
#more_articles = []
#for i in t:
#    t1 = articles('http://'+i)
#    
#    for j in t1:
#        if j.find('.rss') == -1:
#            more_articles.append(j)
#
##find all the articles
#unique_more_articles = list(set(more_articles))
#all_articles = list(set(t+unique_more_articles))

#make a list of all the comments from all the articles found.
#for k in range(len(all_articles)):
#    
#    #get the articles code
#    val = all_articles[k][-8:-1]
#


'''
find comments from brute force searching
'''

opfilename = 'comments1.txt'

if os.path.exists(opfilename):
    os.remove(opfilename)

end = 6959317
start = end - 50000

all_comments = []

p = np.zeros(0)
c = np.zeros(0)

for k in range(start,end):
    time.sleep(0.1)
    #get the list of comments
    comms = comments_list(k)

    
    #put the comments into a list
    if type(comms)!=int:
        for l in comms:
            all_comments.append(l)

        #write to file
        with open(opfilename, 'a') as f:
            for i in range(len(comms)):
                f.write('%s\n' %comms[i])
    
    prog = ((len(range(start, end))-(range(start, end)[-1]-k))/len(range(start, end))) * 100
    
    
    p = np.append(p, prog)
    c = np.append(c, len(all_comments))

    print('%.3f%% progress, %d comments' %(prog, len(all_comments)))

#write list to pickle file
pickle.dump(all_comments,open('all_comments.p','wb'))

fig, ax = plt.subplots(1,1)

ax.plot(p,c)
ax.set_xlabel('Scraping progress (\%)')
ax.set_ylabel('Total number of comments')
ax.set_xlim(0,p.max())
ax.set_ylim(0,c.max())
fig.savefig('fig.png', bbox_inches = 'tight')