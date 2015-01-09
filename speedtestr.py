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
    line_chart.x_labels = [x[0][1] for x in sorted(input_dict[0]["data"].items())]
    for dataset in input_dict:
        line_chart.add(dataset["title"], [x[1] for x in sorted(dataset["data"].items())])
    line_chart.render_to_file(filename)

def organise_data(period_length, index):
    data_dict = {}
    with open("results.csv", "rb") as source:
        rdr = csv.reader(source)
        # Total spent each day of the month
        for r in rdr:
            # Exclude the first line
            if r[0] != "date":
                # If the period length is daily, get day of week
                if period_length == "daily":
                    year, month, day = (int(x) for x in r[0].split('/'))
                    period_index = (str(datetime(year, month, day).weekday()), datetime(year, month, day).strftime("%A"))
                # If period length is hourly, get hour
                elif period_length == "hourly":
                    period_index = r[1][:-3]
                else:
                    print "Invalid Period Length"
                    quit()

                if period_index in data_dict:
                    # Increment number of tests
                    data_dict[period_index]["tests"] += 1
                    # Add tested speed for given index
                    data_dict[period_index]["cumulative_data"] += float(r[index])
                else:
                    data_dict[period_index] = {}
                    # Create number of tests
                    data_dict[period_index]["tests"] = 1
                    # Create tested speed field
                    data_dict[period_index]["cumulative_data"] = float(r[index])

    # Create list of average speeds
    data_median = {}

    for period in data_dict:
        data_median[period] = round(data_dict[period]["cumulative_data"] / data_dict[period]["tests"], 2)

    return data_median

while True:
    """
    try:
        speedtest.speedtest()
    except:
        with open("errors.log", "a") as myfile:
            myfile.write("Failed at %s" % datetime.now().strftime('%Y/%m/%d %H:%M'))
    """
    
    print "Creating Hourly Speed Chart..."
    hourly_data_dict = [{"title" : "Download", "data" : organise_data("hourly", 6)}, {"title" : "Upload", "data" : organise_data("hourly", 7)}]
    create_chart(hourly_data_dict, "charts/hourly-speed.svg", "Average Internet Speed by Hour (mbps)")
    print "Done"

    print "Creating Hourly Ping Chart..."
    hourly_ping_dict = [{"title" : "Ping", "data" : organise_data("hourly", 5)}]
    create_chart(hourly_ping_dict, "charts/hourly-ping.svg", "Average Ping by Hour (ms)")
    print "Done"
    
    print "Creating Daily Speed Chart..."
    daily_data_dict = [{"title" : "Download", "data" : organise_data("daily", 6)}, {"title" : "Upload", "data" : organise_data("daily", 7)}]
    create_chart(daily_data_dict, "charts/daily-speed.svg", "Average Internet Speed by Day (mbps)")
    print "Done"

    print "Creating Daily Ping Chart..."
    daily_ping_dict = [{"title" : "Ping", "data" : organise_data("daily", 5)}]
    create_chart(daily_ping_dict, "charts/daily-ping.svg", "Average Ping by Day (ms)")
    print "Done"

    print "Testing again in 15 minutes..."
    time.sleep(900)
