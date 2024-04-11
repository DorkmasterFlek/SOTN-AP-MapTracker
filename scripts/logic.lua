-- Logic functions.

function hasItem(code)
    return Tracker:ProviderCountForCode(code) > 0
end

function getItemCount(code)
    return Tracker:ProviderCountForCode(code)
end

function canTransform()
    return hasItem("soulofbat") or hasItem("soulofwolf") or hasItem("formofmist")
end

function canJump()
    return hasItem("leapstone") or canHighJump() or canFly()
end

function canHighJump()
    return hasItem("gravityboots") or canFly()
end

function canFly()
    return hasItem("soulofbat") or
            (hasItem("formofmist") and hasItem("powerofmist")) or
            (hasItem("gravityboots") and hasItem("leapstone"))
end

function canDash()
    return hasItem("soulofwolf") and hasItem("powerofwolf")
end

function canAccessInvertedCastle()
    return canFly() and hasItem("holyglasses")
end

function canFightDracula()
    return getItemCount('pieceofvlad') == 5 and
            getItemCount('bosses_killed') >= getItemCount('bosses_need')
end

-- Update the bosses killed counter whenever a boss item changes.
-- The counter has increment set to zero so the user cannot adjust it manually; it only changes via this script.
function bossKilled(code)
    local obj = Tracker:FindObjectForCode("bosses_killed")
    if obj then
        obj.AcquiredCount = Tracker:ProviderCountForCode(code)
    end
end

ScriptHost:AddWatchForCode('Boss killed', 'boss', bossKilled)
