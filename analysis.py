# -*- coding: utf-8 -*-
"""

author: Chris Brasnett, University of Bristol, christopher.brasnett@bristol.ac.uk

"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud

with open('comments2.txt', 'r') as f:
    t = f.read()
    
t1 = t.split('\n')

phrase = ['england']

          
for p in phrase:
    matches = [s for s in t1 if p in s]
    
    text = ''.join(matches)
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