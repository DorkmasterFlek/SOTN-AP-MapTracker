#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Map tracker locations for Castlevania: Symphony of the Night.

# Using my PopTracker Python library to make generating the location JSON easier.
# See: https://github.com/DorkmasterFlek/poptrackerlib-py

import os
import sys

sys.path.append('../poptrackerlib-py/src')

from poptrackerlib import dumps
from poptrackerlib.locations import Map, Area, Location, Section, MapLocation

normal = Map('normal', scale=20, offset=32)
inverted = Map('inverted', scale=20, offset=32)
vertical = Map('vertical', scale=20, offset=32)

LOCATIONS_MAPPING = {}
HOSTED_ITEMS = {}


def process_area(area, prefix=''):
    """Process an area and its children recursively .

    Args:
        area(Area): The area to process.
        prefix(str): The in progress prefix to add to the location names.
    """
    if not prefix:
        prefix = '@' + area.name
    else:
        prefix += '/' + area.name

    for child in area.children:
        if isinstance(child, Area):
            process_area(child, prefix)
        elif isinstance(child, Location):
            process_location(child, prefix)
        else:
            raise TypeError(f"Unknown child type: {child.__class__.__name__}")


def process_location(location, prefix):
    """Process a location and its sections.

    Args:
        location(Location): The location to process.
        prefix(str): The prefix to add to the location names.
    """

    # Add corresponding vertical map positions.
    if len(location.map_locations) != 1:
        raise ValueError(f"Location {location.name} has {len(location.map_locations)} map locations!")

    loc = location.map_locations[0]
    if loc.map is normal:
        location.map_locations.append(MapLocation(vertical, loc.x, loc.y + 49.25))
    else:
        location.map_locations.append(MapLocation(vertical, loc.x, loc.y))

    prefix += '/' + location.name
    for section in location.sections:
        # Skip the final boss location; it doesn't have an ID.
        if section.location_id is None:
            continue

        code = prefix + '/' + section.name
        zone = prefix.split('/')[0].strip('@')
        LOCATIONS_MAPPING.setdefault(zone, {})

        ids = section.location_id
        if not isinstance(ids, (list, tuple)):
            ids = [ids]

        for loc_id in ids:
            LOCATIONS_MAPPING[zone][loc_id] = code

        # If section has a hosted item, record that as well.
        if section.hosted_item:
            HOSTED_ITEMS[section.location_id] = section.hosted_item


def boss_location(name, code, map, x, y, location_id, **kwargs):
    return Location(name, map_locations=[map.location(x, y)], sections=[
        Section(name + ' kill', hosted_item=code, location_id=location_id),
    ], **kwargs)


# *** Normal castle

# Entrance
entrance = Area('Castle Entrance', children=[
    normal.simple_location('Above First Encounter With Death', 17, 34, visibility_rules=['logic_full'], location_id=109),
    normal.simple_location('Right Alcove in Cube of Zoe Room', 18, 32, access_rules=['$canJump'], visibility_rules=['logic_full'], location_id=110),
    Location('Wolf-Bat Secret Room', map_locations=[normal.location(8, 36)], access_rules=['soulofbat,soulofwolf'], sections=[
        Section('Left Item', visibility_rules=['logic_equipment'], location_id=117),
        Section('Right Item', visibility_rules=['logic_full'], location_id=111),
    ]),
    normal.simple_location('Behind Stone Wall in Cube of Zoe Room', 17, 31, visibility_rules=['logic_full'], location_id=112),
    normal.simple_location('Attic Above Mermans', 3, 33, access_rules=['$canFly'], visibility_rules=['logic_full'], location_id=113),
    normal.simple_location('Castle Entrance Teleport Exit', 15, 33, visibility_rules=['logic_full'], location_id=115),
    Location('Attic Near Start Gate', map_locations=[normal.location(0.5, 33)], access_rules=['$canFly'], sections=[
        Section('Left Item', visibility_rules=['logic_relic_prog'], location_id=121),
        Section('Right Item', visibility_rules=['logic_full'], location_id=116),
    ]),
    normal.simple_location('Breakable Wall Above Merman', 10, 35, visibility_rules=['logic_full'], location_id=118),
    normal.simple_location('Breakable Ledge Before Death', 17, 35, visibility_rules=['logic_full'], location_id=119),
    normal.simple_location('Pedestal in Cube of Zoe Room', 16, 31, visibility_rules=['logic_relic_prog'], location_id=120),
])

# Alchemy Laboratory
alchemy_lab = Area('Alchemy Laboratory', children=[
    normal.simple_location('Globe by the Bottom Entrance', 12, 31, visibility_rules=['logic_full'], location_id=158),
    normal.simple_location('Globe in Hidden Room Behind Breakable Wall', 9, 29, visibility_rules=['logic_full'], location_id=159),
    normal.simple_location('Globe After Spike Puzzle', 8, 24, visibility_rules=['logic_equipment'], location_id=160),
    normal.simple_location('Tank in Hidden Basement on Breakable Floor', 10, 31, visibility_rules=['logic_full'], location_id=161),
    normal.simple_location('Globe on Middle Elevator Shaft Room', 14, 26, visibility_rules=['logic_equipment'], location_id=162),
    normal.simple_location('Flame on Table Middle Way Up', 9, 27, visibility_rules=['logic_full'], location_id=163),
    normal.simple_location('Flame Near Spike Switch', 11, 30, visibility_rules=['logic_full'], location_id=164),
    normal.simple_location('Item by Cannon', 14, 29, visibility_rules=['logic_equipment'], location_id=165),
    normal.simple_location('Globe in Big Room With Axe Lord and Spittle Bone', 17, 22, visibility_rules=['logic_full'], location_id=166),
    normal.simple_location('Globe in Attic With Powerup Tanks', 13, 28, access_rules=['$canHighJump'],
                           visibility_rules=['logic_relic_prog'], location_id=167),
    normal.simple_location('Globe in Upper-left Room of Slogra and Gaibon', 11, 22, access_rules=['$canHighJump'],
                           visibility_rules=['logic_relic_prog'], location_id=168),
    # normal.simple_location('Slogra & Gaibon Item', 8.5, 22.5, visibility_rules=['boss_locations'], location_id=387),
])

