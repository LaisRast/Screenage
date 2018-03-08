## Define the functions
datetime ()
    {
    python3 ./scripts/date_time/date_time.py
    cp ./scripts/date_time/date_time.png ./info-beamer/date_time.png
    }

forecast ()
    {
    python3 ./scripts/forecast/forecast.py
    cp ./scripts/forecast/forecast.png ./info-beamer/forecast.png
    }

gcalendar ()
    {
    python3 ./scripts/gcalendar/gcalendar.py
    cp ./scripts/gcalendar/gcalendar.png ./info-beamer/gcalendar.png
    }

rss_aj ()
    {
    python3 ./scripts/rss_aj/rss_aj.py
    cp ./scripts/rss_aj/imgs/* ./info-beamer/news/
    }

rss_ts ()
    {
    python3 ./scripts/rss_ts/rss_ts.py
    cp ./scripts/rss_ts/imgs/* ./info-beamer/news/
    }

notes ()
    {
    python3 ./scripts/notes/notes.py
    cp ./scripts/notes/notes.json ./info-beamer/notes/notes.json
    }

vbb ()
    {
    python3 ./scripts/vbb/vbb.py
    cp ./scripts/vbb/vbb.png ./info-beamer/vbb.png
    }

weather ()
    {
    python3 ./scripts/weather/weather.py
    cp ./scripts/weather/weather.png ./info-beamer/weather.png
    }

## Main Script
info-beamer info-beamer/. >/dev/null 2>&1 &
elapsed=0
while true
do
    if (( $elapsed % 60 == 0))
    then
        weather
        echo "[Weather]: updated at $(date +%H:%M:%S)"
    fi
    
    if (( $elapsed % 10 == 0))
    then
        datetime
        echo "[Time]: updated at $(date +%H:%M:%S)"
    fi
    
    if (( $elapsed % (60*60) == 0))
    then
        gcalendar
        echo "[Calendar]: updated at $(date +%H:%M:%S)"
    fi
    
    if (( $elapsed % 60 == 0))
    then
        forecast
        echo "[Forecast]: updated at $(date +%H:%M:%S)"
    fi
    
    if (( $elapsed % 30 == 0))
    then
        vbb
        echo "[Traffic]: updated at $(date +%H:%M:%S)"
    fi

    if (( $elapsed % (60*60) == 0))
    then
        rss_ts
        echo "[News]: updated at $(date +%H:%M:%S)"
    fi

    if (( $elapsed % (60*2) == 0))
    then
        notes
        echo "[Notes]: updated at $(date +%H:%M:%S)"
    fi
    
    sleep 1
    elapsed=$(($elapsed+1))
done
