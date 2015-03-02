"""
If you have multiple monitors, there's not a good way to set the wallpaper individually,
so just create one bitmap image out of the multiple wallpapers.
"""
import os.path
import ctypes
import json

try:
  import _winreg
except ImportError:
  import winreg as _winreg

from PIL import Image

with open("settings.json", "r") as sf:
    set_dict = json.load(sf)

    monitor_reses = set_dict["monitor_resolutions"]

    merge_path = os.path.abspath(set_dict["merge_path"])

    desktop_locs = set_dict["desktop_locs"]

    image_path = set_dict["image_path"]
    image_names = set_dict["image_names"]

    img_mode = set_dict['img_mode']

img_size = (sum(r[0] for r in monitor_reses),
            max(r[1] for r in monitor_reses))

img = Image.new(img_mode, img_size)

luwh_to_lurl = lambda l, u, w, h: tuple([int(x) for x in [l, u, l+w, u+h]])

for ii, name in enumerate(image_names):
    im = Image.open(image_path+name)
    im = im.convert(img_mode)

    lbuff = (monitor_reses[ii][0]-im.size[0])/2
    tbuff = (monitor_reses[ii][1]-im.size[1])/2

    lbuff = 0 if lbuff < 0 else lbuff
    tbuff = 0 if tbuff < 0 else tbuff

    left = sum(r[0] for monitor_rses[0:desktop_locs])
    img.paste(im, luwh_to_lurl(left + lbuff,
                               tbuff,
                               im.size[0],
                               im.size[1]))

img.save(merge_path)