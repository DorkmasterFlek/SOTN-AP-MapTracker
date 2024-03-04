#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Map tracker locations for Castlevania: Symphony of the Night.

import os
import sys

sys.path.append('../poptrackerlib-py/src')

from poptrackerlib import Map, Area, Location, Section, dumps

normal = Map('normal', scale=20, offset=32)
inverted = Map('inverted', scale=20, offset=32)

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
    prefix += '/' + location.name
    for section in location.sections:
        # Skip the final boss location; it doesn't have an ID.
        if section.name == 'Kill Dracula':
            continue

        code = prefix + '/' + section.name
        zone = prefix.split('/')[0].strip('@')
        LOCATIONS_MAPPING.setdefault(zone, {})
        LOCATIONS_MAPPING[zone][section.location_id] = code

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
    normal.simple_location('Heart Vessel (Above Death)', 17, 34, location_id=127110000),
    normal.simple_location('Life Vessel (Bellow shield potion)', 18, 32, access_rules=['$canJump'], location_id=127110001),
    Location('Hidden Room', map_locations=[normal.location(8, 36)], access_rules=['soulofbat,soulofwolf'], sections=[
        Section('Life Apple (Hidden room)', location_id=127110002),
        Section('Jewel sword', location_id=127110009),
    ]),
    normal.simple_location('Shield Potion', 17, 31, location_id=127110004),
    normal.simple_location('Holy mail', 3, 33, access_rules=['$canFly'], location_id=127110005),
    normal.simple_location('Life Vessel (UC exit)', 12, 36, access_rules=['@Underground Caverns/Lower Caverns'], location_id=127110006),
    normal.simple_location('Heart Vessel (Teleport exit)', 15, 33, location_id=127110007),
    Location('Above Entrance', map_locations=[normal.location(0.5, 33)], access_rules=['$canFly'], sections=[
        Section('Life Vessel (Above entry)', location_id=127110008),
        Section('Power of Wolf', location_id=127113113),
    ]),
    normal.simple_location('Pot Roast', 10, 35, location_id=127113110),
    normal.simple_location('Turkey', 17, 35, location_id=127113111),
    normal.simple_location('Cube of Zoe', 16, 31, location_id=127113112),
])

# Alchemy Laboratory
alchemy_lab = Area('Alchemy Laboratory', children=[
    normal.simple_location('Hide cuirass', 12, 31, location_id=127140000),
    normal.simple_location('Heart Vessel', 9, 29, location_id=127140001),
    normal.simple_location('Cloth cape', 8, 24, location_id=127140002),
    normal.simple_location('Life Vessel', 10, 31, location_id=127140003),
    normal.simple_location('Sunglasses', 14, 26, location_id=127140006),
    normal.simple_location('Resist thunder', 9, 27, location_id=127140007),
    normal.simple_location('Leather shield', 11, 30, location_id=127140008),
    normal.simple_location('Basilard', 14, 29, location_id=127140009),
    normal.simple_location('Potion', 17, 22, location_id=127140010),
    boss_location('Slogra and Gaibon', 'slogragaibon', normal, 8.5, 22.5, location_id=127143140),
    normal.simple_location('Skill of Wolf', 13, 28, access_rules=['$canHighJump'], location_id=127143141),
    normal.simple_location('Bat Card', 11, 22, access_rules=['$canFly'], location_id=127143142),
])

# Marble Gallery
marble_gallery = Area('Marble Gallery', children=[
    normal.simple_location('Life Vessel(Left clock)', 29, 20, access_rules=['$canJump', 'opened_are,jewelofopen'], location_id=127080000),
    Location('Right Clock', map_locations=[normal.location(31.5, 20)], access_rules=['$canJump'], sections=[
        Section('Heart Vessel(Right clock)', location_id=127080002),
        Section('Alucart shield', location_id=127080001),
        Section('Alucart mail', location_id=127080006),
        Section('Alucart sword', location_id=127080007),
    ]),
    Location('Middle Clock', map_locations=[normal.location(28.5, 18)], access_rules=['$canFly'], sections=[
        Section('Life apple(Middle clock)', location_id=127080003),
        Section('Hammer(Middle clock)', location_id=127080004),
        Section('Potion(Middle clock)', location_id=127080005),
    ]),
    Location('Inside Clock', map_locations=[normal.location(31, 22)], access_rules=['silverring,goldring'], sections=[
        Section('Life Vessel(Inside)', location_id=127080008),
        Section('Heart Vessel(Inside)', location_id=127080009),
    ]),
    Location('Under Floor', map_locations=[normal.location(42, 21)], access_rules=['jewelofopen'], sections=[
        Section('Library card(Jewel)', location_id=127080010),
        Section('Attack potion(Jewel)', location_id=127080011),
    ]),
    normal.simple_location('Hammer(Spirit)', 24, 25, access_rules=['$canHighJump'], location_id=127080012),
    normal.simple_location('Str. potion', 24, 23, access_rules=['$canHighJump'], location_id=127080013),
    normal.simple_location('Holy glasses', 30, 26, access_rules=['silverring,goldring'], location_id=127083080),
    normal.simple_location('Spirit Orb', 23, 26, location_id=127083081),
    normal.simple_location('Gravity Boots', 32, 18, access_rules=['$canFly'], location_id=127083082),
])

