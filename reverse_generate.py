#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Generate starting template for inverted castle by simply mirroring the normal castle around the origin.
# This generated a starting point for the reverse locations that can be used as a base for further editing.
# It shouldn't be needed to run this script again after the initial generation!

import os

from generate_locations import areas

ORIGIN = (29.5, 23)


def mirror_point(x, y):
    """Mirror a point around the origin."""
    newx, newy = 2 * ORIGIN[0] - x, 2 * ORIGIN[1] - y
    # Convert to int if no decimal part.
    if newx == int(newx):
        newx = int(newx)
    if newy == int(newy):
        newy = int(newy)
    return newx, newy


# Convert normal locations into inverted locations by rotating around the origin.
for area, fname in areas:
    var = os.path.split(fname)[1].split('.')[0]
    if var.startswith("reverse_"):
        continue

    var = "reverse_" + var
    name = "Reverse " + area.name
    print(f"""# {name}""")
    print(f"""{var} = Area("{name}", children=[""")

    # Check for simple location vs location with multiple sections.
    for location in area.children:
        map_loc = location.map_locations[0]
        x, y = mirror_point(map_loc.x, map_loc.y)
        if location.sections:
            print(f"""    Location("{location.name}", map_locations=[inverted.location({x}, {y})], sections=[""")
            for section in location.sections:
                print(f"""        Section("{section.name}"),""")
            print(f"""    ]),""")
        else:
            print(f"""    inverted.simple_location("{location.name}", {x}, {y}),""")

    print(f"""])\n""")
