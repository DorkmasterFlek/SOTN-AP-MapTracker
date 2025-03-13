-- Relics start at offset 300 from the base.
RELIC_OFFSET = 300

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
    ITEM_MAPPING[RELIC_OFFSET + n - 1] = item
end

-- Additional mappings for specific equipment we care about.
ITEM_MAPPING[241] = { "goldring", "toggle" }
ITEM_MAPPING[242] = { "silverring", "toggle" }
ITEM_MAPPING[183] = { "spikebreaker", "toggle" }
ITEM_MAPPING[203] = { "holyglasses", "toggle" }