# Marble Gallery
marble_gallery = Area('Marble Gallery', children=[
    normal.simple_location("Left Clock Before Olrox's Quarters", 29, 20, access_rules=['$canJump', 'open_are,jewelofopen'],
                           visibility_rules=['logic_full'], location_id=71),
    # Need Cube of Zoe to get stop watch from candles!
    Location('Right Clock', map_locations=[normal.location(31.5, 20)], access_rules=['cubeofzoe,$canJump'], sections=[
        Section('Item 1', visibility_rules=['logic_full'], location_id=72),
        Section('Item 2', visibility_rules=['logic_full'], location_id=73),
        Section('Item 3', visibility_rules=['logic_full'], location_id=77),
        Section('Item 4', visibility_rules=['logic_equipment'], location_id=78),
    ]),
    Location('Middle Clock Left', map_locations=[normal.location(28.5, 18)], access_rules=['$canFly'], visibility_rules=['logic_full'], sections=[
        Section('Left Item 1', location_id=74),
        Section('Left Item 2', location_id=75),
        Section('Left Item 3', location_id=76),
    ]),
    Area('Inside Clock', access_rules=['silverring,goldring'], children=[
        Location('Inside Clock', map_locations=[normal.location(31, 22)], visibility_rules=['logic_full'], sections=[
            Section('Left Item', location_id=79),
            Section('Right Item', location_id=80),
        ]),
        normal.simple_location('Item Given by Maria', 30, 26, visibility_rules=['logic_relic_prog'], location_id=85),
    ]),
    Location('Below Red Trap Door', map_locations=[normal.location(42, 21)], access_rules=['jewelofopen'], visibility_rules=['logic_full'], sections=[
        Section('Left Item', location_id=82),
        Section('Right Item', location_id=81),
    ]),
    normal.simple_location('Descend to Entrance Item 1', 24, 23, access_rules=['$canHighJump'], visibility_rules=['logic_full'], location_id=84),
    normal.simple_location('Descend to Entrance Item 2', 24, 25, access_rules=['$canHighJump'], visibility_rules=['logic_full'], location_id=83),
    normal.simple_location('Descend to Entrance Item 3', 23, 26, visibility_rules=['logic_relic_prog'], location_id=86),
    normal.simple_location('Middle Clock Right Item', 32, 18, access_rules=['$canFly'], visibility_rules=['logic_relic_prog'], location_id=87),
])

# Outer Wall
outer_wall = Area('Outer Wall', children=[
    Location('Behind Mist Grate', map_locations=[normal.location(57, 22)], sections=[
        Section('Item 1', visibility_rules=['logic_equipment'], location_id=88),
        Section('Item 2', visibility_rules=['logic_full'], location_id=89),
    ]),
    normal.simple_location('Red Vase Near Elevator Switch', 58, 10, visibility_rules=['logic_full'], location_id=90),
    normal.simple_location('Yellow Vase on High Ledge', 59, 19, access_rules=['$canJump'], visibility_rules=['logic_full'], location_id=91),
    normal.simple_location('Item After Doppleganger 10', 57, 18, visibility_rules=['logic_equipment'], location_id=92),
    normal.simple_location('Red Vase After Doppleganger 10', 59, 18, visibility_rules=['logic_full'], location_id=93),
    normal.simple_location('Red Vase Near Marble Gallery Door', 59, 20, visibility_rules=['logic_full'], location_id=94),
    normal.simple_location('Breakable Wall in Room Behind Armor Lord', 57, 21, visibility_rules=['logic_full'], location_id=95),
    normal.simple_location('Inside of Elevator', 59, 13, visibility_rules=['logic_relic_prog'], location_id=96),
])

# Long Library
library = Area('Long Library', children=[
    normal.simple_location('Item Below Librarian', 47, 16, visibility_rules=['logic_equipment'], location_id=60),
    Location('Top Left Room', map_locations=[normal.location(50, 13)], access_rules=['$canJump'], sections=[
        Section('Item 1', visibility_rules=['logic_relic_prog'], location_id=69),
        Section('Item 2', visibility_rules=['logic_full'], location_id=64),
        Section('Item 3', visibility_rules=['logic_full'], location_id=65),
    ]),
    normal.simple_location('Top Right Floor', 57, 13, visibility_rules=['logic_relic_prog'], location_id=68),
    normal.simple_location('Librarian Shop Item', 47, 15, visibility_rules=['logic_relic_prog'], location_id=70),
    Area('Deeper Library', access_rules=['$canJump'], children=[
        normal.simple_location('Upper Part Flame on Table', 47, 13, visibility_rules=['logic_full'], location_id=58),
        Location('Deeper Library Behind Bookshelf', map_locations=[normal.location(48, 13)], sections=[
            Section('Item 1', visibility_rules=['logic_full'], location_id=66),
            Section('Item 2', visibility_rules=['logic_equipment'], location_id=59),
        ]),
        Location('Deeper Library Lower Part', map_locations=[normal.location(44, 16)], sections=[
            Section('Statue 1', visibility_rules=['logic_full'], location_id=61),
            Section('Statue 2', visibility_rules=['logic_equipment'], location_id=62),
            Section('Red Vase', visibility_rules=['logic_full'], location_id=63),
        ]),
        normal.simple_location('Deeper Library Behind Mist Crate', 46, 16, access_rules=['mist'],
                               visibility_rules=['logic_relic_prog'], location_id=67),
    ]),
])

# Royal Chapel
chapel = Area('Royal Chapel', access_rules=['jewelofopen', '$canJump'], children=[
    Location('Middle of Stairs', map_locations=[normal.location(4, 18)], access_rules=['$canJump'], sections=[
        Section('Red Vase on Alcove 4', visibility_rules=['logic_equipment'], location_id=42),
        Section('Red Vase on Alcove 5', visibility_rules=['logic_full'], location_id=49),
    ]),
    normal.simple_location('Upper Alcove', 7, 16, access_rules=['$canJump'], visibility_rules=['logic_equipment'], location_id=43),
    normal.simple_location('Item Behind Maria', 6, 10, access_rules=['jewelofopen,formofmist,spikebreaker'],
                           visibility_rules=['logic_relic_prog'], location_id=44),
    normal.simple_location('Bottom Red Vase', 0, 22, visibility_rules=['logic_full'], location_id=45),
    Location('Bottom of Stairs', map_locations=[normal.location(2, 20)], access_rules=['$canJump'], sections=[
        Section('Red Vase on Alcove 1', visibility_rules=['logic_equipment'], location_id=46),
        Section('Red Vase on Alcove 2', visibility_rules=['logic_full'], location_id=47),
    ]),
    normal.simple_location('Red Vase on Alcove 3', 3, 19, access_rules=['$canJump'], visibility_rules=['logic_full'], location_id=48),
    normal.simple_location('Red Vase on Alcove 6', 5, 17, access_rules=['$canJump'], visibility_rules=['logic_full'], location_id=50),
    normal.simple_location('Inner Chapel Doorway Roof', 8, 16, visibility_rules=['logic_equipment'], location_id=51),
    normal.simple_location('Tower 1 - Top Item', 12, 7, visibility_rules=['logic_equipment'], location_id=52),
    normal.simple_location('Tower 1 - Yellow Vase', 13, 8, visibility_rules=['logic_full'], location_id=53),
    normal.simple_location('Tower 1 - Red Vase', 12, 8, visibility_rules=['logic_full'], location_id=54),
    normal.simple_location('Tower 2 - Top Item', 17, 6, visibility_rules=['logic_full'], location_id=55),
    normal.simple_location('Tower 3 - Top Item', 25, 5, visibility_rules=['logic_equipment'], location_id=56),
    normal.simple_location('Tower 3 - Red Vase', 25, 6, visibility_rules=['logic_full'], location_id=57),
    # Technically in Colosseum but on the other side of the back door from Chapel!
    normal.simple_location('Next to Royal Chapel Passage', 12, 17, visibility_rules=['logic_equipment'], location_id=4),
])

