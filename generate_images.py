#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Generate text images for settings in SOTN map tracker using SOTN font and split them up.

import math
import re

from PIL import Image, ImageDraw, ImageFont

labels = [
    'Closed',
    'Opened',
    'Full',
    'Relic/Prog',
    'Guarded',
    'Equipment',
    'Enabled',
    'Disabled',
]
text = '\n'.join(labels)
text_color = (255, 255, 255, 255)
# text_color = (0, 0, 0, 255)
img_colour = (0, 0, 0, 0)

font = ImageFont.truetype("SymphonyoftheNightfont.ttf", 32)
img = Image.new("RGBA", (1000, 1000), img_colour)

draw = ImageDraw.Draw(img)
draw_point = (0, 0)
draw.text(draw_point, text, font=font, fill=text_color)

text_window = img.getbbox()
img = img.crop(text_window)

# Figure out how big each label should be.
img_width, img_height = img.size
# print(f"Image size: {img_width} x {img_height}")
label_width = img_width
label_height = math.ceil(img_height / len(labels))
# print(f"Label size: {label_width} x {label_height}")

# Make new image the same size for each label.
for i, label in enumerate(labels):
    # Make filename by converting label to lowercase and replacing non-words with underscores.
    fname = re.sub(r'\W+', '_', label.lower())

    img = Image.new("RGBA", (1000, 1000), img_colour)

    draw = ImageDraw.Draw(img)
    draw_point = (0, 0)
    draw.text(draw_point, label, font=font, fill=text_color)

    bbox = img.getbbox()
    img = img.crop((0, 0, max(bbox[2], label_width), max(bbox[3], label_height)))
    img_fname = f"images/settings/{fname}.png"
    img.save(img_fname, "PNG")

    print(f"Saved {img_fname}")
