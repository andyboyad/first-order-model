from moviepy.editor import *
import moviepy.video.fx.all as vfx
import sys
import os
import random

template = sys.argv[1]
template_vid = os.path.join(template, sys.argv[2])
gen_folder = os.path.join(template, "gen")
final_vid = os.path.join(template, sys.argv[3])



gens = sorted(os.listdir(gen_folder), key= lambda x: int(x.split("_")[0]))
print(gens)
first = True
vids = []
for vid in gens:
    vid_path = os.path.join(gen_folder, vid)
    vid_clip = VideoFileClip(vid_path, audio=False)
    vid_clip = vid_clip.fx(vfx.speedx, 3)
    if first:
        template_audio = VideoFileClip(template_vid).audio
        vid_clip.audio = template_audio
        first = False
    vids.append(vid_clip)
print(vids)
final_clip = concatenate_videoclips(vids, method="compose")
final_clip.write_videofile(final_vid, fps=30)




