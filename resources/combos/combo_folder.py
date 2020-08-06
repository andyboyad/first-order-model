import os
import sys

if len(sys.argv) != 2:
    print("usage: combo_folder.py <name of combo>")
    sys.exit()

name = sys.argv[1]
if os.path.exists(name):
    print(f"combo {name} already exists")
    sys.exit()
os.mkdir(name)
gen_folder = os.path.join(name, "gen")
images_folder = os.path.join(name, "images")
os.mkdir(gen_folder)
os.mkdir(images_folder)
print(f"combo folder created for {name}")


