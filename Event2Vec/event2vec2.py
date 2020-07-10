import pickle
import tensorflow as tf
from tensorflow import keras
from pprint import pprint
import numpy as np
import scipy
from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense

# pickle that contains information in the following format
'''
elat - Key: event id, Value: Latitude of event location
elon - Key: event id, Value: Longitude of event location
etime - Key: event id, Value: Timestamp of event, convert this to hour of day, day of week, month of year format
ersvp - Key: event id, Value: List of tuples where each tuple (val1,val2) contains val1 as user_id who attended the event
egroup - Key: event id, Value: group_id that hosted the event
'''
ersvp = pickle.load(open("ersvp", "rb"))
egroup = pickle.load(open("egroup", "rb"))
elat = pickle.load(open("elat", "rb"))
elon = pickle.load(open("elon", "rb"))
etime = pickle.load(open("etime", "rb"))

def main():
    # location l is represented as {lat,long}
    # set of user profiles {e,lat,lon,time} of events user u attended in chronological order
    D = {}
    users = []

#     counting all users in all events
    for event in ersvp:
        for attendees in ersvp[event]:
            users.append(attendees[0])

    users = list(set(users))
    # dict to store user profiles
    for user in users:
        D[user] = []

    # removing redundant entries in ersvp list
    # other criteria can be added similarly
    for event in list(ersvp):
        # deleting events with non numeric event ID's
        if not event.isnumeric():
            del ersvp[event]
            continue
        # deleting events with strength < 20
        if (len(ersvp[event])) < 20:
            del ersvp[event]
            continue
        # deleting events not present in other dictionaries
        if event not in elat or event not in elon or event not in etime:
            del ersvp[event]
            continue

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

    # list of all items
    events = [event for event in ersvp]
    lats = [elat[event] for event in ersvp]
    longs = [elon[event] for event in ersvp]
    times = [datetime.utcfromtimestamp(etime[event] / 1000).strftime("%d/%m/%Y, %H:%M:%S") for event in ersvp]

    # D[u] = e1, lat1, lon1, time1
    # length of onehot vector
    one_hot_depth = len(events)
    # event2int and int2event mappings for creating one hot vectors with indices.
    events_mappings = {}
    times_mappings = {}
    location_mappings = {}

    for x in range(one_hot_depth):
        events_mappings[events[x]] = x
        times_mappings[tuple(times[x])] = x
        location_mappings[tuple([lats[x], longs[x]])] = x


    # one hot vectors for each type of entity.
    one_hot_event = {}
    one_hot_time = {}
    one_hot_location = {}
    # one hot vector for each type of entities' target.
    one_hot_event_target = {}
    one_hot_time_target = {}
    one_hot_location_target = {}
    # this loop creates a one hot vector for each user profile

    # D[u] = e1, lat1, lon1, time1

    for user in D:
        input_sequence = D[user][:-1]
        target = D[user][-1]

        one_hot_event[user] = [0] * one_hot_depth
        one_hot_time[user] = [0] * one_hot_depth
        one_hot_location[user] = [0]*one_hot_depth

        one_hot_event_target[user] = [0] * one_hot_depth
        one_hot_time_target[user] = [0] * one_hot_depth
        one_hot_location_target[user] = [0] * one_hot_depth

        for quad in input_sequence:
            one_hot_event[user][events_mappings[quad[0]]] = 1
            one_hot_time[user][times_mappings[quad[3]]] = 1
            one_hot_location[user][location_mappings[tuple([quad[1], quad[2]])]] = 1

        one_hot_event_target[user][target[0]] = 1
        one_hot_time_target[user][target[3]] = 1
        one_hot_location_target[user][target[tuple([target[1], target[2]])]] = 1

    # created onehot vectors
    event_model = Sequential()
    time_model = Sequential()
    location_model = Sequential()

    event_model.add(Dense(one_hot_depth, activation='softmax', input_shape=(1, len(one_hot_event))))
    time_model.add(Dense(one_hot_depth, activation='softmax', input_shape=(1,len(one_hot_time))))
    location_model.add(Dense(one_hot_depth, activation='softmax', input_shape=(1,len(one_hot_location))))

    event_model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy'],
    )

    event_model.fit(
        one_hot_event,
        one_hot_event_target,
        epochs=5,
        batch_size=32
    )
    
    time_model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy'],
    )

    time_model.fit(
        one_hot_time,
        one_hot_time_target,
        epochs=5,
        batch_size=32
    )

    location_model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy'],
    )

    event_model.fit(
        one_hot_location,
        one_hot_location_target,
        epochs=5,
        batch_size=32
    )















        












if __name__ == '__main__':
    main()
