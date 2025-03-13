-- Configuration --------------------------------------
AUTOTRACKER_ENABLE_ITEM_TRACKING = true
AUTOTRACKER_ENABLE_LOCATION_TRACKING = true
AUTOTRACKER_ENABLE_DEBUG_LOGGING = true and ENABLE_DEBUG_LOG
AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP = true and AUTOTRACKER_ENABLE_DEBUG_LOGGING
-------------------------------------------------------
print("")
print("Active Auto-Tracker Configuration")
print("---------------------------------------------------------------------")
print("Enable Item Tracking:        ", AUTOTRACKER_ENABLE_ITEM_TRACKING)
print("Enable Location Tracking:    ", AUTOTRACKER_ENABLE_LOCATION_TRACKING)
if AUTOTRACKER_ENABLE_DEBUG_LOGGING then
    print("Enable Debug Logging:        ", AUTOTRACKER_ENABLE_DEBUG_LOGGING)
    print("Enable AP Debug Logging:        ", AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP)
end
print("---------------------------------------------------------------------")
print("")

ScriptHost:LoadScript("scripts/autotracking/item_mapping.lua")
ScriptHost:LoadScript("scripts/autotracking/location_mapping.lua")

CUR_INDEX = -1
SLOT_DATA = nil


function onClear(slot_data)
    if AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
        print(string.format("called onClear, PlayerNumber: %s, slot_data:\n%s",
                Archipelago.PlayerNumber, dump_table(slot_data)))
    end
    SLOT_DATA = slot_data
    CUR_INDEX = -1

    -- reset locations
    for location_id, _ in pairs(LOCATIONS_MAPPING) do
        local code = LOCATIONS_MAPPING[location_id]
        if code then
            local obj = Tracker:FindObjectForCode(code)
            if obj then
                obj.AvailableChestCount = obj.ChestCount
            elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
                print(string.format("onClear: could not find location %s", code))
            end
        end

        -- Check if this location has a hosted item to collect.
        local hosted_code = HOSTED_ITEMS[location_id]
        if hosted_code then
            local hosted_obj = Tracker:FindObjectForCode(hosted_code)
            if hosted_obj then
                hosted_obj.Active = false
            end
        end
    end

    -- reset items
    for _, v in pairs(ITEM_MAPPING) do
        if v[1] and v[2] then
            local obj = Tracker:FindObjectForCode(v[1])
            if obj then
                if v[2] == "toggle" then
                    obj.Active = false
                elseif v[2] == "progressive" then
                    obj.CurrentStage = 0
                    obj.Active = false
                elseif v[2] == "consumable" then
                    obj.AcquiredCount = 0
                elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
                    print(string.format("onClear: unknown item type %s for code %s", v[2], v[1]))
                end
            elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
                print(string.format("onClear: could not find object for code %s", v[1]))
            end
        end
    end

    -- Opened back doors, if server populates them.
    -- There are now two Underground Caverns back door flags (normal and before Death) so we need to check both.
    if slot_data["early_open_no4"] == 1 then
        slot_data["open_no4"] = 1
    end

    for _, v in ipairs({ "open_no4", "open_are" }) do
        local flag = slot_data[v]
        if flag ~= nil then
            local obj = Tracker:FindObjectForCode(v)
            if obj then
                if flag == 1 then
                    obj.Active = true
                else
                    obj.Active = false
                end
            elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
                print(string.format("onClear: could not find object for code %s", v))
            end
        elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
            print(string.format("onClear: could not find slot data for code %s", v))
        end
    end

    -- Check which extension (location set) we're using.
    local obj = Tracker:FindObjectForCode("extension")
    if obj then
        local flag = slot_data["extension"]
        if flag ~= nil then
            -- Full is 0, but we want to put them in increasing order so move everything down by 1.
            obj.CurrentStage = (flag - 1) % 4
        elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
            print("onClear: could not find slot data for code extension")
        end
    elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
        print("onClear: could not find object for code extension")
    end

    -- Number of bosses needed.
    obj = Tracker:FindObjectForCode("bosses_need")
    if obj then
        if slot_data["bosses_need"] then
            obj.AcquiredCount = slot_data["bosses_need"]
        else
            obj.AcquiredCount = 0
        end
    elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
        print("onClear: could not find object for code bosses_need")
    end

end


function onItem(index, item_id, item_name, player_number)
    if AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
        print(string.format("called onItem: index %s, item_id %s, item_name %s, player_number %s",
                index, item_id, item_name, player_number))
    end

    if index <= CUR_INDEX then
        return
    end
    CUR_INDEX = index;

    local is_local = player_number == Archipelago.PlayerNumber
    local v = ITEM_MAPPING[item_id]
    if not v then
        if AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
            print(string.format("onItem: could not find item_id %s", item_id))
        end
        return
    end

    if is_local then
        local obj = Tracker:FindObjectForCode(v[1])
        if obj then
            if v[2] == "toggle" then
                obj.Active = true
            elseif v[2] == "progressive" then
                if obj.Active then
                    obj.CurrentStage = obj.CurrentStage + 1
                else
                    obj.Active = true
                end
            elseif v[2] == "consumable" then
                obj.AcquiredCount = obj.AcquiredCount + obj.Increment
            elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
                print(string.format("onItem: unknown item type %s for code %s", v[2], v[1]))
            end
        end
    end
end


function onLocation(location_id, location_name)
    if AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
        print(string.format("called onLocation: location_id %s, location_name %s", location_id, location_name))
    end

    local code = LOCATIONS_MAPPING[location_id]
    if not code then
        if AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
            print(string.format("onLocation: could not find location_id %s", location_id))
        end
        return
    end

    local obj = Tracker:FindObjectForCode(code)
    if obj then
        -- Update the chest count if there's any checks left.
        if obj.AvailableChestCount > 0 then
            obj.AvailableChestCount = obj.AvailableChestCount - 1
        end

        -- Check if this location has a hosted item to collect.
        local hosted_code = HOSTED_ITEMS[location_id]
        if hosted_code then
            local hosted_obj = Tracker:FindObjectForCode(hosted_code)
            if hosted_obj then
                hosted_obj.Active = true
            end
        end
    elseif AUTOTRACKER_ENABLE_DEBUG_LOGGING_AP then
        print(string.format("called onLocation: location_id %s, location_name %s", location_id, location_name))
        print(string.format("onLocation: could not find location %s", code))
    end
end


Archipelago:AddClearHandler("clear handler", onClear)
Archipelago:AddItemHandler("item handler", onItem)
Archipelago:AddLocationHandler("location handler", onLocation)
