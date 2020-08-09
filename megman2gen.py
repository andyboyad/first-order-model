import os

img = "yandere.png"
name = "megman"
vid_name = lambda x,y: f"{name}_{x}_{y}.mp4"
vid_name_gen = lambda x,y: f"{name}_{x}_{y}_gens.mp4"
vid_name_final = lambda x,y: f"{name}_{x}_{y}_final.mp4"

for x in range(3):
    for y in range(3):
        os.system(f"python3 deepfake.py {img} {vid_name(x, y)} {vid_name_gen(x,y)} {vid_name_final(x,y)}")  
print("DONE") 