# Underground Caverns
caverns = Area('Underground Caverns', children=[
    # Upper Caverns needs flight if entering from the back door from the start.
    Area('Upper Caverns', access_rules=['jewelofopen', 'open_no4,$canFly'], children=[
        normal.simple_location('Red Vase on Ledge Next to Marble Gallery', 37, 21, access_rules=['$canJump'],
                               visibility_rules=['logic_full'], location_id=129),
        normal.simple_location('Wooden Stand Close to Stairway', 34, 22, visibility_rules=['logic_full'], location_id=122),
        normal.simple_location('Middle of Stairway Room', 35, 27, visibility_rules=['logic_full'], location_id=123),
        normal.simple_location('Breakable Wall Close to Stairway', 33, 22, visibility_rules=['logic_equipment'], location_id=131),
        normal.simple_location('Bottom of Stairway', 36, 31, visibility_rules=['logic_full'], location_id=132),
        normal.simple_location('Alcove Next to Drowned Guards', 35, 32, visibility_rules=['logic_full'], location_id=147),
        Location('Caverns Entrance', map_locations=[normal.location(36, 32)], sections=[
            Section('Below Stairway', visibility_rules=['logic_full'], location_id=146),
            Section('Air Pocket Item', visibility_rules=['logic_equipment'], location_id=155),
        ]),
        Location('Underwater', map_locations=[normal.location(28, 33)], access_rules=['holysymbol'], visibility_rules=['logic_full'], sections=[
            Section('Top Underwater Item', location_id=125),
            Section('Bottom Underwater Item', location_id=126),
        ]),
        normal.simple_location('Underwater Stream', 23, 32, visibility_rules=['logic_full'], location_id=150),
        normal.simple_location('Top Left Room From Waterfall', 20, 32, access_rules=['leapstone', '$canFly', '$canDash'],
                               visibility_rules=['logic_full'], location_id=128),
        Location('Below Wooden Bridge', map_locations=[normal.location(27, 32)], access_rules=['leapstone', '$canFly', '$canDash'],
                 visibility_rules=['logic_full'], sections=[
            Section('Left Item', location_id=148),
            Section('Right Item', location_id=149),
        ]),
        Area('Succubus Side', access_rules=['$canFly'], children=[
            normal.simple_location('First Red Vase', 41, 24, visibility_rules=['logic_full'], location_id=133),
            Location('Red Vases', map_locations=[normal.location(42, 27.5)], visibility_rules=['logic_full'], sections=[
                Section('Red Vases', location_id=[134, 135, 136, 137, 138]),
            ]),
            normal.simple_location('Succubus Item', 43, 28, visibility_rules=['logic_relic_prog'], location_id=130),
        ]),
        Area('Scylla Area', children=[
            normal.simple_location('Scylla Item', 38, 33, visibility_rules=['logic_guarded'], location_id=124),
            normal.simple_location('Right Item', 43, 34, visibility_rules=['logic_full'], location_id=139),
            normal.simple_location('Left Item', 41, 34, visibility_rules=['logic_full'], location_id=140),
            normal.simple_location('Red Vase', 43, 33, visibility_rules=['logic_full'], location_id=141),
        ]),
        Area('Ice Area', children=[
            normal.simple_location('Underwater Item 1', 38, 37, visibility_rules=['logic_equipment'], location_id=143),
            normal.simple_location('Underwater Item 2', 40, 37, visibility_rules=['logic_full'], location_id=144),
            normal.simple_location('On Alcove', 43, 36, access_rules=['mermanstatue', '$canJump'],
                                   visibility_rules=['logic_equipment'], location_id=142),
            normal.simple_location('Underwater Item 3', 50, 37, access_rules=['mermanstatue'],
                                   visibility_rules=['logic_full'], location_id=145),
            normal.simple_location('After Ferryman', 53, 36, access_rules=['mermanstatue'],
                                   visibility_rules=['logic_relic_prog'], location_id=156),
        ]),
        normal.simple_location('Alcove Behind Waterfall', 22, 34, access_rules=['$canJump'], visibility_rules=['logic_equipment'], location_id=151),
        normal.simple_location('Waterfall Upper Item', 21, 35, access_rules=['$canJump'], visibility_rules=['logic_full'], location_id=152),
    ]),
    Area('Lower Caverns', access_rules=['jewelofopen', 'open_no4'], children=[
        normal.simple_location('Waterfall Bottom Item', 21, 37, access_rules=['$canJump'], visibility_rules=['logic_full'], location_id=153),
        normal.simple_location('Hidden Room Behind Waterfall', 23, 37, visibility_rules=['logic_full'], location_id=127),
        normal.simple_location('Next to Castle Entrance Passage', 15, 36, visibility_rules=['logic_full'], location_id=154),
        # Technically in Entrance but on the other side of the back door from Caverns!
        normal.simple_location('By Underground Caverns Bottom Exit', 12, 36, visibility_rules=['logic_full'], location_id=114),
        normal.simple_location('After Ferryman', 6, 37, visibility_rules=['logic_relic_prog'], location_id=157),
    ]),
])

# Abandoned Mine
mine = Area('Abandoned Mine', access_rules=[
        '@Underground Caverns/Upper Caverns/Below Wooden Bridge',
    ], children=[
    Area('Behind Demon Button', access_rules=['demoncard'], children=[
        Location('Behind Breakable Wall', map_locations=[normal.location(34, 36)], visibility_rules=['logic_full'], sections=[
            Section('Behind Breakable Wall', location_id=[29, 35, 36, 37, 38, 39]),
        ]),
        Location('Demon Side', map_locations=[normal.location(35, 36)], sections=[
            Section('Item on the Floor', visibility_rules=['logic_equipment'], location_id=31),
            Section('Item on Breakable Wall', visibility_rules=['logic_full'], location_id=40),
        ]),
    ]),
    Location('Bottom', map_locations=[normal.location(29, 43)], sections=[
        Section('Left Item', visibility_rules=['logic_equipment'], location_id=32),
        Section('Right Item', visibility_rules=['logic_full'], location_id=30),
    ]),
    Location('Bottom Descent', map_locations=[normal.location(30, 41)], sections=[
        Section('Bottom Descent', visibility_rules=['logic_full'], location_id=[33, 34]),
    ]),
    normal.simple_location('Middle Descent Left Room', 27, 39, visibility_rules=['logic_relic_prog'], location_id=41),
])

