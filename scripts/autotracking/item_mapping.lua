BASE_ITEM_ID = 127000000

RELICS = {
    { "soulofbat", "toggle" },
    { "fireofbat", "toggle" },
    { "echoofbat", "toggle" },
    { "forceofecho", "toggle" },
    { "soulofwolf", "toggle" },
    { "powerofwolf", "toggle" },
    { "skillofwolf", "toggle" },
    { "formofmist", "toggle" },
    { "powerofmist", "toggle" },
    { "gascloud", "toggle" },
    { "cubeofzoe", "toggle" },
    { "spiritorb", "toggle" },
    { "gravityboots", "toggle" },
    { "leapstone", "toggle" },
    { "holysymbol", "toggle" },
    { "faeriescroll", "toggle" },
    { "jewelofopen", "toggle" },
    { "mermanstatue", "toggle" },
    { "batcard", "toggle" },
    { "ghostcard", "toggle" },
    { "faeriecard", "toggle" },
    { "demoncard", "toggle" },
    { "swordcard", "toggle" },
    -- Blank entries for ID gap (this rando doesn't include the JP specific familiars).
    { "" },
    { "" },
    { "heartofvlad", "toggle" },
    { "toothofvlad", "toggle" },
    { "ribofvlad", "toggle" },
    { "ringofvlad", "toggle" },
    { "eyeofvlad", "toggle" },
}

ITEM_MAPPING = {}
for n, item in ipairs(RELICS) do
    -- Relics start at offset 300 from the base.
    ITEM_MAPPING[BASE_ITEM_ID + 300 + n - 1] = item
end

-- Additional mappings for specific equipment we care about.
ITEM_MAPPING[BASE_ITEM_ID + 241] = { "goldring", "toggle" }
ITEM_MAPPING[BASE_ITEM_ID + 242] = { "silverring", "toggle" }
ITEM_MAPPING[BASE_ITEM_ID + 183] = { "spikebreaker", "toggle" }
ITEM_MAPPING[BASE_ITEM_ID + 203] = { "holyglasses", "toggle" }
