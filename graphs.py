import numpy as np
import matplotlib.pyplot as plt
import datetime

def plot_time_of_the_day(my_timestamps, other_timestamps):
    my_messages = [0 for x in range(24)]
    other_messages = [0 for x in range(24)]
    for ts in my_timestamps:
        date_time_object = datetime.datetime.fromtimestamp(ts)
        my_messages[date_time_object.hour] += 1
    for ts in other_timestamps:
        date_time_object = datetime.datetime.fromtimestamp(ts)
        other_messages[date_time_object.hour] += 1

    ind = np.arange(len(my_messages))
    width = 0.35

    fig, ax = plt.subplots()

    rects1 = ax.bar(ind - width/2, my_messages, width, color='SkyBlue', label="Sent")
    rects2 = ax.bar(ind + width/2, other_messages, width, color='IndianRed', label="Received")

    ax.set_ylabel("Messages")
    ax.set_title("Messages throughout the day")
    ax.set_xticks(ind)
    ax.set_xticklabels(["%02d" % x for x in range(24)])
    ax.legend()

    plt.show()
