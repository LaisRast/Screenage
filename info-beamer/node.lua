gl.setup(1920, 1080)

util.auto_loader(_G)

function node.render()
    black:draw(0, 0, WIDTH, HEIGHT)
    yellow:draw(0, 150, WIDTH, 150 + 5)
    background:draw(0, 155, WIDTH, 995)
    yellow:draw(0, 995, WIDTH, 995 + 5)
    weather:draw(30, 15, 30 + 300, 15 + 120)
    date_time:draw(1590, 15, 1590 + 300, 15 + 120)
    gcalendar:draw(30 , 190, 30 + 650, 190 + 770)
    forecast:draw(710, 190, 710 + 650, 190 + 370)
    vbb:draw(1390, 190, 1390 + 500, 190 + 770)

    local news = resource.render_child("news")
    news:draw(710, 590, 710 + 650, 590 + 370)
    
    local notes = resource.render_child("notes")
    notes:draw(0, 1000, 0+ 1920, 1000 + 80)
end
