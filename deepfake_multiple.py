import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
from IPython.display import HTML
import warnings
import sys
import os

from demo import load_checkpoints
from demo import make_animation
from skimage import img_as_ubyte
warnings.filterwarnings("ignore")

if len(sys.argv) < 6:
    print("Usage: deepfake_multiple.py <source name> <template name> <final_vid_name> <rows> <columns> <shuffle?>")
    sys.exit()

source_folder = os.path.join(os.curdir, "resources", "combos", sys.argv[1])
image_folder = os.path.join(os.curdir, "resources", "combos", sys.argv[1], "images")
template_video = os.path.join(os.curdir, "resources", "combos", sys.argv[1], sys.argv[2])
template_video_name = sys.argv[2]
gen_vid_folder = os.path.join(os.curdir, "resources", "combos", sys.argv[1], "gen")
final_vid = os.path.join(os.curdir, "resources", "combos", sys.argv[1], sys.argv[3])
final_vid_name = sys.argv[3]
x = int(sys.argv[4])
y = int(sys.argv[5])
shuffle = ""
if len(sys.argv) > 6:
    print("SHOULD NOT CREATE SHUFFLE")
    shuffle="noshuffle"

list_images = os.listdir(image_folder)
driving_video = imageio.mimread(template_video)
driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]
generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml', 
                            checkpoint_path='vox-cpk.pth.tar')
for image in list_images:
    image_path = os.path.join(image_folder, image)
    source_image = imageio.imread(image_path)
    source_image = resize(source_image, (256, 256))[..., :3]
    gen_vid_name = image.split(".")[0]
    gen_vid_name = f"{gen_vid_name}_gen.mp4"
    gen_vid = os.path.join(gen_vid_folder, gen_vid_name)
    if not os.path.exists(gen_vid):
        predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
        imageio.mimsave(gen_vid, [img_as_ubyte(frame) for frame in predictions])

combiner = os.path.join(os.curdir, "resources", "combos", "createcombo.py")
os.system(f"python3 {combiner} {source_folder} {template_video_name} {final_vid_name} {x} {y} {shuffle}")
sys.exit()




#Resize image and video to 256x256



            

#save resulting video




#predictions2 = make_animation(source_image, driving_video, generator, kp_detector, relative=False, adapt_movement_scale=True)
#imageio.mimsave("testing.mp4", [img_as_ubyte(frame) for frame in predictions2])

#os.system(f"python3 {createvid} {template_video} {gen_vid} {final_vid}")
#print(f"VIDEO GENERATED: {final_vid}")