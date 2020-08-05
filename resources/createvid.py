from moviepy.editor import *
import moviepy.video.fx.all as vfx
import sys
import os

#template = os.path.join(os.curdir, "templates", sys.argv[1])
#deepfake = os.path.join(os.curdir, "generated_videos", sys.argv[2])
#newfile = os.path.join(os.curdir, "final_videos", sys.argv[3])

template = sys.argv[1]
deepfake = sys.argv[2]
newfile = sys.argv[3]


deepfake_clip = VideoFileClip(deepfake, audio=False)
deepfake_clip = deepfake_clip.fx(vfx.speedx , 3)

template_audio = VideoFileClip(template).audio

deepfake_clip.audio = template_audio
final = CompositeVideoClip([deepfake_clip])
final.write_videofile(newfile, fps=30)
