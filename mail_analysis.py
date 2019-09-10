# -*- coding: utf-8 -*-
"""

author: Chris Brasnett, University of Bristol, christopher.brasnett@bristol.ac.uk

"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import markovify


with open('comments2316069.txt', 'r') as f:
    t = f.read()
    
t1 = t.split('\n')

phrase = [''] 

          
for p in phrase:
    matches = [s for s in t1 if p in s]
    print(len(matches))
    text = ''.join(matches)
    
    text_model = markovify.Text(text, state_size = 3)


    for i in range(20):
        t = text_model.make_sentence(tries =100)
        try:
            if len(t)>5:
                print(t, '\n')
        except TypeError:
            pass

    try:
        wordcloud = WordCloud(max_font_size = 100, width = 1000, height = 500).generate_from_text(text)
        
        fig, ax = plt.subplots(1,1)
        fig.subplots_adjust(0,0,1,1)
        
        ax.imshow(wordcloud, interpolation = 'bilinear')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        
        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(p+'.png', dpi = 500, bbox_inches = 'tight', pad_inches = 0)
        plt.show()
    except ValueError:
        pass