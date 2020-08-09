from moviepy.editor import *
import moviepy.video.fx.all as vfx
import sys
import os
import random

template = sys.argv[1]
template_vid = os.path.join(template, "templates", sys.argv[2])
#template_vid = os.path.join(template, sys.argv[2])
gen_folder = os.path.join(template, "gen")
final_vid = os.path.join(template, sys.argv[3])
row = int(sys.argv[4])
column = int(sys.argv[5])
acopella_vid = os.path.join(template, sys.argv[6])

gens = os.listdir(gen_folder)
if row*column < len(gens):
    print(f"Error: there are {len(gens)} videos but dimensions are {row}*{column}")
    sys.exit()

first = True
vids = []
vids_row = []
x = 0
y = 0
for vid in gens:
    if x == 1 and y == 1:
        vid_clip = VideoFileClip(acopella_vid, audio=False)
        vids_row.append(vid_clip)
        x+=1
    vid_path = os.path.join(gen_folder, vid)
    vid_clip = VideoFileClip(vid_path, audio=False)
    vid_clip = vid_clip.fx(vfx.speedx, 3)
    if first:
        template_audio = VideoFileClip(template_vid).audio
        vid_clip.audio = template_audio
        first = False
    vids_row.append(vid_clip)
    x+=1
    if len(vids_row) == row:
        vids.append(vids_row[:])
        vids_row = []
        y+=1
        x=0
    
if len(vids_row) != 0:
    vids.append(vids_row)
print(vids)
final_clip = clips_array(vids)
final_clip.write_videofile(final_vid, fps=30)




