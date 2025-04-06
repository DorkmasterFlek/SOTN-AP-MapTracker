#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Generate text images for settings in SOTN map tracker using SOTN font and split them up.

import math

from PIL import Image, ImageDraw, ImageFont

labels = [
    ('Closed', 'closed'),
    ('Opened', 'opened'),
    ('Full', 'full'),
    ('Relic/Prog', 'relic_prog'),
    ('Guarded', 'guarded'),
    ('Equipment', 'equipment'),
]
text = '\n'.join(l[0] for l in labels)
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
for i, (label, fname) in enumerate(labels):
    img = Image.new("RGBA", (1000, 1000), img_colour)

    draw = ImageDraw.Draw(img)
    draw_point = (0, 0)
    draw.text(draw_point, label, font=font, fill=text_color)

    bbox = img.getbbox()
    img = img.crop((0, 0, max(bbox[2], label_width), max(bbox[3], label_height)))
    img.save(f"images/settings/{fname}.png", "PNG")

    print(f"Saved {label} image.")