# Catacombs
catacombs = Area('Catacombs', access_rules=['@Abandoned Mine'], children=[
    Area('Catacombs Upper', children=[
        Location('After Save Point', map_locations=[normal.location(26, 45)], sections=[
            Section('Breakable Wall', visibility_rules=['logic_full'], location_id=9),
            Section('On Floor', visibility_rules=['logic_equipment'], location_id=16),
        ]),
        normal.simple_location('Above Discus Lord Breakable Wall Room', 22, 45, access_rules=['$canHighJump'],
                               visibility_rules=['logic_equipment'], location_id=10),
    ]),
    Area('Catacombs Bottom', children=[
        normal.simple_location('After Save Point', 21, 45, visibility_rules=['logic_equipment'], location_id=11),
        normal.simple_location('After Granfaloon', 15, 45, visibility_rules=['logic_guarded'], location_id=12),
        Location('Above Discus Lord', map_locations=[normal.location(24, 45)], access_rules=['$canHighJump'], visibility_rules=['logic_full'], sections=[
            Section('Red Vase 1', location_id=15),
            Section('Red Vase 2', location_id=14),
        ]),
        Location('After Crypt', map_locations=[normal.location(30, 46)], visibility_rules=['logic_full'], sections=[
            Section('Left Item', location_id=17),
            Section('Right Item', location_id=18),
        ]),
        Location('Sarcophagus', map_locations=[normal.location(31.5, 46)], visibility_rules=['logic_full'], sections=[
            Section('Sarcophagus', location_id=[25, 26, 27, 28]),
        ]),
    ]),
    Area('After Dark Spiked Area', access_rules=['soulofbat,echoofbat', 'spikebreaker,$canJump'], children=[
        Location('Red Vases', map_locations=[normal.location(46, 45)], visibility_rules=['logic_full'], sections=[
            Section('Red Vases', location_id=[19, 20, 21, 22]),
        ]),
        normal.simple_location('Bottom Right Item', 46, 46, visibility_rules=['logic_full'], location_id=23),
        Location('Spike Breaker Room', map_locations=[normal.location(39, 46)], sections=[
            Section('Bottom Left Breakable', visibility_rules=['logic_full'], location_id=13),
            Section('Bottom Left Item', visibility_rules=['logic_relic_prog'], location_id=24),
        ]),
    ]),
])

# Olrox's Quarters
olrox = Area("Olrox's Quarters", access_rules=['open_are,jewelofopen', '$canJump'], children=[
    Area('Front Quarters', access_rules=['$canJump', 'open_are,@Royal Chapel'], children=[
        Location('Room Behind Breakable Wall', map_locations=[normal.location(30, 17)], sections=[
            Section('Vase 1', visibility_rules=['logic_full'], location_id=100),
            Section('Vase 2', visibility_rules=['logic_full'], location_id=99),
            Section('Vase 3', visibility_rules=['logic_equipment'], location_id=98),
        ]),
        normal.simple_location('Ascent Shaft Red Vase 1', 33, 15, access_rules=['$canHighJump'], visibility_rules=['logic_full'], location_id=101),
        normal.simple_location('Ascent Shaft Red Vase 2', 33, 14, access_rules=['$canFly'], visibility_rules=['logic_full'], location_id=102),
        normal.simple_location('Ascent Shaft Red Vase 3', 33, 12, access_rules=['$canFly'], visibility_rules=['logic_full'], location_id=103),
        normal.simple_location('Ledge Before Drop to Courtyard', 28, 10, access_rules=['$canFly'], visibility_rules=['logic_equipment'], location_id=104),
    ]),
    Area('Back Quarters', access_rules=['$canFly'], children=[
        normal.simple_location('On Wooden Display', 19, 14, visibility_rules=['logic_full'], location_id=97),
        normal.simple_location('Hole Before Olrox', 20, 11, access_rules=['$canFly'], visibility_rules=['logic_full'], location_id=105),
        normal.simple_location('Right Room', 31, 13, access_rules=['$canFly'], visibility_rules=['logic_equipment'], location_id=106),
        normal.simple_location('After Olrox', 14, 11, access_rules=['$canFly,$canTransform'], visibility_rules=['logic_relic_prog'], location_id=107),
        normal.simple_location('Hidden Attic', 18, 13, access_rules=['$canHighJump'], visibility_rules=['logic_relic_prog'], location_id=108),
    ]),
])

# Colosseum
colosseum = Area('Colosseum', access_rules=['open_are,jewelofopen', '$canJump'], children=[
    normal.simple_location('Second Part - Bottom Right Room', 24, 19, visibility_rules=['logic_full'], location_id=1),
    normal.simple_location('First Part - Bottom Left Room', 11, 19, visibility_rules=['logic_equipment'], location_id=2),
    normal.simple_location('Second Part - Bottom Left Room', 18, 19, visibility_rules=['logic_equipment'], location_id=3),
    normal.simple_location('Before Minotaurus & Werewolf', 16, 17, visibility_rules=['logic_full'], location_id=5),
    normal.simple_location('First Part - Bottom Right Room', 17, 19, visibility_rules=['logic_full'], location_id=6),
    normal.simple_location('Attic', 17, 15, access_rules=['$canHighJump'], visibility_rules=['logic_full'], location_id=7),
    normal.simple_location('Behind Mist Crate', 19, 17, visibility_rules=['logic_relic_prog'], location_id=8),
])

# Clock Tower
clock_tower = Area('Clock Tower', access_rules=['$canJump'], children=[
    Location('Bellow Broken Bridge', map_locations=[normal.location(53, 9)], visibility_rules=['logic_full'], sections=[
        Section('Item 1', location_id=170),
        Section('Item 2', location_id=169),
    ]),
    Location('On Top of Column', map_locations=[normal.location(52, 8)], access_rules=['$canHighJump'], sections=[
        Section('Item 1', visibility_rules=['logic_full'], location_id=176),
        Section('Item 2', visibility_rules=['logic_equipment'], location_id=175),
        Section('Item 3', visibility_rules=['logic_full'], location_id=177),
    ]),
    Location('Rotating Gears Puzzle Room', map_locations=[normal.location(47, 9)], sections=[
        Section('Item 1', visibility_rules=['logic_full'], location_id=171),
        Section('Item 2', visibility_rules=['logic_equipment'], location_id=172),
        Section('Item 3', visibility_rules=['logic_full'], location_id=173),
    ]),
    normal.simple_location('Behind Breakable Wall Close to Bronze Statue', 40, 6, visibility_rules=['logic_full'], location_id=174),
    normal.simple_location('Gears Puzzle Room Breakable Wall Room Left Item', 48, 4, visibility_rules=['logic_full'], location_id=178),
    normal.simple_location('Gears Puzzle Room Breakable Wall Room Right Item', 50, 4, visibility_rules=['logic_full'], location_id=179),
    normal.simple_location('After Rotating Gears Behind Breakable Wall', 46, 5, visibility_rules=['logic_full'], location_id=181),
    Location('Before Karasuman Breakable Wall', map_locations=[normal.location(40, 5)], visibility_rules=['logic_full'], sections=[
        Section('Item 1', location_id=182),
        Section('Item 2', location_id=180),
        Section('Item 3', location_id=183),
    ]),
    normal.simple_location('Top Right Room in Open Area', 57, 6, access_rules=['$canFly'], visibility_rules=['logic_relic_prog'], location_id=184),
])

