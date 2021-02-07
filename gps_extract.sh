#!/bin/bash

# write a setup script later
# install shell program as a shell executable
pip3 install geopy pandas geopandas > /dev/null
rm img_coord
touch img_coord
for pic in *
do
    echo "processing $pic"
    lat=`exiftool -filename -gpslatitude -n "$pic" | egrep Latitude | cut -d':' -f2 | sed 's/ //g'`
    lon=`exiftool -filename -gpslongitude -n "$pic" | egrep Longitude | cut -d':' -f2 | sed 's/ //g'`
    if [ -z $lat ] || [ -z $lon ]
    then
        echo "$pic issa meme lmao" >> img_coord
        continue
    fi
    echo "$pic has lat $lat and long $lon" >> img_coord
    #python3 reverse_gc.py $lat $lon
    addy=$(( python3 reverse_gc.py $lat $lon ) 2>&1) 
    echo $addy
    sleep 1
done


