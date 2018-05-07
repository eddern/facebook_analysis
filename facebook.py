import json
import os
from collections import defaultdict
from pprint import pprint
import datetime
import graphs as g

PATH = "../messages"
conversations = os.listdir(PATH)

line_with_pipes = "|"+"-"*136+"|"
line = "-"*138
my_messages_timestamps = []
other_messages_timestamps = []

def list_chats():
    messages = defaultdict(list)
    total_messages = 0
    total_images = 0
    for conv_name in conversations:
        if conv_name == "stickers_used" or conv_name.startswith(".") or "justyou" in conv_name:
            continue
        with open(PATH + "/" + conv_name + "/message.json") as f:
            number_of_imgs = number_of_images(PATH + "/" + conv_name)
            json_data = json.load(f)
        total_images += number_of_imgs
        total_messages += len(json_data["messages"])
        written_by_me = numb_written_by_me(json_data["messages"])
        title = json_data["title"].encode('latin1').decode('utf8')
        messages[title] = (len(json_data["messages"]), number_of_imgs, written_by_me)
        # messages[json_data["title"]] = (len(json_data["messages"]), number_of_imgs, written_by_me)

    # sorted = sorted(messages, key=messages.get)
    tuple_list = [(k, v) for k, v in messages.items()]
    tuple_list.sort(reverse=True, key=lambda x: x[1][0])
    print(line)
    print("| %6s | %60s | %30s | %15s | Percentage |" % ("Index", "Message with", "Number of messages", "Number og photos"))
    print(line_with_pipes)
    counter = 1
    for key, value in tuple_list:
        percentage = (value[0] / total_messages) * 100
        total_and_me = "%d / %d (%3.2f%% me)" % (value[0], value[2], 100*(value[2] / value[0]))
        print("| %6d | %60s | %30s | %16d | %9.2f%% | " % (counter, key, total_and_me, value[1], percentage))
        counter += 1
    print(line_with_pipes)
    total_and_me_overall = total_and_me = "%d / %d (%3.2f%% me)" % (total_messages, len(my_messages_timestamps), 100*(len(my_messages_timestamps) / total_messages))
    print("| %6s | %60s | %30s | %16s |    100.00%% |" % ("", "Total:", total_and_me_overall, total_images))
    print(line)
    g.plot_time_of_the_day(my_messages_timestamps, other_messages_timestamps)

    analyze_timestamps()

def analyze_timestamps():
    times = defaultdict(lambda: defaultdict(int))
    for timestamp in my_messages_timestamps:
        time = datetime.datetime.fromtimestamp(timestamp)
        times[time.year][time.month] += 1


def numb_written_by_me(data):
    me = 0
    for message in data:
        if "sender_name" in message and message["sender_name"].startswith("Cornelius"):
            my_messages_timestamps.append(message["timestamp"])
            me += 1
        else:
            other_messages_timestamps.append(message["timestamp"])
    return me


def number_of_images(path):
    try:
        return len(os.listdir(path + "/photos"))
    except:
        return 0


def main():
    list_chats()

main()