# Castle Keep
keep = Area('Castle Keep', children=[
    Location('Open Area Bottom Left', map_locations=[normal.location(29, 6)], access_rules=['$canJump', 'jewelofopen'], sections=[
        Section('On Ledge', visibility_rules=['logic_full'], location_id=185),
        Section('On Ledge Breakable Wall', visibility_rules=['logic_full'], location_id=186),
        Section('Floor Item', visibility_rules=['logic_relic_prog'], location_id=203),
    ]),
    Area('Main Keep', access_rules=['$canJump'], children=[
        Location('Open Area Top Left Alcove', map_locations=[normal.location(29, 4)], access_rules=['$canFly'], sections=[
            Section('Breakable Wall', visibility_rules=['logic_full'], location_id=187),
            Section('Floor Item', visibility_rules=['logic_relic_prog'], location_id=204),
        ]),
        normal.simple_location('Top Right Room by Dual Moving Platforms', 37, 6, visibility_rules=['logic_full'], location_id=188),
        normal.simple_location('Attic by Elevator Surround by Torches', 37, 3, visibility_rules=['logic_equipment'], location_id=197),
        normal.simple_location('Red Vase Before Richter', 33, 3, access_rules=['$canFly'], visibility_rules=['logic_full'], location_id=202),
        Location('Hidden Stair Room', map_locations=[normal.location(32, 1)], access_rules=['$canFly'], sections=[
            Section('Left Statue 1', visibility_rules=['logic_full'], location_id=189),
            Section('Left Statue 2', visibility_rules=['logic_full'], location_id=190),
            Section('Left Yellow Vase 1', visibility_rules=['logic_full'], location_id=191),
            Section('Left Yellow Vase 2', visibility_rules=['logic_full'], location_id=192),
            Section('Right Yellow Vase 1', visibility_rules=['logic_full'], location_id=193),
            Section('Right Yellow Vase 2', visibility_rules=['logic_full'], location_id=194),
            Section('Right Statue 1', visibility_rules=['logic_full'], location_id=195),
            Section('Right Statue 2', visibility_rules=['logic_equipment'], location_id=196),
        ]),
        Location('Open Area Top Right Room', map_locations=[normal.location(36.5, 1)], access_rules=['$canFly'], sections=[
            Section('Items 1-4', visibility_rules=['logic_full'], location_id=[198, 199, 200, 201]),
            Section('Item 5', visibility_rules=['logic_relic_prog'], location_id=205),
        ]),
    ]),
])

# *** Inverted castle

# Reverse Entrance
reverse_entrance = Area("Reverse Entrance", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Middle Room in Open Area Before Main Corridor", 42, 12, visibility_rules=['logic_full'], location_id=310),
    inverted.simple_location("Room by Nova Skeleton on the Ledge", 41, 14, visibility_rules=['logic_equipment'], location_id=311),
    Location("Wolf-Bat Secret Room", map_locations=[inverted.location(51, 10)], access_rules=['soulofbat,soulofwolf'], sections=[
        Section("Left Item", visibility_rules=['logic_full'], location_id=306),
        Section("Middle Item", visibility_rules=['logic_full'], location_id=307),
        Section("Right Item", visibility_rules=['logic_equipment'], location_id=308),
    ]),
    inverted.simple_location("Bellow Stone Pedestal", 42, 15, visibility_rules=['logic_full'], location_id=305),
    inverted.simple_location("Hole in Main Corridor Back Item", 56, 13, visibility_rules=['logic_full'], location_id=309),
    Location("Main Gate Bottom", map_locations=[inverted.location(58.5, 13)], visibility_rules=['logic_full'], sections=[
        Section("Left Item", location_id=302),
        Section("Right Item", location_id=303),
    ]),
    inverted.simple_location("Breakable Big Rock in Main Corridor", 49, 11, visibility_rules=['logic_full'], location_id=312),
    inverted.simple_location("Breakable Ledge on Main Corridor", 42, 11, visibility_rules=['logic_full'], location_id=304),
])

# Necromancy Laboratory
necromancy_lab = Area("Necromancy Laboratory", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Globe in the Room With Lesser Demons and Ctulhu", 47, 15, visibility_rules=['logic_full'], location_id=349),
    inverted.simple_location("Breakable Wall on Tunnel Right of Elevator Shaft", 50, 17, visibility_rules=['logic_full'], location_id=341),
    inverted.simple_location("Bottom Room From Spike Traps", 51, 22, visibility_rules=['logic_full'], location_id=342),
    inverted.simple_location("Breakable Ceiling on Tunnel Right of Elevator Shaft", 49, 15, visibility_rules=['logic_equipment'], location_id=345),
    inverted.simple_location("Middle Room on Elevator Shaft", 45, 20, visibility_rules=['logic_equipment'], location_id=343),
    inverted.simple_location("Blue Flame in Room With Lesser and Fire Demons", 48, 16, visibility_rules=['logic_full'], location_id=344),
    inverted.simple_location("Globe in Bitterfly Room", 42, 24, visibility_rules=['logic_full'], location_id=347),
    inverted.simple_location("Hole in Room With Lesser and Fire Demons", 46, 18, visibility_rules=['logic_full'], location_id=346),
    inverted.simple_location("Bottom Left Room From Beezelbub", 48, 24, visibility_rules=['logic_guarded'], location_id=348),
])

# Black Marble Gallery
black_marble_gallery = Area("Black Marble Gallery", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Corridor to Entrance Item on Spike Trap", 35, 17, visibility_rules=['logic_full'], location_id=267),
    Location("Left Clock", map_locations=[inverted.location(27.5, 26)], visibility_rules=['logic_full'], sections=[
        Section("First Room Item on Left", location_id=274),
        Section("First Room Item on Right", location_id=275),
        Section("Second Room Item on Left", location_id=272),
        Section("Second Room Item on Right", location_id=273),
    ]),
    inverted.simple_location("Middle Clock Right Item", 31, 28, visibility_rules=['logic_full'], location_id=270),
    inverted.simple_location("Middle Clock Left Item", 27, 28, visibility_rules=['logic_full'], location_id=271),
    inverted.simple_location("Hole on the Ceiling", 17, 25, visibility_rules=['logic_full'], location_id=277),
    inverted.simple_location("Behind Magic Blue Door", 15, 27, access_rules=['jewelofopen'], visibility_rules=['logic_full'], location_id=276),
    inverted.simple_location("Ascend to Entrance Item on Floor 1", 36, 22, visibility_rules=['logic_full'], location_id=269),
    inverted.simple_location("Ascend to Entrance Item on Floor 2", 36, 20, visibility_rules=['logic_full'], location_id=268),
    Area("Inside Clock", access_rules=['$canFightDracula'], children=[
        inverted.simple_location("Item Inside the Clock", 28, 24, visibility_rules=['logic_full'], location_id=278),
        inverted.simple_location("Kill Dracula", 29, 20),
    ]),
])

