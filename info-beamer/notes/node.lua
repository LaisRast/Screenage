gl.setup(1920, 80)
util.auto_loader(_G)
json = require("json")

function feeder()
    local notes_json = json.decode(resource.load_file "notes.json")
    local notes = {}
    for idx, note in pairs(notes_json) do
        notes[#notes + 1] = note
    end
    return notes
end

node.event("content_update", function(filename, file)
    text = util.running_text{
        font = font;
        size = 30;
        speed = 100;
        color = {1,1,1,1};
        generator = util.generator(feeder)
    }
end)

function node.render()
    gl.clear(0,0,0,1)
    text:draw(20)
    black:draw(0,0,150,80)
    black:draw(1880,0,WIDTH,HEIGHT)
    font:write(20, 20, "Notes »", 30, 0.88,0.75,0,1)
end








