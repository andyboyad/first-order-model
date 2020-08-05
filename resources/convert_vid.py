from moviepy.editor import *
import sys
import os

template = sys.argv[1]
template_new = sys.argv[2]

template_clip = VideoFileClip(template)
template_clip = template_clip.resize(width=256,height=256)
template_clip.write_videofile(template_new)

os.remove(template)
os.rename(template_new, template)