# Outer Wall
outer_wall = Area('Outer Wall', children=[
    Location('Secret Elevator', map_locations=[normal.location(57, 22)], sections=[
        Section('Jewel knuckles', location_id=127090000),
        Section('Mirror cuirass', location_id=127090001),
    ]),
    normal.simple_location('Heart Vessel', 58, 10, location_id=127090002),
    normal.simple_location('Garnet', 59, 19, access_rules=['$canJump'], location_id=127090003),
    normal.simple_location('Gladius', 57, 18, location_id=127090004),
    normal.simple_location('Life Vessel', 59, 18, location_id=127090005),
    normal.simple_location('Zircon', 59, 20, location_id=127090006),
    normal.simple_location('Pot Roast', 57, 21, location_id=127093090),
    boss_location('Doppleganger 10', 'doppleganger10', normal, 55.5, 18, location_id=127093091),
    normal.simple_location('Soul of Wolf', 59, 13, location_id=127093092),
])

# Long Library
library = Area('Long Library', children=[
    normal.simple_location('Bronze cuirass', 47, 16, location_id=127070004),
    Location('Top Level', map_locations=[normal.location(50, 13)], access_rules=['$canJump'], sections=[
        Section('Potion', location_id=127070008),
        Section('Antivenom', location_id=127070009),
        Section('Faerie Card', location_id=127073075),
    ]),
    normal.simple_location('Faerie Scroll', 57, 13, access_rules=['$canJump'], location_id=127073073),
    normal.simple_location('Jewel of Open', 47, 15, location_id=127073074),
    Area('Back of Library', access_rules=['$canJump'], children=[
        normal.simple_location('Stone mask', 47, 13, location_id=127070001),
        Location('Behind Bookcase', map_locations=[normal.location(48, 13)], sections=[
            Section('Holy rod', location_id=127070002),
            Section('Topaz circlet', location_id=127070010),
        ]),
        Location('Dead End', map_locations=[normal.location(44, 16)], sections=[
            Section('Takemitsu', location_id=127070005),
            Section('Onyx', location_id=127070006),
            Section('Frankfurter', location_id=127070007),
        ]),
        boss_location('Lesser Demon', 'lesserdemon', normal, 43.5, 15, location_id=127073070),
        normal.simple_location('Soul of Bat', 46, 16, access_rules=['mist'], location_id=127073072),
    ]),
])

# Royal Chapel
chapel = Area('Royal Chapel', access_rules=['jewelofopen', '$canJump'], children=[
    Location('Middle of Stairs', map_locations=[normal.location(4, 18)], access_rules=['$canJump'], sections=[
        Section('Ankh of life(Stairs)', location_id=127050000),
        Section('TNT(Stairs)', location_id=127050007),
    ]),
    normal.simple_location('Morningstar', 7, 16, access_rules=['$canJump'], location_id=127050001),
    normal.simple_location('Silver ring', 6, 10, access_rules=['jewelofopen,formofmist,spikebreaker'], location_id=127050002),
    normal.simple_location('Aquamarine(Stairs)', 0, 22, location_id=127050003),
    Location('Bottom of Stairs', map_locations=[normal.location(2, 20)], access_rules=['$canJump'], sections=[
        Section('Mystic pendant', location_id=127050004),
        Section('Magic missile(Stairs)', location_id=127050005),
    ]),
    normal.simple_location('Shuriken(Stairs)', 3, 19, access_rules=['$canJump'], location_id=127050006),
    normal.simple_location('Boomerang(Stairs)', 5, 17, access_rules=['$canJump'], location_id=127050008),
    normal.simple_location('Goggles', 8, 16, location_id=127050009),
    normal.simple_location('Silver plate', 12, 7, location_id=127050010),
    normal.simple_location('Str. potion(Bell)', 13, 8, location_id=127050011),
    normal.simple_location('Life Vessel(Bell)', 12, 8, location_id=127050012),
    normal.simple_location('Zircon', 17, 6, location_id=127050013),
    normal.simple_location('Cutlass', 25, 5, location_id=127050014),
    normal.simple_location('Potion', 25, 6, location_id=127050015),
    boss_location('Hippogryph', 'hippogryph', normal, 21.5, 8, location_id=127053050),
])

