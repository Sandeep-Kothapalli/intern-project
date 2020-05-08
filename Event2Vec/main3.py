import pickle
from pprint import pprint
from datetime import datetime
import tensorflow as tf
from keras.utils import to_categorical

ersvp = pickle.load(open("ersvp", "rb"))
egroup = pickle.load(open("egroup", "rb"))
elat = pickle.load(open("elat", "rb"))
elon = pickle.load(open("elon", "rb"))
etime = pickle.load(open("etime", "rb"))


def main():
    D = {}
    users = []

    # counting all users in all events
    for event in ersvp:
        for attendees in ersvp[event]:
            users.append(attendees[0])

    # unique number of users
    users = list(set(users))
    for user in users:
        D[user] = []

    # deleting events with non numeric event ids
    for event in list(ersvp):
        if not event.isnumeric():
            del ersvp[event]
    # # experimental.. should ideally be commented
    # for event in list(ersvp):
    #     if int(event) % 2 == 0:
    #         del ersvp[event]

    # deleting events with strength less than 20
    for event in list(ersvp):
        if len(ersvp[event]) < 20:
            del ersvp[event]

    # deleting events for which corresponding entries in other dictionaries is not present
    for event in list(ersvp):
        if event not in elat or event not in elon or event not in etime:
            del ersvp[event]

    # creating user profiles
    for event in ersvp:
        for attendees in ersvp[event]:
            if (event in elat) and (event in elon) and (event in etime):
                fourTuple = [event, elon[event], elat[event], etime[event]]
                D[attendees[0]].append(fourTuple)

    # removing users who have attended less than 20 events
    for user in list(D):
        if len(D[user]) < 20:
            del D[user]

    # sort user profiles chronological order
    for user in D:
        D[user] = sorted(D[user], key=lambda events: events[3])
        for event in D[user]:
            event[3] = datetime.utcfromtimestamp(event[3] / 1000).strftime("%d/%m/%Y, %H:%M:%S")

    # the dictionary containing only the events attended by each user without timestamps
    D_only_events = {}
    i = 0
    for user in D:
        # 2621867
        D_only_events[user] = []
        for event in D[user]:
            D_only_events[user].append(int(event[0]))

    # eltForInputs = {}
    # eltForOutputs = {}
    # i = 0
    # for user in D:
    #     eltForInputs[user] = D[user][:-1]
    #     eltForOutputs[user] = D[user][-1]
    #

    allEvents = [event for event in ersvp]

    mapping = {}
    for x in range(len(allEvents)):
        mapping[allEvents[x]] = x
    # for user in eltForInputs:
    userOneHots = {}
    for user in D_only_events:
        userOneHots[user] = [0]*len(ersvp)
        for x in range(len(D_only_events[user])):
            userOneHots[user][mapping[D_only_events[user][x]]] = 1








if __name__ == '__main__':
    main()
