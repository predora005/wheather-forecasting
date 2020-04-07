#!/bin/bash

while read row; do
    name=`echo ${row} | cut -d , -f 1`
    point_no=`echo ${row} | cut -d , -f 2`
    date=`echo ${row} | cut -d , -f 3`
    days=`echo ${row} | cut -d , -f 4`
    
    python3 highrise_scraping.py ${name} ${point_no} ${date} ${days}
    
done < ./csv/highrise_scraping.csv
