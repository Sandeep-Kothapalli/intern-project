import tensorflow as tf
import keras
import random
import pandas as pd
import os
from pprint import pprint


class eventNode:
    def __int__(self, event_id, latitude, longitude, event_time):
        self.event_id = event_id
        self.latitude = latitude
        self.longitude = longitude
        self.event_time = event_time

    def printNode(self):
        print(self.event_id, self.latitude, self.longitude, self.event_time)


def main():
    # events.csv taken from meetup api
    filePath = 'events.csv'
    eventData = pd.read_csv(filePath, nrows=10)
    events = eventData['event_id'].values.tolist()
    elat = eventData[['event_id', 'venue.lat']].set_index('event_id').T.to_dict()
    # pprint(elat)
    elong = eventData[['event_id', 'venue.lon']].set_index('event_id').T.to_dict()
    # pprint(elong)
    etime = eventData[['event_id', 'event_time']].set_index('event_id').T.to_dict()
    # pprint(etime)
    egroup = eventData[['event_id', 'group_id']].set_index('event_id').T.to_dict()
    # pprint(egroup)
    # rsvp is the event list
    # ersvp is the event list mapped to people that attended the corresponding event
    rsvp = eventData['event_id']
    strength = 10
    members = [i for i in range(strength)]
    ersvp = {}
    for i in range(len(rsvp)):
        ersvp[rsvp[i]] = random.sample(members, random.randint(0, len(members)))
    Du = {}
    for i in members:
        Du[i] = []
    for i in events:
        attend = eventNode()
        attend.event_id = i
        attend.latitude = elat[i]
        attend.longitude = elong[i]
        attend.event_time = etime[i]
        for j in ersvp[i]:
            Du[j].append(attend)

    # pprint(ersvp)
    # for i in range(strength):
    #     print(i)
    #     for events in Du[i]:
    #         events.printNode()



if __name__ == '__main__':
    main()
