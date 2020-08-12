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
    print("Usage: deepfake_multiple_acopella.py <source_folder> <image_name> <final_vid_name> <rows> <columns> <acopella clip>")
    sys.exit()

source_folder = os.path.join(os.curdir, "resources", "combos", sys.argv[1])

image_name = sys.argv[2]
image_path = os.path.join(source_folder, "images")
template_folder = os.path.join(source_folder, "templates")
#template_video_name = lambda x,y: os.path.join(template_folder, f"{sys.argv[3]}_{x}_{y}.mp4")
gen_folder = os.path.join(source_folder, "gen")
final_vid = os.path.join(source_folder, sys.argv[3])
final_vid_name = sys.argv[3]
x = int(sys.argv[4])
y = int(sys.argv[5])
acopella_name = sys.argv[6]
generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml', 
                            checkpoint_path='vox-cpk.pth.tar')
list_templates = os.listdir(template_folder)
list_image = os.listdir(image_path)
#source_image = imageio.imread(image_path)
#source_image = resize(source_image, (256, 256))[..., :3]
first = True
first_template_video_name = None
for template_video,cur_image in zip(list_templates, list_image):
    print(template_video)
    print(cur_image)
    if first:
        first_template_video_name = template_video
        first = False
    template_video_path = os.path.join(template_folder, template_video)
    image_cur_path = os.path.join(image_path, cur_image)
    source_image = imageio.imread(image_cur_path)
    source_image = resize(source_image, (256, 256))[..., :3]
    template_video_name = template_video.split(".")[0]
    img_name = image_name.split(".")[0]
    gen_vid = os.path.join(gen_folder, f"{img_name}_{template_video_name}_gen.mp4")
    if not os.path.exists(gen_vid):
        driving_video_source = imageio.get_reader(template_video_path)
        print(template_video_path)
        driving_video = []
        while True:
            try:
                d = driving_video_source.get_next_data()
            except Exception:
                print("processing video")
                break
            else:
                driving_video.append(resize(d, (256, 256))[..., :3])
        predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
        imageio.mimsave(gen_vid, [img_as_ubyte(frame) for frame in predictions])

combiner = os.path.join(os.curdir, "resources", "combos", "createcombo_acopella.py")
os.system(f"python3 {combiner} {source_folder} {first_template_video_name} {final_vid_name} {x} {y} {acopella_name}")
sys.exit()




#Resize image and video to 256x256



            

#save resulting video




#predictions2 = make_animation(source_image, driving_video, generator, kp_detector, relative=False, adapt_movement_scale=True)
#imageio.mimsave("testing.mp4", [img_as_ubyte(frame) for frame in predictions2])

#os.system(f"python3 {createvid} {template_video} {gen_vid} {final_vid}")
#print(f"VIDEO GENERATED: {final_vid}")