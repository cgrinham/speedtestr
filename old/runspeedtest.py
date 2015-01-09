#/usr/bin/python
""" Run a speed test every 15 minutes """
import speedtest
from datetime import datetime
import time
import csv
import pygal
from pygal.style import LightSolarizedStyle
import operator


def create_chart(input_dict, filename, title):
    """ Create the output chart with pygal"""
    line_chart = pygal.Line(style=LightSolarizedStyle)
    line_chart.title = title
    line_chart.x_labels = [x[0] for x in sorted(input_dict[0]["data"].items())]
    for dataset in input_dict:
        #print [x[1] for x in sorted(dataset["data"].items())]
        line_chart.add(dataset["title"], [x[1] for x in sorted(dataset["data"].items())])
    line_chart.render_to_file(filename)

while True:
    try:
        speedtest.speedtest()
    except:
        with open("errors.log", "a") as myfile:
            myfile.write("Failed at %s" % datetime.now().strftime('%Y/%m/%d %H:%M'))

    # Prepare download data for chart
    DOWNLOAD_HOURS = {}
    with open("results.csv", "rb") as source:
        rdr = csv.reader(source)
        # Total spent each day of the month
        for r in rdr:
            # Exclude the first line
            if r[0] != "date":
                # Get the hour
                hour = r[1][:-3]
                if hour in DOWNLOAD_HOURS:
                    # Increment number of tests
                    DOWNLOAD_HOURS[hour]["tests"] += 1
                    # Add tested speed
                    DOWNLOAD_HOURS[hour]["cumulative_speed"] += float(r[6])
                else:
                    DOWNLOAD_HOURS[hour] = {}
                    # Create number of tests
                    DOWNLOAD_HOURS[hour]["tests"] = 1
                    # Create tested speed field
                    DOWNLOAD_HOURS[hour]["cumulative_speed"] = float(r[6])

    # Create list of average speeds
    average_dl_speed = {}

    for hour in DOWNLOAD_HOURS:
        average_dl_speed[hour] = round(DOWNLOAD_HOURS[hour]["cumulative_speed"] / DOWNLOAD_HOURS[hour]["tests"], 2)


    # Prepare Upload data for chart
    UPLOAD_HOURS = {}
    with open("results.csv", "rb") as source:
        rdr = csv.reader(source)
        # Total spent each day of the month
        for r in rdr:
            # Exclude the first line
            if r[0] != "date":
                # Get the hour
                hour = r[1][:-3]
                if hour in UPLOAD_HOURS:
                    # Increment number of tests
                    UPLOAD_HOURS[hour]["tests"] += 1
                    # Add tested speed
                    UPLOAD_HOURS[hour]["cumulative_speed"] += float(r[7])
                else:
                    UPLOAD_HOURS[hour] = {}
                    # Create number of tests
                    UPLOAD_HOURS[hour]["tests"] = 1
                    # Create tested speed field
                    UPLOAD_HOURS[hour]["cumulative_speed"] = float(r[7])

    # Create list of average speeds
    average_ul_speed = {}

    for hour in UPLOAD_HOURS:
        average_ul_speed[hour] = round(UPLOAD_HOURS[hour]["cumulative_speed"] / UPLOAD_HOURS[hour]["tests"], 2)

    #print average_ul_speed

    # Prepare PING data for chart
    PING_HOURS = {}
    with open("results.csv", "rb") as source:
        rdr = csv.reader(source)
        # Total spent each day of the month
        for r in rdr:
            # Exclude the first line
            if r[0] != "date":
                # Get the hour
                hour = r[1][:-3]
                if hour in PING_HOURS:
                    # Increment number of tests
                    PING_HOURS[hour]["tests"] += 1
                    # Add tested speed
                    PING_HOURS[hour]["cumulative_ping"] += float(r[5])
                else:
                    PING_HOURS[hour] = {}
                    # Create number of tests
                    PING_HOURS[hour]["tests"] = 1
                    # Create tested speed field
                    PING_HOURS[hour]["cumulative_ping"] = float(r[5])

    # Create list of average speeds
    average_ping = {}

    for hour in PING_HOURS:
        average_ping[hour] = round(PING_HOURS[hour]["cumulative_ping"] / PING_HOURS[hour]["tests"], 2)


    data_dict = [{"title" : "Avg. Download (mbps)", "data" : average_dl_speed}, {"title" : "Avg. Upload (mbps)", "data" : average_ul_speed}]

    ping_dict = [{"title" : "Avg. Ping (ms)", "data" : average_ping}]


    print "Creating Speed Chart..."
    create_chart(data_dict, "/var/www/static/internet/chart.svg", "Internet Speed by Hour")
    print "Done"

    print "Creating Ping Chart..."
    create_chart(ping_dict, "/var/www/static/internet/ping.svg", "Ping by Hour")
    print "Done"

    print "Testing again in 15 minutes..."
    time.sleep(900)
