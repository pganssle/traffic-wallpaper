"""
Script that pulls the traffic map from Houston TranStar and a bunch of 
traffic cameras and merges it to a background image.

This was slapped-together in not much time - it could use cleaning up.
"""
from __future__ import division         # Use Python 3.x division

import requests
import shutil

from PIL import Image
import json
import os

# Functions and classes for handling downloads
class HTTPError(Exception):
    pass

def download_image(url, loc, error=None):
    """
    Downloads the image at `url` to `loc`.

    @param error:
        If `True`, an error is thrown whenever it is not possible to download
        the image. If `False`, errors are never thrown. If `None` or omitted,
        an error is thrown only when the file does not exist (e.g. if it has
        has been downloaded once it will be skipped).
    
    @raises HTTPError
    """
    resp = requests.get(url, stream=True)
    status = resp.status_code
    if status == 200:
        file_obj = resp.raw
        with open(loc, 'wb') as img:
            shutil.copyfileobj(file_obj, img)
    else:
        if error or (error is None and not os.path.exists(loc)):
            raise HTTPError('An HTTP error has occurred, response code: ' +
                            repr(status))



# Load settings
with open("settings.json", "r") as sf:
    set_dict = json.load(sf)

    bg_color = set_dict["bg_color"]
    img_mode = set_dict["img_mode"]
    monitor_res = tuple(set_dict["monitor_resolution"])
    cam_width, cam_height = set_dict["cam_size"]

    cam_urls, cam_poses, crop_boxes = zip(*[(cam["url"],
                                            cam["loc"],
                                            cam.get("crop_box", set_dict["default_crop_box"]))
                                           for cam in set_dict["cams"]])
    cam_grid = tuple(set_dict["cam_grid"])

    map_url = set_dict["map_url"]
    map_crop_box = set_dict["map_crop_box"]

    id_fold = set_dict["id_fold"]

###
# Image Download
###
tm_loc = os.path.join(id_fold, 'traffic_map.gif')
cam_locs = os.path.join(id_fold, 'img_{:02.0f}.jpg')

download_image(map_url, tm_loc)
for ii, url in enumerate(cam_urls):
    download_image(url, cam_locs.format(ii))

###
# Image Patching
###

# Convenience functions
luwh_to_lurl = lambda box: tuple(int(x) for x in (box[0], box[1], box[0]+box[2], box[1]+box[3]))

# Function for camera transforms
def transform_cam(loc, cam_width=cam_width, cam_height=cam_height,
                  img_mode=img_mode, crop_box=None):
    """
    Opens a camera image file, then returns the cropped and scaled version.
    
    :param loc:
        Image file to transform.

    :param cam_width:
        The final width of the output. If `None` is passed to this and
        :param:`cam_height` is specified, this is set from the aspect
        ratio post-cropping. If both are set to `None`, then no
        resizing is applied.

    :param cam_height:
        The final height of the output. If `None` is passed to this and
        :param:`cam_width` is specified, this is set from the aspect
        ratio post-cropping. If both are set to `None`, then no
        resizing is applied.

    :param img_mode:
        The mode with which to open the image (e.g. RGB, CMYK, etc)

    :param crop_box:
        A 4-element indexable sequence where to crop the image before resizing.
        Takes the form:

            `[left, top, right, bottom]`

        Use negative numbers with a "1-based index" for relative cropping, so -1 is
        the rightmost edge of the image (e.g. `(0, 0, 0, -16)` crops 15 pixels off 
        the bottom of the image.)
    """

    im = Image.open(loc)

    # Handle negative values in the crop box
    crop_box = list(crop_box)
    for ii, val in enumerate(crop_box):
        if val < 0:
            val += 1
            val += im.size[ii % 2]

            if val <= 0:
                raise ValueError('Crop box negative indexing greater than image size.')

        crop_box[ii] = val

    # Handle unspecified final sizes.
    rs_size = (crop_box[2] - crop_box[0], crop_box[3] - crop_box[1])
    if cam_width is None and cam_height is None:
        cam_width, cam_height = rs_size
    elif cam_width is None:
        cam_width = cam_height * (rs_size[0] / rs_size[1])
    elif cam_height is None:
        cam_height = cam_width * (rs_size[1] / rs_size[0])

    # Apply the transformation
    new_size = (cam_width, cam_height)
    im = im.convert(img_mode)
    region = im.crop(crop_box)
    return region.resize((cam_width, cam_height))

# Create the new image
img = Image.new(img_mode, monitor_res, bg_color)

# Modify and paste in the webcam photos
col_buff = ((monitor_res[0] - cam_width) / (cam_grid[0]-1)) - cam_width
row_buff = ((monitor_res[1] - cam_height) / (cam_grid[1]-1)) - cam_height
column_locs = [ii * (cam_width + col_buff) for ii in range(cam_grid[0])]
row_locs = [ii * (cam_height + row_buff) for ii in range(cam_grid[1])]

for ii in range(len(cam_urls)):
    c_img = transform_cam(cam_locs.format(ii), cam_width=cam_width,
                                               cam_height=cam_height,
                                               img_mode=img_mode,
                                               crop_box=crop_boxes[ii])
    img.paste(c_img, luwh_to_lurl((column_locs[cam_poses[ii][0]],
                                   row_locs[cam_poses[ii][1]],
                                   cam_width,
                                   cam_height)))

# Map needs to be scaled to accomodate 1 camera image on either side, plus one above and below.
map_new_size = (monitor_res[0] - 2 * cam_width, monitor_res[1] - 2 * cam_height)
map_crop_box = luwh_to_lurl(map_crop_box)

mimg = Image.open(tm_loc)
mimg = mimg.convert(img_mode)
region = mimg.crop(map_crop_box)
region = region.resize(map_new_size)

img.paste(region, luwh_to_lurl((cam_width, cam_height, map_new_size[0], map_new_size[1])))


img.save('images/wallpaper/composite_map.png')