# Underground Caverns
caverns = Area('Underground Caverns', children=[
    # Upper Caverns needs flight if entering from the back door from the start.
    Area('Upper Caverns', access_rules=['jewelofopen', 'opened_no4,$canFly'], children=[
        normal.simple_location('Zircon', 37, 21, access_rules=['$canJump'], location_id=127130009),
        normal.simple_location('Heart Vessel(0)', 34, 22, location_id=127130000),
        normal.simple_location('Life Vessel(1)', 35, 27, location_id=127130001),
        normal.simple_location('Bandanna', 33, 22, location_id=127130011),
        normal.simple_location('Shiitake(12)', 36, 31, location_id=127130012),
        Location('Caverns Entrance', map_locations=[normal.location(36, 32)], sections=[
            Section('Toadstool(26)', location_id=127130026),
            Section('Nunchaku', location_id=127130036),
        ]),
        normal.simple_location('Shiitake(27)', 35, 32, location_id=127130027),
        Location('Underwater', map_locations=[normal.location(28, 33)], access_rules=['holysymbol'], sections=[
            Section('Antivenom(Underwater)', location_id=127130004),
            Section('Life Vessel(Underwater)', location_id=127130005),
        ]),
        normal.simple_location('Pentagram', 23, 32, location_id=127130030),
        normal.simple_location('Herald Shield', 20, 32, access_rules=['$canJump', '$canDash'], location_id=127130007),
        Location('Below Bridge', map_locations=[normal.location(27, 32)], access_rules=['$canJump', '$canDash'], sections=[
            Section('Life Vessel(Bellow bridge)', location_id=127130028),
            Section('Heart Vessel(Bellow bridge)', location_id=127130029),
        ]),
        Area('Side Section', access_rules=['$canJump'], children=[
            normal.simple_location('Claymore', 41, 24, location_id=127130013),
            Location('Succubus Approach', map_locations=[normal.location(42, 27.5)], sections=[
                Section('Meal ticket 1(Succubus)', location_id=127130014),
                Section('Meal ticket 2(Succubus)', location_id=127130015),
                Section('Meal ticket 3(Succubus)', location_id=127130016),
                Section('Meal ticket 4(Succubus)', location_id=127130017),
                Section('Moonstone', location_id=127130018),
            ]),
            Location('Succubus', map_locations=[normal.location(43, 28)], sections=[
                Section('Gold Ring', location_id=127130010),
                Section('Succubus kill', hosted_item='succubus', location_id=127133131),
            ]),
        ]),
        normal.simple_location('Crystal cloak', 38, 33, location_id=127130002),
        normal.simple_location('Scimitar', 43, 34, location_id=127130019),
        normal.simple_location('Resist ice', 41, 34, location_id=127130020),
        normal.simple_location('Pot roast', 43, 33, location_id=127130021),
        boss_location("Scylla", "scylla", normal, 39, 33, location_id=127133130),
        normal.simple_location('Knuckle duster(Holy)', 38, 37, location_id=127130023),
        normal.simple_location('Life Vessel(Holy)', 40, 37, location_id=127130024),
        normal.simple_location('Onyx(Holy)', 43, 36, access_rules=['mermanstatue', '$canJump'], location_id=127130022),
        normal.simple_location('Elixir(Holy)', 50, 37, access_rules=['mermanstatue'], location_id=127130025),
        normal.simple_location('Holy Symbol', 53, 36, access_rules=['mermanstatue'], location_id=127133132),
        normal.simple_location('Secret boots', 22, 34, access_rules=['$canJump'], location_id=127130031),
        normal.simple_location('Shiitake(Waterfall)', 21, 35, access_rules=['$canJump'], location_id=127130032),
    ]),
    Area('Lower Caverns', access_rules=['jewelofopen', 'opened_no4'], children=[
        normal.simple_location('Toadstool(Waterfall)', 21, 37, access_rules=['$canJump'], location_id=127130033),
        normal.simple_location('Life Vessel(Behind waterfall)', 23, 37, location_id=127130006),
        normal.simple_location('Shiitake(Near entrance passage)', 15, 36, location_id=127130035),
        normal.simple_location('Merman Statue', 6, 37, location_id=127133133),
    ]),
])

# Abandoned Mine
mine = Area('Abandoned Mine', access_rules=[
        '@Underground Caverns/Upper Caverns,$canJump',
        '@Underground Caverns/Upper Caverns,$canDash',
    ], children=[
    Area('Behind Demon Button', access_rules=['demoncard'], children=[
        Location('Demon Button Room', map_locations=[normal.location(34, 36)], sections=[
            Section('Power of sire(Demon)', location_id=127040000),
            Section('Barley tea(Demon)', location_id=127040008),
            Section('Peanuts 1(Demon)', location_id=127040009),
            Section('Peanuts 2(Demon)', location_id=127040010),
            Section('Peanuts 3(Demon)', location_id=127040011),
            Section('Peanuts 4(Demon)', location_id=127040012),
        ]),
        Location('Demon Button Shaft', map_locations=[normal.location(35, 36)], sections=[
            Section('Ring of ares', location_id=127040004),
            Section('Turkey(Demon)', location_id=127043040),
        ]),
    ]),
    Location('Mine Shaft Bottom', map_locations=[normal.location(29, 43)], sections=[
        Section('Karma coin', location_id=127040001),
        Section('Combat knife', location_id=127040005),
    ]),
    Location('Mine Shaft Middle', map_locations=[normal.location(30, 41)], sections=[
        Section('Shiitake 1', location_id=127040006),
        Section('Shiitake 2', location_id=127040007),
    ]),
    boss_location('Cerberos', 'cerberos', normal, 28.5, 35, location_id=127043041),
    normal.simple_location('Demon Card', 27, 39, location_id=127043042),
])