# Reverse Outer Wall
reverse_outer_wall = Area("Reverse Outer Wall", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Mist Crate Room", map_locations=[inverted.location(2, 24)], access_rules=['formofmist'], sections=[
        Section("Left Item", visibility_rules=['logic_full'], location_id=280),
        Section("Right Item", visibility_rules=['logic_equipment'], location_id=281),
    ]),
    inverted.simple_location("Bottom Red Vase Near Elevator Machinery", 1, 36, visibility_rules=['logic_full'], location_id=286),
    inverted.simple_location("Yellow Vase on Alcove Near Creature", 0, 27, visibility_rules=['logic_full'], location_id=283),
    inverted.simple_location("Item on the Floor Near Creature", 2, 28, visibility_rules=['logic_full'], location_id=284),
    inverted.simple_location("Red Vase Near Creature", 0, 28, visibility_rules=['logic_full'], location_id=285),
    inverted.simple_location("Red Vase Near Door to BMG", 0, 26, visibility_rules=['logic_full'], location_id=282),
    inverted.simple_location("Breakable Wall on Room Below Mist Crate", 2, 25, visibility_rules=['logic_full'], location_id=287),
    inverted.simple_location("Creature Kill Item", 3.5, 28, visibility_rules=['logic_relic_prog'], location_id=288),
    inverted.simple_location("Item at the Top", 0, 23, visibility_rules=['logic_full'], location_id=279),
])

# Forbidden Library
reverse_library = Area("Forbidden Library", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Bottom Left Room Green Candle", 12, 33, visibility_rules=['logic_full'], location_id=264),
    inverted.simple_location("Bottom Left Room Behind Bookshelf", 11, 33, visibility_rules=['logic_equipment'], location_id=265),
    Location("Bottom Right Room", map_locations=[inverted.location(9, 33)], visibility_rules=['logic_full'], sections=[
        Section("Left Item", location_id=261),
        Section("Middle Item", location_id=262),
        Section("Right Item", location_id=263),
    ]),
    inverted.simple_location("Behind Mist Crate", 13, 30, access_rules=['formofmist'], visibility_rules=['logic_equipment'], location_id=266),
    Location("Inner Study", map_locations=[inverted.location(12, 31)], visibility_rules=['logic_full'], sections=[
        Section('Red Vase', location_id=258),
        Section('Left Statue', location_id=259),
        Section('Right Statue', location_id=260),
    ]),
])

# Anti-Chapel
anti_chapel = Area("Anti-Chapel", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Red Vase Alcove 2", 55, 28, visibility_rules=['logic_full'], location_id=247),
    inverted.simple_location("Red Vase Alcove 3", 55, 27, visibility_rules=['logic_full'], location_id=242),
    inverted.simple_location("Bottom Yellow Vase", 52, 30, visibility_rules=['logic_full'], location_id=241),
    inverted.simple_location("After Spiked Tunnel", 52, 36, access_rules=[
        'formofmist,spikebreaker',
        'formofmist,powerofmist',
    ], visibility_rules=['logic_equipment'], location_id=255),
    inverted.simple_location("Red Vase at Top", 59, 24, visibility_rules=['logic_full'], location_id=243),
    inverted.simple_location("Red Vase Alcove 5", 57, 26, visibility_rules=['logic_full'], location_id=245),
    inverted.simple_location("Red Vase Alcove 6", 57, 25, visibility_rules=['logic_full'], location_id=244),
    inverted.simple_location("Next to Upper Save Point", 58, 23, visibility_rules=['logic_full'], location_id=256),
    inverted.simple_location("Red Vase Alcove 4", 56, 27, visibility_rules=['logic_full'], location_id=246),
    inverted.simple_location("Red Vase Alcove 1", 54, 29, visibility_rules=['logic_full'], location_id=248),
    inverted.simple_location("Tower 3 - Bottom Item", 47, 39, visibility_rules=['logic_full'], location_id=249),
    inverted.simple_location("Tower 3 - Yellow Vase", 46, 38, visibility_rules=['logic_full'], location_id=250),
    inverted.simple_location("Tower 3 - Red Vase", 47, 37, visibility_rules=['logic_full'], location_id=251),
    inverted.simple_location("Tower 2 - Bottom Item", 42, 40, visibility_rules=['logic_equipment'], location_id=252),
    inverted.simple_location("Tower 1 - Bottom Item", 34, 41, visibility_rules=['logic_full'], location_id=253),
    inverted.simple_location("Tower 1 - Red Vase", 34, 40, visibility_rules=['logic_full'], location_id=254),
    inverted.simple_location("Medusa Kill Item", 37.5, 38, visibility_rules=['logic_relic_prog'], location_id=257),
])

# Reverse Caverns
reverse_caverns = Area("Reverse Caverns", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Stairs - Bottom Item", 25, 24, visibility_rules=['logic_full'], location_id=325),
    inverted.simple_location("Stairs - Middle Room", 24, 19, visibility_rules=['logic_equipment'], location_id=324),
    inverted.simple_location("Bottom Area Right Room", 21, 13, visibility_rules=['logic_guarded'], location_id=336),
    Location("Underwater", map_locations=[inverted.location(31, 13)], access_rules=['gravityboots'], visibility_rules=['logic_full'], sections=[
        Section('Top Item', location_id=319),
        Section('Bottom Item', location_id=321),
    ]),
    inverted.simple_location("Behind Waterfall Room", 36, 9, access_rules=[
        'soulofbat',
        'gravityboots,leapstone',
    ], visibility_rules=['logic_equipment'], location_id=339),
    inverted.simple_location("Waterfall - Bottom Right Room", 39, 14, visibility_rules=['logic_equipment'], location_id=317),
    inverted.simple_location("Red Vase Near Exit", 22, 25, visibility_rules=['logic_full'], location_id=327),
    inverted.simple_location("Bottom Item Behind Breakable Wall", 26, 24, visibility_rules=['logic_equipment'], location_id=326),
    inverted.simple_location("Item on Air Pocket", 23, 13, access_rules=['gravityboots,holysymbol'],
                             visibility_rules=['logic_full'], location_id=320),
    inverted.simple_location("First Red Vase", 18, 22, visibility_rules=['logic_full'], location_id=328),
    Location("Succubus Side", map_locations=[inverted.location(17, 18.5)], visibility_rules=['logic_full'], sections=[
        Section("Red Vases", location_id=[329, 330, 331, 332, 333]),
    ]),
    inverted.simple_location("Item on Alcove", 18, 12, visibility_rules=['logic_full'], location_id=334),
    inverted.simple_location("Bottom Area Left Red Vase", 16, 13, visibility_rules=['logic_full'], location_id=335),
    inverted.simple_location("Inside Cave", 16, 10, visibility_rules=['logic_full'], location_id=338),
    inverted.simple_location("Underwater Alcove Item", 19, 9, visibility_rules=['logic_full'], location_id=337),
    inverted.simple_location("Alcove Near Water Leak", 24, 14, visibility_rules=['logic_full'], location_id=322),
    inverted.simple_location("Near Stairs Hole", 23, 14, visibility_rules=['logic_full'], location_id=323),
    inverted.simple_location("Underwater Stream", 36, 14, access_rules=['leapstone', 'soulofbat'],
                             visibility_rules=['logic_full'], location_id=318),
    inverted.simple_location("Waterfall - Alcove 1", 38, 10, visibility_rules=['logic_full'], location_id=315),
    inverted.simple_location("Waterfall - Alcove 2", 38, 11, visibility_rules=['logic_full'], location_id=316),
    inverted.simple_location("Near Exit", 44, 10, visibility_rules=['logic_full'], location_id=314),
    inverted.simple_location("Ice Area - At End", 6, 10, visibility_rules=['logic_relic_prog'], location_id=340),
    inverted.simple_location("End of Cavern", 53, 9, visibility_rules=['logic_equipment'], location_id=313),
])

