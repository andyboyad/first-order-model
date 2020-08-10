import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
from IPython.display import HTML
import warnings
import sys
import os

warnings.filterwarnings("ignore")

if len(sys.argv) != 5:
    print("Usage: deepfake.py <image> <template> <generated_vid_name> <final_vid_name>")
    sys.exit()

first_img = os.path.join(os.curdir, "resources", "images", sys.argv[1])
template_video = os.path.join(os.curdir, "resources", "templates", sys.argv[2])
gen_vid = os.path.join(os.curdir, "resources", "generated_videos", sys.argv[3])
final_vid = os.path.join(os.curdir, "resources", "final_videos", sys.argv[4])
createvid = os.path.join(os.curdir, "resources", "createvid.py")

source_image = imageio.imread(first_img)
driving_video_source = imageio.get_reader(template_video)
print("READ")


#Resize image and video to 256x256

source_image = resize(source_image, (256, 256))[..., :3]
driving_video = []
print("NOT PROCESSING YET")
while True:
    try:
        d = driving_video_source.get_next_data()
    except Exception:
            break
    else:
        driving_video.append(resize(d, (256, 256))[..., :3])
#driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]
print("PROCESSED DRIVING VIDEO")
print(len(driving_video))
def display(source, driving, generated=None):
    fig = plt.figure(figsize=(8 + 4 * (generated is not None), 6))

    ims = []
    for i in range(len(driving)):
        cols = [source]
        cols.append(driving[i])
        if generated is not None:
            cols.append(generated[i])
        im = plt.imshow(np.concatenate(cols, axis=1), animated=True)
        plt.axis('off')
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=1000)
    plt.close()
    return ani

from demo import load_checkpoints
#generator, kp_detector = load_checkpoints(config_path='config/vox-adv-256.yaml', 
#                            checkpoint_path='vox-adv-cpk.pth.tar')
generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml', 
                            checkpoint_path='vox-cpk.pth.tar')            


from demo import make_animation
from skimage import img_as_ubyte

predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)

#save resulting video
imageio.mimsave(gen_vid, [img_as_ubyte(frame) for frame in predictions])

#predictions2 = make_animation(source_image, driving_video, generator, kp_detector, relative=False, adapt_movement_scale=True)
#imageio.mimsave("testing.mp4", [img_as_ubyte(frame) for frame in predictions2])

os.system(f"python3 {createvid} {template_video} {gen_vid} {final_vid}")
print(f"VIDEO GENERATED: {final_vid}")