# Catacombs
catacombs = Area('Catacombs', access_rules=['@Abandoned Mine'], children=[
    Location('Catacombs Entrance', map_locations=[normal.location(26, 45)], sections=[
        Section('Cat-eye circl.', location_id=127020000),
        Section('Bloodstone', location_id=127020008),
    ]),
    normal.simple_location('Icebrand', 22, 45, access_rules=['$canHighJump'], location_id=127020001),
    normal.simple_location('Walk armor', 21, 45, location_id=127020002),
    normal.simple_location('Mormegil', 15, 45, location_id=127020003),
    Location('Lava Bridge', map_locations=[normal.location(24, 45)], access_rules=['$canHighJump'], sections=[
        Section('Heart Vessel(Ballroom mask)', location_id=127020006),
        Section('Ballroom mask', location_id=127020007),
    ]),
    Location('Crypt', map_locations=[normal.location(30, 46)], sections=[
        Section('Life Vessel(Crypt)', location_id=127020009),
        Section('Heart Vessel(Crypt)', location_id=127020010),
    ]),
    Location('Sarcophagus', map_locations=[normal.location(31.5, 46)], sections=[
        Section('Monster vial 3 1(Sarcophagus)', location_id=127020017),
        Section('Monster vial 3 2(Sarcophagus)', location_id=127020018),
        Section('Monster vial 3 3(Sarcophagus)', location_id=127020019),
        Section('Monster vial 3 4(Sarcophagus)', location_id=127020020),
    ]),
    boss_location('Legion', 'legion', normal, 16.5, 45.5, location_id=127023020),
    Area('Beyond Spike Maze', access_rules=['soulofbat,echoofbat', 'spikebreaker,$canJump'], children=[
        Location('Spike Hallway', map_locations=[normal.location(46, 45)], sections=[
            Section('Cross shuriken 1(Spike breaker)', location_id=127020011),
            Section('Cross shuriken 2(Spike breaker)', location_id=127020012),
            Section('Karma coin 1(Spike breaker)', location_id=127020013),
            Section('Karma coin 2(Spike breaker)', location_id=127020014),
        ]),
        normal.simple_location('Pork bun', 46, 46, location_id=127020015),
        Location('Spike Breaker Room', map_locations=[normal.location(39, 46)], sections=[
            Section('Library card(Spike breaker)', location_id=127020004),
            Section('Spike breaker', location_id=127020016),
        ]),
    ]),
])

# Olrox's Quarters
olrox = Area("Olrox's Quarters", access_rules=['opened_no2,jewelofopen', 'opened_are,jewelofopen', '$canJump'], children=[
    Area('Front Quarters', access_rules=[
        '$canJump',
        'opened_are,@Royal Chapel',
        'opened_no2,jewelofopen,$canFly',
    ], children=[
        Location('Secret Hallway', map_locations=[normal.location(30, 17)], sections=[
            Section('Broadsword', location_id=127100004),
            Section('Onyx', location_id=127100005),
            Section('Cheese', location_id=127100006),
        ]),
        normal.simple_location('Manna prism', 33, 15, access_rules=['$canFly'], location_id=127100007),
        normal.simple_location('Resist fire', 33, 14, access_rules=['$canFly'], location_id=127100008),
        normal.simple_location('Luck potion', 33, 12, access_rules=['$canFly'], location_id=127100009),
        normal.simple_location('Estoc', 28, 10, access_rules=['$canFly'], location_id=127100010),
    ]),
    Area('Back Quarters', access_rules=[
        '$canFly',
        'opened_no2,jewelofopen',
    ], children=[
        normal.simple_location('Heart Vessel', 19, 14, location_id=127100001),
        normal.simple_location('Iron ball', 20, 11, access_rules=['$canFly'], location_id=127100011),
        normal.simple_location('Garnet', 31, 13, access_rules=['$canFly'], location_id=127100012),
        normal.simple_location('Echo of Bat', 14, 11, access_rules=['$canFly'], location_id=127103101),
        normal.simple_location('Sword Card', 18, 13, access_rules=['$canFly'], location_id=127103102),
        boss_location('Olrox', 'olrox', normal, 17.5, 11.5, access_rules=['$canFly'], location_id=127103100),
    ]),
])

# Colosseum
colosseum = Area('Colosseum', access_rules=['opened_are,jewelofopen', '$canJump'], children=[
    normal.simple_location('Heart Vessel', 24, 19, location_id=127010000),
    normal.simple_location('Shield rod', 11, 19, location_id=127010001),
    normal.simple_location('Blood cloak', 18, 19, location_id=127010003),
    normal.simple_location('Knight shield(Chapel passage)', 12, 17, location_id=127010004),
    normal.simple_location('Library card', 16, 17, location_id=127010005),
    normal.simple_location('Green tea', 17, 19, location_id=127010006),
    normal.simple_location('Holy sword(Hidden attic)', 17, 15, access_rules=['$canHighJump'], location_id=127010007),
    boss_location('Minotaurus & Werewolf', 'minotauruswerewolf', normal, 17.5, 17, location_id=127013010),
    normal.simple_location('Form of Mist', 19, 17, location_id=127013011),
])

# Clock Tower
clock_tower = Area('Clock Tower', access_rules=['$canJump'], children=[
    Location('Below Bridge', map_locations=[normal.location(53, 9)], sections=[
        Section('Magic missile', location_id=127150000),
        Section('Pentagram', location_id=127150001),
    ]),
    Location('Pillars', map_locations=[normal.location(52, 8)], access_rules=['$canHighJump'], sections=[
        Section('Bekatowa', location_id=127150007),
        Section('Shaman shield', location_id=127150008),
        Section('Ice mail', location_id=127150009),
    ]),
    Location('Hidden Room', map_locations=[normal.location(47, 9)], sections=[
        Section('Star flail', location_id=127150003),
        Section('Gold plate', location_id=127150004),
        Section('Steel helm', location_id=127150005),
    ]),
    normal.simple_location('Healing mail', 40, 6, location_id=127150006),
    normal.simple_location('Life Vessel(Gear train)', 48, 4, location_id=127150010),
    normal.simple_location('Heart Vessel(Gear train)', 50, 4, location_id=127150011),
    normal.simple_location('Pot roast', 46, 5, location_id=127153151),
    Location('Keep Approach', map_locations=[normal.location(40, 5)], sections=[
        Section('Bwaka knife', location_id=127153150),
        Section('Shuriken', location_id=127153152),
        Section('TNT', location_id=127153153),
    ]),
    boss_location('Karasuman', 'karasuman', normal, 38, 5, location_id=127153154),
    normal.simple_location('Fire of Bat', 57, 6, access_rules=['$canFly'], location_id=127153155),
])