# Cave
cave = Area("Cave", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Breakable Wall Room", map_locations=[inverted.location(25, 10)], access_rules=['demoncard'], visibility_rules=['logic_full'], sections=[
        Section("Left Item", location_id=233),
        Section("Right Item", location_id=234),
    ]),
    inverted.simple_location("Upper Right Room Left Item", 24, 10, access_rules=['demoncard'], visibility_rules=['logic_full'], location_id=236),
    inverted.simple_location("Upper Right Room Right Item", 30, 3, visibility_rules=['logic_full'], location_id=237),
    inverted.simple_location("Upper Ascent", 29, 5, visibility_rules=['logic_full'], location_id=[238, 239]),
    inverted.simple_location("Middle Ascent Right Item", 32, 7, visibility_rules=['logic_equipment'], location_id=235),
    inverted.simple_location("Death Item", 30.5, 11, visibility_rules=['logic_relic_prog'], location_id=240),
])

# Floating Catacombs
floating_catacombs = Area("Floating Catacombs", access_rules=['$canAccessInvertedCastle'], children=[
    Location("After Save Point", map_locations=[inverted.location(33, 1)], visibility_rules=['logic_full'], sections=[
        Section("Item", location_id=214),
        Section("Breakable Wall", location_id=215),
    ]),
    inverted.simple_location("After Crypt Breakable Wall Room", 37, 1, visibility_rules=['logic_equipment'], location_id=227),
    inverted.simple_location("Before Galamoth Save Point", 38, 1, visibility_rules=['logic_equipment'], location_id=228),
    Location("After Galamoth", map_locations=[inverted.location(44, 0)], visibility_rules=['logic_full'], sections=[
        Section("Left Item", location_id=229),
        Section("Right Item", location_id=230),
    ]),
    Location("After Galamoth Deeper Room", map_locations=[inverted.location(44, 1)], sections=[
        Section("Right Item", visibility_rules=['logic_full'], location_id=231),
        Section("Left Item", visibility_rules=['logic_relic_prog'], location_id=232),
    ]),
    Location("After Crypt Cave", map_locations=[inverted.location(35, 1)], visibility_rules=['logic_full'], sections=[
        Section("Upper Red Vase", location_id=225),
        Section("Bottom Red Vase", location_id=226),
    ]),
    Location("Start of Crypt", map_locations=[inverted.location(29, 0)], visibility_rules=['logic_full'], sections=[
        Section("Left Item", location_id=223),
        Section("Right Item)", location_id=224),
    ]),
    Area('After Spike Tunnel', access_rules=[
        'soulofbat',
        'formofmist,powerofmist',
        'spikebreaker,leapstone',
        'spikebreaker,gravityboots',
    ], children=[
        Location("Spike Hallway", map_locations=[inverted.location(13, 1)], visibility_rules=['logic_full'], sections=[
            Section("Top Left Vase", location_id=216),
            Section("Top Right Vase", location_id=217),
            Section("Bottom Left Vase", location_id=218),
            Section("Bottom Right Vase", location_id=219),
        ]),
        inverted.simple_location("Deep Left Item", 13, 0, visibility_rules=['logic_full'], location_id=220),
        Location("Deep Right", map_locations=[inverted.location(20, 0)], visibility_rules=['logic_full'], sections=[
            Section("Item", location_id=221),
            Section("Breakable Wall Item", location_id=222),
        ]),
    ]),
])

# Death Wing's Lair
death_wing = Area("Death Wing's Lair", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Bellow Wooden Pedestal", 40, 32, visibility_rules=['logic_full'], location_id=297),
    Location("Room Behind Breakable Wall", map_locations=[inverted.location(29, 29)], sections=[
        Section("Left Red Vase", visibility_rules=['logic_equipment'], location_id=289),
        Section("Middle Red Vase", visibility_rules=['logic_full'], location_id=290),
        Section("Right Red Vase", visibility_rules=['logic_full'], location_id=291),
    ]),
    Location("Shaft", map_locations=[inverted.location(26, 32)], visibility_rules=['logic_full'], sections=[
        Section("Top Red Vase", location_id=292),
        Section("Middle Red Vase", location_id=293),
    ]),
    inverted.simple_location("Bottom Red Vase on Shaft", 26, 34, visibility_rules=['logic_full'], location_id=294),
    inverted.simple_location("Red Vase Next to Path to Courtyard", 31, 36, visibility_rules=['logic_full'], location_id=295),
    inverted.simple_location("Attic Before Akmodan II", 39, 35, visibility_rules=['logic_full'], location_id=299),
    inverted.simple_location("Top Left Room", 28, 33, visibility_rules=['logic_equipment'], location_id=296),
    inverted.simple_location("After Akmodan II", 45, 35, access_rules=['$canTransform'], visibility_rules=['logic_full'], location_id=300),
    inverted.simple_location("Breakable Floor Room", 41, 33, visibility_rules=['logic_full'], location_id=298),
    inverted.simple_location("Akmodan II Item", 41.5, 34.5, visibility_rules=['logic_relic_prog'], location_id=301),
])

# Reverse Colosseum
reverse_colosseum = Area("Reverse Colosseum", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Breakable Floor Room", 42, 31, visibility_rules=['logic_equipment'], location_id=206),
    inverted.simple_location("Right Part - Top Right Room", 48, 27, visibility_rules=['logic_full'], location_id=207),
    inverted.simple_location("Right Part - Top Left Room", 42, 27, visibility_rules=['logic_full'], location_id=208),
    inverted.simple_location("Left Part - Top Right Room", 41, 27, visibility_rules=['logic_equipment'], location_id=209),
    inverted.simple_location("Left Part - Top Left Room", 35, 27, visibility_rules=['logic_full'], location_id=210),
    Location("Left Part", map_locations=[inverted.location(38, 28)], visibility_rules=['logic_full'], sections=[
        Section('Left Item on Floor', location_id=211),
        Section('Middle Item on Floor', location_id=212),
        Section('Right Item on Floor', location_id=213),
    ]),
    inverted.simple_location("Trio Item", 41.5, 29, visibility_rules=['logic_relic_prog'], location_id=386),
])

