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
        D[user] = sorted(D[user], key=lambda eventsKey: eventsKey[3])
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

    allEvents = [event for event in ersvp]
    #     implementation of event2vec2 not using event descriptions .. only using latitude, longitude, time
    allLats = [elat[event] for event in ersvp]
    allLongs = [elon[event] for event in ersvp]
    allTimes = [datetime.utcfromtimestamp(etime[event] / 1000).strftime("%d/%m/%Y, %H:%M:%S") for event in ersvp]

    latMappings = {}
    lonMappings = {}
    timeMappings = {}
    #             create mappings for onehot vectors
    #     latitudes
    for x in range(len(allLats)):
        latMappings[allLats[x]] = x
    #     longitudes
    for x in range(len(allLongs)):
        lonMappings[allLongs[x]] = x
    #     times
    for x in range(len(allTimes)):
        timeMappings[allTimes[x].split(" ")[1]] = x

    oneHotLongitude = {}
    oneHotTime = {}
    oneHotLatitude = {}
    for user in D:
        oneHotLatitude[user] = [0] * len(allLats)
        oneHotLongitude[user] = [0] * len(allLongs)
        oneHotTime[user] = [0] * len(allTimes)
        for events in D[user]:
            oneHotLongitude[user][lonMappings[events[1]]] = 1
            oneHotLatitude[user][latMappings[events[2]]] = 1
            oneHotTime[user][timeMappings[events[3].split(" ")[1]]] = 1

#     for each user oneHotLatitude contains ones at each event mapped index
#     considering only time and not date, parsing and removing it for further indexing purposes
#     basic feedforward neural network
    model = tf.keras.models.Sequential()
    # input layer
    model.add(tf.keras.layers.Flatten())
    # two hidden layers with relu activation
    model.add(tf.keras.layers.Dense(128,  activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(128,  activation=tf.nn.relu))
    # output classes : probability of attending the event and probability of not attending a event
    # how to give inputs and outputs?
    
    model.add(tf.keras.layers.Dense(2,  activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit()
#     what are xtrain and xtest and ytrain and ytest
#     we need the


if __name__ == '__main__':
    main()