# Castle Keep
keep = Area('Castle Keep', children=[
    Location('Keep Bottom', map_locations=[normal.location(29, 6)], access_rules=['$canJump', 'jewelofopen'], sections=[
        Section('Turquoise', location_id=127160000),
        Section('Turkey(Behind wall)', location_id=127160001),
        Section('Leap Stone', location_id=127163160),
    ]),
    Area('Main Keep', access_rules=['$canJump'], children=[
        Location('Below Throne', map_locations=[normal.location(29, 4)], access_rules=['$canFly'], sections=[
            Section('Fire mail(Behind wall)', location_id=127160002),
            Section('Power of Mist', location_id=127163161),
        ]),
        normal.simple_location('Tyrfing', 37, 6, location_id=127160003),
        normal.simple_location('Falchion', 37, 3, location_id=127160012),
        normal.simple_location('Heart Vessel(Before Richter)', 33, 3, access_rules=['$canFly'], location_id=127160018),
        Location('Above Throne', map_locations=[normal.location(32, 1)], access_rules=['$canFly'], sections=[
            Section('Sirloin(Above Richter)', location_id=127160004),
            Section('Turkey(Above Richter)', location_id=127160005),
            Section('Pot roast(Above Richter)', location_id=127160006),
            Section('Frankfurter(Above Richter)', location_id=127160007),
            Section('Resist stone(Above Richter)', location_id=127160008),
            Section('Resist dark(Above Richter)', location_id=127160009),
            Section('Resist holy(Above Richter)', location_id=127160010),
            Section('Platinum mail(Above Richter)', location_id=127160011),
        ]),
        Location('Viewing Room', map_locations=[normal.location(36.5, 1)], access_rules=['$canFly'], sections=[
            Section('Life Vessel 1(Viewing room)', location_id=127160013),
            Section('Life Vessel 2(Viewing room)', location_id=127160014),
            Section('Heart Vessel 1(Viewing room)', location_id=127160015),
            Section('Heart Vessel 2(Viewing room)', location_id=127160016),
            Section('Ghost Card', location_id=127163162),
        ]),
    ]),
])

# *** Inverted castle

# Reverse Entrance
reverse_entrance = Area("Reverse Entrance", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Life Vessel", 42, 12, location_id=127270008),
    inverted.simple_location("Talisman", 41, 14, location_id=127270009),
    Location("Hidden Room", map_locations=[inverted.location(51, 10)], access_rules=['soulofbat,soulofwolf'], sections=[
        Section("Zircon", location_id=127270004),
        Section("Opal", location_id=127270005),
        Section("Beryl circlet", location_id=127270006),
    ]),
    inverted.simple_location("Heart Vessel", 42, 15, location_id=127270003),
    inverted.simple_location("Fire boomerang", 56, 13, location_id=127270007),
    Location("Below Entrance", map_locations=[inverted.location(58.5, 13)], sections=[
        Section("Hammer", location_id=127270000),
        Section("Antivenom", location_id=127270001),
    ]),
    inverted.simple_location("Pot roast", 49, 11, location_id=127273270),
    inverted.simple_location("High potion", 42, 11, location_id=127270002),
])

# Necromancy Laboratory
necromancy_lab = Area("Necromancy Laboratory", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Resist dark", 47, 15, location_id=127290009),
    inverted.simple_location("Heart Vessel", 50, 17, location_id=127290001),
    inverted.simple_location("Life Vessel", 51, 22, location_id=127290002),
    inverted.simple_location("Katana", 49, 15, location_id=127290005),
    inverted.simple_location("Goddess shield", 45, 20, location_id=127290003),
    inverted.simple_location("Manna prism", 48, 16, location_id=127290004),
    inverted.simple_location("Turquoise", 42, 24, location_id=127290007),
    inverted.simple_location("High potion", 46, 18, location_id=127290006),
    inverted.simple_location("Ring of Arcana", 48, 24, location_id=127290008),
    boss_location('Beezelbub', 'beezelbub', inverted, 50.5, 23.5, location_id=127293290),
])

