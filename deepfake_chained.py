import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
from IPython.display import HTML
import warnings
import sys
import os 
import random

from demo import load_checkpoints
from demo import make_animation
from skimage import img_as_ubyte
warnings.filterwarnings("ignore")

if len(sys.argv) < 5:
    print("Usage: deepfake_multiple.py <source name> <template name> <final_vid_name> <interval>")
    sys.exit()

source_folder = os.path.join(os.curdir, "resources", "chained", sys.argv[1])
image_folder = os.path.join(os.curdir, "resources", "chained", sys.argv[1], "images")
template_video = os.path.join(os.curdir, "resources", "chained", sys.argv[1], sys.argv[2])
template_video_name = sys.argv[2]
gen_vid_folder = os.path.join(os.curdir, "resources", "chained", sys.argv[1], "gen")
final_vid = os.path.join(os.curdir, "resources", "chained", sys.argv[1], sys.argv[3])
final_vid_name = sys.argv[3]
interval = int(30*float(sys.argv[4]))

list_images = os.listdir(image_folder)
#random.shuffle(list_images)
print(template_video)
driving_video_source = imageio.get_reader(template_video)
driving_video = []
while True:
    try:
        d = driving_video_source.get_next_data()
    except Exception:
            break
    else:
        driving_video.append(resize(d, (256, 256))[..., :3])
generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml', 
                            checkpoint_path='vox-cpk.pth.tar')
print("LOADED VIDEO")
images_pointer = 0
counter=0
print(interval)
print(len(driving_video))
for m in range(0, len(driving_video), interval):
    inter = m
    image = list_images[images_pointer]
    images_pointer+=1
    if images_pointer >= len(list_images):
        images_pointer=0
    image_path = os.path.join(image_folder, image)
    source_image = imageio.imread(image_path)
    source_image = resize(source_image, (256, 256))[..., :3]
    gen_vid_name = image.split(".")[0]
    gen_vid_name = f"{inter}_gen.mp4"
    gen_vid = os.path.join(gen_vid_folder, gen_vid_name)
    if not os.path.exists(gen_vid):
        predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
        imageio.mimsave(gen_vid, [img_as_ubyte(frame) for frame in predictions[inter:inter+interval]])

print("???")
combiner = os.path.join(os.curdir, "resources", "chained", "createchained.py")
os.system(f"python3 {combiner} {source_folder} {template_video_name} {final_vid_name}")
sys.exit()




#Resize image and video to 256x256



            

#save resulting video




#predictions2 = make_animation(source_image, driving_video, generator, kp_detector, relative=False, adapt_movement_scale=True)
#imageio.mimsave("testing.mp4", [img_as_ubyte(frame) for frame in predictions2])

#os.system(f"python3 {createvid} {template_video} {gen_vid} {final_vid}")
#print(f"VIDEO GENERATED: {final_vid}")