# Reverse Clock Tower
reverse_clock_tower = Area("Reverse Clock Tower", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Above Stone Bridge", map_locations=[inverted.location(6, 37)], visibility_rules=['logic_full'], sections=[
        Section("Left Item", location_id=350),
        Section("Right Item", location_id=351),
    ]),
    Location("Columns", map_locations=[inverted.location(7, 38)], sections=[
        Section("Left Column", visibility_rules=['logic_full'], location_id=352),
        Section("Middle Column", visibility_rules=['logic_equipment'], location_id=353),
        Section("Right Column", visibility_rules=['logic_full'], location_id=354),
    ]),
    inverted.simple_location("Bottom Left Room", 2, 40, visibility_rules=['logic_equipment'], location_id=355),
    Location("Gears Puzzle Room", map_locations=[inverted.location(12, 37)], sections=[
        Section("Left Item", visibility_rules=['logic_full'], location_id=356),
        Section("Middle Item", visibility_rules=['logic_full'], location_id=357),
        Section("Right Item", visibility_rules=['logic_equipment'], location_id=358),
    ]),
    inverted.simple_location("Behind Breakable Wall Next to Bronze Statue", 19, 40, visibility_rules=['logic_equipment'], location_id=361),
    inverted.simple_location("Room Behind Bottom Left Breakable Wall Left Item", 9, 42, visibility_rules=['logic_full'], location_id=359),
    inverted.simple_location("Room Behind Bottom Left Breakable Wall Right Item", 11, 42, visibility_rules=['logic_full'], location_id=360),
    inverted.simple_location("Breakable Wall Item on Brackets", 13, 40, visibility_rules=['logic_full'], location_id=363),
    Location("Near Darkwing Bat", map_locations=[inverted.location(19, 41)], visibility_rules=['logic_full'], sections=[
        Section("Left Breakable Wall", location_id=365),
        Section("Middle Breakable Wall", location_id=362),
        Section("Right Breakable Wall", location_id=364),
    ]),
    inverted.simple_location("Darkwing Bat Item", 21, 41, visibility_rules=['logic_relic_prog'], location_id=366),
])

# Reverse Castle Keep
reverse_keep = Area("Reverse Castle Keep", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Open Area Top Right", map_locations=[inverted.location(30, 40)], sections=[
        Section("Breakable Wall", visibility_rules=['logic_full'], location_id=367),
        Section("Ledge", visibility_rules=['logic_equipment'], location_id=383),
    ]),
    inverted.simple_location("Open Area Bottom Left Underpass Breakable Wall", 30, 42, visibility_rules=['logic_full'], location_id=368),
    inverted.simple_location("Bottom Left Room on Dual Elevator Area", 22, 40, visibility_rules=['logic_equipment'], location_id=384),
    Location("Bellow Stairs", map_locations=[inverted.location(27, 45)], sections=[
        Section("Left Statue 1", visibility_rules=['logic_full'], location_id=376),
        Section("Left Statue 2", visibility_rules=['logic_equipment'], location_id=377),
        Section("Left Yellow Vase 1", visibility_rules=['logic_full'], location_id=375),
        Section("Left Yellow Vase 2", visibility_rules=['logic_full'], location_id=374),
        Section("Right Yellow Vase 1", visibility_rules=['logic_full'], location_id=373),
        Section("Right Yellow Vase 2", visibility_rules=['logic_full'], location_id=372),
        Section("Right Statue 1", visibility_rules=['logic_full'], location_id=371),
        Section("Right Statue 2", visibility_rules=['logic_equipment'], location_id=370),
    ]),
    inverted.simple_location("Bellow Save Point", 22, 43, visibility_rules=['logic_full'], location_id=385),
    Location("Open Area Bottom Right Room", map_locations=[inverted.location(22.5, 45)], visibility_rules=['logic_full'], sections=[
        Section("Item 1", location_id=378),
        Section("Item 2", location_id=379),
        Section("Item 3", location_id=381),
        Section("Item 4", location_id=380),
        Section("Window Item", location_id=382),
    ]),
    inverted.simple_location("Red Vase After Entering", 27, 43, visibility_rules=['logic_full'], location_id=369),
])

# *** Write out files.
areas = (
    # Normal castle
    (entrance, 'normal/entrance.json'),
    (alchemy_lab, 'normal/alchemy_lab.json'),
    (marble_gallery, 'normal/marble_gallery.json'),
    (outer_wall, 'normal/outer_wall.json'),
    (library, 'normal/library.json'),
    (chapel, 'normal/chapel.json'),
    (caverns, 'normal/caverns.json'),
    (mine, 'normal/mine.json'),
    (catacombs, 'normal/catacombs.json'),
    (olrox, 'normal/olrox.json'),
    (colosseum, 'normal/colosseum.json'),
    (clock_tower, 'normal/clock_tower.json'),
    (keep, 'normal/keep.json'),

    # Inverted castle
    (reverse_entrance, 'inverted/entrance.json'),
    (necromancy_lab, 'inverted/necromancy_lab.json'),
    (black_marble_gallery, 'inverted/black_marble_gallery.json'),
    (reverse_outer_wall, 'inverted/outer_wall.json'),
    (reverse_library, 'inverted/library.json'),
    (anti_chapel, 'inverted/anti_chapel.json'),
    (reverse_caverns, 'inverted/caverns.json'),
    (cave, 'inverted/cave.json'),
    (floating_catacombs, 'inverted/floating_catacombs.json'),
    (death_wing, 'inverted/death_wing.json'),
    (reverse_colosseum, 'inverted/colosseum.json'),
    (reverse_clock_tower, 'inverted/clock_tower.json'),
    (reverse_keep, 'inverted/keep.json'),
)

if __name__ == '__main__':
    # Write out each area to its JSON file.
    for area, filename in areas:
        process_area(area)

        filename = os.path.join('locations', filename)
        with open(filename, 'w') as f:
            f.write(dumps([area], indent=4))
            print(f'Wrote {filename}')

    # Write out location and hosted item mappings.
    lua_file = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'scripts/autotracking/location_mapping.lua')
    with open(lua_file, 'w') as f:
        print("-- Generated by generate_locations.py script.  DO NOT EDIT MANUALLY!\n", file=f)

        # Main locations mapping.
        print("-- Main locations mapping.", file=f)
        print("LOCATIONS_MAPPING = {", file=f)
        for zone in sorted(LOCATIONS_MAPPING.keys()):
            print(f"    -- {zone}", file=f)
            for location_id, code in sorted(LOCATIONS_MAPPING[zone].items()):
                print(f"""    [{location_id}] = "{code}",""", file=f)
            print(file=f)
        print("}\n", file=f)

        # Hosted items mapping.
        print("-- Hosted items mapping for boss kill items.", file=f)
        print("HOSTED_ITEMS = {", file=f)
        for location_id, item in sorted(HOSTED_ITEMS.items()):
            print(f"""    [{location_id}] = "{item}",""", file=f)
        print("}", file=f)