# Black Marble Gallery
black_marble_gallery = Area("Black Marble Gallery", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Library card", 35, 17, location_id=127240000),
    Location("Left Clock", map_locations=[inverted.location(27.5, 26)], sections=[
        Section("Resist dark(Left clock)", location_id=127240005),
        Section("Resist holy(Left clock)", location_id=127240006),
        Section("Resist thunder(Left clock)", location_id=127240007),
        Section("Resist fire(Left clock)", location_id=127240008),
    ]),
    inverted.simple_location("Life Vessel(Middle clock)", 31, 28, location_id=127240003),
    inverted.simple_location("Heart Vessel(Middle clock)", 27, 28, location_id=127240004),
    inverted.simple_location("Heart Refresh(Inside clock)", 28, 24, location_id=127240011),
    inverted.simple_location("Iron ball", 17, 25, location_id=127240010),
    inverted.simple_location("Meal ticket", 15, 27, location_id=127240009),
    inverted.simple_location("Antivenom", 36, 22, location_id=127240002),
    inverted.simple_location("Potion", 36, 20, location_id=127240001),
    inverted.simple_location("Kill Dracula", 29, 20, access_rules=['$canFightDracula']),
])

# Reverse Outer Wall
reverse_outer_wall = Area("Reverse Outer Wall", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Behind Grate", map_locations=[inverted.location(2, 24)], access_rules=['formofmist'], sections=[
        Section("Shotel", location_id=127250001),
        Section("Hammer", location_id=127250002),
    ]),
    inverted.simple_location("Garnet", 1, 36, location_id=127250007),
    inverted.simple_location("Luck potion", 0, 27, location_id=127250004),
    inverted.simple_location("Shield potion", 2, 28, location_id=127250005),
    inverted.simple_location("High potion", 0, 28, location_id=127250006),
    inverted.simple_location("Life Vessel", 0, 26, location_id=127250003),
    inverted.simple_location("Dim Sum set", 2, 25, location_id=127253240),
    Location("The Creature", map_locations=[inverted.location(3.5, 28)], sections=[
        Section('Creature kill', hosted_item='creature', location_id=127253241),
        Section('Tooth of Vlad', location_id=127253242),
    ]),
    inverted.simple_location("Heart Vessel", 0, 23, location_id=127250000),
])

# Forbidden Library
reverse_library = Area("Forbidden Library", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Neutron bomb", 12, 33, location_id=127230006),
    inverted.simple_location("Badelaire", 11, 33, location_id=127230007),
    Location("Side Room", map_locations=[inverted.location(9, 33)], sections=[
        Section("Resist fire", location_id=127230003),
        Section("Resist ice", location_id=127230004),
        Section("Resist stone", location_id=127230005),
    ]),
    inverted.simple_location("Staurolite", 13, 30, access_rules=['formofmist'], location_id=127230008),
    Location("Reverse Librarian", map_locations=[inverted.location(12, 31)], sections=[
        Section('Turquoise', location_id=127230000),
        Section('Opal', location_id=127230001),
        Section('Library card', location_id=127230002),
    ]),
])

# Anti-Chapel
anti_chapel = Area("Anti-Chapel", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Boomerang", 55, 28, location_id=127220008),
    inverted.simple_location("Diamond", 55, 27, location_id=127220003),
    inverted.simple_location("Fire boomerang", 52, 30, location_id=127220002),
    inverted.simple_location("Twilight cloak", 52, 36, access_rules=[
        'formofmist,spikebreaker',
        'formofmist,powerofmist',
    ], location_id=127220016),
    inverted.simple_location("Zircon", 59, 24, location_id=127220004),
    inverted.simple_location("Shuriken", 57, 26, location_id=127220006),
    inverted.simple_location("Heart Vessel(5)", 57, 25, location_id=127220005),
    inverted.simple_location("Heart Vessel(17)", 58, 23, location_id=127220017),
    inverted.simple_location("TNT", 56, 27, location_id=127220007),
    inverted.simple_location("Javelin", 54, 29, location_id=127220009),
    inverted.simple_location("Manna prism", 47, 39, location_id=127220010),
    inverted.simple_location("Smart potion", 46, 38, location_id=127220011),
    inverted.simple_location("Life Vessel", 47, 37, location_id=127220012),
    inverted.simple_location("Talwar", 42, 40, location_id=127220013),
    inverted.simple_location("Bwaka knife", 34, 41, location_id=127220014),
    inverted.simple_location("Magic missile", 34, 40, location_id=127220015),
    Location("Medusa", map_locations=[inverted.location(37.5, 38)], sections=[
        Section('Medusa kill', location_id=127223220),
        Section('Heart of Vlad', location_id=127223221),
    ]),
])

