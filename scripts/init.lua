-- Entry point for all lua code of the pack
-- More info on the Lua API: https://github.com/black-sliver/PopTracker/blob/master/doc/PACKS.md#lua-interface

ENABLE_DEBUG_LOG = false

-- get current variant
local variant = Tracker.ActiveVariantUID

-- check variant info
IS_ITEMS_ONLY = variant:find("itemsonly")

print("Loaded variant: ", variant)
if ENABLE_DEBUG_LOG then
    print("Debug logging is enabled!")
end

-- Utility Script for helper functions etc.
ScriptHost:LoadScript("scripts/utils.lua")

-- Logic
ScriptHost:LoadScript("scripts/logic.lua")

-- Items
Tracker:AddItems("items/settings.json")
Tracker:AddItems("items/relics.json")
Tracker:AddItems("items/bosses.json")

if not IS_ITEMS_ONLY then
    -- Maps
    Tracker:AddMaps("maps/maps.json")

    -- Locations
    -- Normal castle
    Tracker:AddLocations("locations/normal/entrance.json")
    Tracker:AddLocations("locations/normal/alchemy_lab.json")
    Tracker:AddLocations("locations/normal/marble_gallery.json")
    Tracker:AddLocations("locations/normal/outer_wall.json")
    Tracker:AddLocations("locations/normal/library.json")
    Tracker:AddLocations("locations/normal/chapel.json")
    Tracker:AddLocations("locations/normal/caverns.json")
    Tracker:AddLocations("locations/normal/mine.json")
    Tracker:AddLocations("locations/normal/catacombs.json")
    Tracker:AddLocations("locations/normal/olrox.json")
    Tracker:AddLocations("locations/normal/colosseum.json")
    Tracker:AddLocations("locations/normal/clock_tower.json")
    Tracker:AddLocations("locations/normal/keep.json")

    -- Inverted castle
    Tracker:AddLocations("locations/inverted/entrance.json")
    Tracker:AddLocations("locations/inverted/necromancy_lab.json")
    Tracker:AddLocations("locations/inverted/black_marble_gallery.json")
    Tracker:AddLocations("locations/inverted/outer_wall.json")
    Tracker:AddLocations("locations/inverted/library.json")
    Tracker:AddLocations("locations/inverted/anti_chapel.json")
    Tracker:AddLocations("locations/inverted/caverns.json")
    Tracker:AddLocations("locations/inverted/cave.json")
    Tracker:AddLocations("locations/inverted/floating_catacombs.json")
    Tracker:AddLocations("locations/inverted/death_wing.json")
    Tracker:AddLocations("locations/inverted/colosseum.json")
    Tracker:AddLocations("locations/inverted/clock_tower.json")
    Tracker:AddLocations("locations/inverted/keep.json")
end

-- Layout
Tracker:AddLayouts("layouts/items.json")
Tracker:AddLayouts("layouts/broadcast.json")

if IS_ITEMS_ONLY then
    Tracker:AddLayouts("layouts/tracker_items_only.json")
else
    Tracker:AddLayouts("layouts/tracker.json")
end

-- AutoTracking for Archipelago
ScriptHost:LoadScript("scripts/autotracking/archipelago.lua")
