gl.setup(650, 370)

local SWITCH_TIME = 20

--[=[ Get all the pictures in the current dictionary. ]=]
local pictures = util.generator(function()
    local images = {}
    for name, _ in pairs(CONTENTS) do
        if name:match(".*jpg") or name:match(".*png") then
            images[#images + 1] = name
        end
    end
    return images
end)

--[=[ This is called if a file was removed from the current node. ]=]
node.event("content_remove", function(filename)
    pictures:remove(filename)
end)

local current_image = resource.load_image(pictures.next())
local next_image
local next_image_time = sys.now() + SWITCH_TIME

function node.render()
    gl.clear(0,0,0,0)
    local time_to_next = next_image_time - sys.now()
    if time_to_next < 0 then
        if next_image then
            current_image:dispose()
            current_image = next_image
            next_image = nil
            next_image_time = sys.now() + SWITCH_TIME
            util.draw_correct(current_image, 0,0,WIDTH,HEIGHT)
        else
            next_image_time = sys.now() + SWITCH_TIME
        end
        util.draw_correct(current_image, 0,0,WIDTH,HEIGHT)
    elseif time_to_next < 1 then
        if not next_image then
            next_image = resource.load_image(pictures.next())
        end
        local xoff = (1 - time_to_next) * WIDTH

        gl.pushMatrix()
        gl.rotate(200 * (1-time_to_next), 0,1,0)
        util.draw_correct(current_image, 0 + xoff, 0, WIDTH + xoff, HEIGHT, time_to_next)
        gl.popMatrix()
        gl.pushMatrix()
        xoff = time_to_next * -WIDTH
        gl.rotate(100 * (time_to_next), 1,-1,0)
        util.draw_correct(next_image, 0 + xoff, 0,WIDTH + xoff, HEIGHT, 1-time_to_next)
        gl.popMatrix()
    else
        util.draw_correct(current_image, 0,0,WIDTH,HEIGHT)
    end
end