# Reverse Caverns
reverse_caverns = Area("Reverse Caverns", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Life Vessel", 25, 24, location_id=127280012),
    inverted.simple_location("Opal", 24, 19, location_id=127280011),
    inverted.simple_location("Dark Blade", 21, 13, location_id=127280023),
    Location("Underwater", map_locations=[inverted.location(31, 13)], access_rules=['gravityboots'], sections=[
        Section('Life Vessel(Underwater)', location_id=127280006),
        Section('Potion(Underwater)', location_id=127280008),
    ]),
    inverted.simple_location("Osafune katana", 36, 9, access_rules=[
        'soulofbat',
        'gravityboots,leapstone',
        'gravityboots,soulofwolf',
    ], location_id=127280026),
    inverted.simple_location("Garnet", 39, 14, location_id=127280004),
    inverted.simple_location("Zircon(Vase)", 22, 25, location_id=127280014),
    inverted.simple_location("Diamond", 26, 24, location_id=127280013),
    inverted.simple_location("Heart Vessel(Air pocket)", 23, 13, access_rules=['gravityboots,holysymbol'], location_id=127280007),
    inverted.simple_location("Heart Vessel(Succubus side)", 18, 22, location_id=127280015),
    Location("Succubus Side", map_locations=[inverted.location(17, 18.5)], sections=[
        Section("Meal ticket 1(Succubus side)", location_id=127280016),
        Section("Meal ticket 2(Succubus side)", location_id=127280017),
        Section("Meal ticket 3(Succubus side)", location_id=127280018),
        Section("Meal ticket 4(Succubus side)", location_id=127280019),
        Section("Meal ticket 5(Succubus side)", location_id=127280020),
    ]),
    inverted.simple_location("Zircon(Doppleganger)", 18, 12, location_id=127280021),
    inverted.simple_location("Pot roast(Doppleganger)", 16, 13, location_id=127280022),
    inverted.simple_location("Elixir", 16, 10, location_id=127280025),
    inverted.simple_location("Manna prism", 19, 9, location_id=127280024),
    inverted.simple_location("Shiitake 3(Near air pocket)", 23, 14, location_id=127280009),
    inverted.simple_location("Shiitake 4(Near air pocket)", 24, 14, location_id=127280010),
    inverted.simple_location("Bat Pentagram", 36, 14, access_rules=['leapstone', 'soulofbat'], location_id=127280005),
    inverted.simple_location("Shiitake 2(Waterfall)", 38, 11, location_id=127280003),
    inverted.simple_location("Toadstool(Waterfall)", 38, 10, location_id=127280002),
    inverted.simple_location("Shiitake 1(Near entrance passage)", 44, 10, location_id=127280001),
    boss_location('Doppleganger40', 'doppleganger40', inverted, 21, 12, location_id=127283280),
    inverted.simple_location("Force of Echo", 6, 10, location_id=127283281),
    inverted.simple_location("Alucard shield", 53, 9, location_id=127280000),
])

# Cave
cave = Area("Cave", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Demon Button Room", map_locations=[inverted.location(25, 10)], access_rules=['demoncard'], sections=[
        Section("Power of Sire(Demon)", location_id=127210000),
        Section("Life apple(Demon)", location_id=127210001),
    ]),
    Location("Cave Top", map_locations=[inverted.location(30, 3)], sections=[
        Section("Green tea(Demon)", location_id=127210003),
        Section("Power of Sire", location_id=127210004),
    ]),
    Location("Cave Middle", map_locations=[inverted.location(29, 5)], sections=[
        Section("Shiitake 1(6)", location_id=127210006),
        Section("Shiitake 2(7)", location_id=127210007),
    ]),
    inverted.simple_location("Alucard sword", 32, 7, location_id=127210002),
    Location("Death", map_locations=[inverted.location(30.5, 11)], sections=[
        Section("Death kill", hosted_item='death', location_id=127213210),
        Section("Eye of Vlad", location_id=127213211),
    ]),
])

# Floating Catacombs
floating_catacombs = Area("Floating Catacombs", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Catacombs Entrance", map_locations=[inverted.location(33, 1)], sections=[
        Section("Magic missile", location_id=127190000),
        Section("Buffalo star", location_id=127190001),
    ]),
    inverted.simple_location("Necklace of j", 37, 1, location_id=127190013),
    inverted.simple_location("Diamond", 38, 1, location_id=127190014),
    Location("After Galamoth", map_locations=[inverted.location(44, 0)], sections=[
        Section("Heart Vessel(After Galamoth)", location_id=127190015),
        Section("Life Vessel(After Galamoth)", location_id=127190016),
    ]),
    Location("Gas Cloud Room", map_locations=[inverted.location(44, 1)], sections=[
        Section("Ruby circlet", location_id=127190017),
        Section("Gas Cloud", location_id=127193191),
    ]),
    Location("Lava Bridge", map_locations=[inverted.location(35, 1)], sections=[
        Section("Shield potion", location_id=127190011),
        Section("Attack potion", location_id=127190012),
    ]),
    Location("Crypt", map_locations=[inverted.location(29, 0)], sections=[
        Section("Life Vessel(9)", location_id=127190009),
        Section("Heart Vessel(10)", location_id=127190010),
    ]),
    Area('Beyond Spike Maze', access_rules=[
        'soulofbat',
        'formofmist,powerofmist',
        'spikebreaker,leapstone',
        'spikebreaker,gravityboots',
    ], children=[
        Location("Spike Hallway", map_locations=[inverted.location(13, 1)], sections=[
            Section("Resist thunder", location_id=127190002),
            Section("Resist fire", location_id=127190003),
            Section("Karma coin(4)(Spike breaker)", location_id=127190004),
            Section("Karma coin(5)(Spike breaker)", location_id=127190005),
        ]),
        inverted.simple_location("Red bean bun", 13, 0, location_id=127190006),
        Location("Spike Breaker Room", map_locations=[inverted.location(20, 0)], sections=[
            Section("Elixir", location_id=127190007),
            Section("Library card", location_id=127190008),
        ]),
    ]),
    boss_location("Galamoth", "galamoth", inverted, 42.5, 0.5, location_id=127193190),
])

# Death Wing's Lair
death_wing = Area("Death Wing's Lair", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Life Vessel", 40, 32, location_id=127260008),
    Location("Secret Hallway", map_locations=[inverted.location(29, 29)], sections=[
        Section("Opal", location_id=127260000),
        Section("Sword of hador", location_id=127260001),
        Section("High potion", location_id=127260002),
    ]),
    Location("Middle Shaft", map_locations=[inverted.location(26, 32)], sections=[
        Section("Shield potion", location_id=127260003),
        Section("Luck potion", location_id=127260004),
    ]),
    inverted.simple_location("Manna prism", 26, 34, location_id=127260005),
    inverted.simple_location("Aquamarine", 31, 36, location_id=127260006),
    inverted.simple_location("Shuriken", 39, 35, location_id=127260010),
    inverted.simple_location("Alucard mail", 28, 33, location_id=127260007),
    inverted.simple_location("Heart Vessel", 45, 35, access_rules=['soulofbat', 'soulofwolf', 'formofmist'], location_id=127260011),
    inverted.simple_location("Heart Refresh", 41, 33, location_id=127260009),
    Location("Akmodan II", map_locations=[inverted.location(41.5, 34.5)], access_rules=['soulofbat', 'soulofwolf', 'formofmist'], sections=[
        Section("Akmodan II kill", hosted_item='akmodan', location_id=127263260),
        Section("Rib of Vlad", location_id=127263261),
    ]),
])

# Reverse Colosseum
reverse_colosseum = Area("Reverse Colosseum", access_rules=['$canAccessInvertedCastle'], children=[
    inverted.simple_location("Fury plate(Hidden floor)", 42, 31, location_id=127180000),
    inverted.simple_location("Zircon", 48, 27, location_id=127180001),
    inverted.simple_location("Buffalo star", 42, 27, location_id=127180002),
    inverted.simple_location("Gram", 41, 27, location_id=127180003),
    inverted.simple_location("Aquamarine", 35, 27, location_id=127180004),
    Location("Passage", map_locations=[inverted.location(38, 28)], sections=[
        Section('Heart Vessel(5)', location_id=127180005),
        Section('Life Vessel', location_id=127180006),
        Section('Heart Vessel(7)', location_id=127180007),
    ]),
    boss_location('Fake Trevor & Grant & Sypha', 'faketrio', inverted, 41.5, 29, location_id=127183180),
])

# Reverse Clock Tower
reverse_clock_tower = Area("Reverse Clock Tower", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Above Bridge", map_locations=[inverted.location(6, 37)], sections=[
        Section("Magic missile", location_id=127300000),
        Section("Karma coin", location_id=127300001),
    ]),
    Location("Pillars", map_locations=[inverted.location(7, 38)], sections=[
        Section("Str. potion", location_id=127300002),
        Section("Luminus", location_id=127300003),
        Section("Smart potion", location_id=127300004),
    ]),
    inverted.simple_location("Dragon helm", 2, 40, location_id=127300005),
    Location("Hidden Room", map_locations=[inverted.location(12, 37)], sections=[
        Section("Diamond(Hidden room)", location_id=127300006),
        Section("Life apple(Hidden room)", location_id=127300007),
        Section("Sunstone(Hidden room)", location_id=127300008),
    ]),
    inverted.simple_location("Moon rod", 19, 40, location_id=127300011),
    inverted.simple_location("Heart Vessel", 11, 42, location_id=127300010),
    inverted.simple_location("Life Vessel", 9, 42, location_id=127300009),
    inverted.simple_location("Turkey", 13, 40, location_id=127303301),
    Location("Keep Approach", map_locations=[inverted.location(19, 41)], sections=[
        Section("Bwaka knife", location_id=127303300),
        Section("Shuriken", location_id=127303302),
        Section("TNT", location_id=127303303),
    ]),
    Location("Darkwing Bat", map_locations=[inverted.location(21, 41)], sections=[
        Section("Darkwing bat kill", hosted_item='darkwingbat', location_id=127303304),
        Section("Ring of Vlad", location_id=127303305),
    ]),
])

# Reverse Castle Keep
reverse_keep = Area("Reverse Castle Keep", access_rules=['$canAccessInvertedCastle'], children=[
    Location("Keep Top", map_locations=[inverted.location(30, 40)], sections=[
        Section("Sword of dawn", location_id=127310000),
        Section("Garnet", location_id=127310022),
    ]),
    inverted.simple_location("Iron ball(Above Richter)", 30, 42, location_id=127310001),
    inverted.simple_location("Lightning mail", 22, 40, location_id=127310023),
    Location("Below Throne", map_locations=[inverted.location(27, 45)], sections=[
        Section("Bastard sword", location_id=127310004),
        Section("Life Vessel 1", location_id=127310005),
        Section("Heart Vessel 1", location_id=127310006),
        Section("Life Vessel 2", location_id=127310007),
        Section("Heart Vessel 2", location_id=127310008),
        Section("Life Vessel 3", location_id=127310009),
        Section("Heart Vessel 4", location_id=127310010),
        Section("Royal cloak", location_id=127310011),
    ]),
    inverted.simple_location("Library card", 22, 43, location_id=127310024),
    Location("Viewing Room", map_locations=[inverted.location(22.5, 45)], sections=[
        Section("Resist fire(Viewing room)", location_id=127310017),
        Section("Resist ice(Viewing room)", location_id=127310018),
        Section("Resist thunder(Viewing room)", location_id=127310019),
        Section("Resist stone(Viewing room)", location_id=127310020),
        Section("High potion(Viewing room)", location_id=127310021),
    ]),
    inverted.simple_location("Zircon", 27, 43, location_id=127310002),
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