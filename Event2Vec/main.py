import tensorflow as tf
import keras
import random
import pandas as pd
import os
from pprint import pprint


def main():
    filePath = 'events.csv'
    eventData = pd.read_csv(filePath)
    # eventData.drop('description')
    # print(eventData.head())
    elat = eventData[['event_id', 'venue.lat']].set_index('event_id').T.to_dict('list')
    elong = eventData[['event_id', 'venue.lon']].set_index('event_id').T.to_dict('list')
    etime = eventData[['event_id', 'event_time']].set_index('event_id').T.to_dict('list')
    egroup = eventData[['event_id', 'group_id']].set_index('event_id').T.to_dict('list')
    rsvp = eventData['event_id']
    members = [random.randint(1, 100) for i in range(100)]
    ersvp = {}
    for i in range(len(rsvp)):
        ersvp[rsvp[i]] = [random.sample(members, random.randint(0, len(members)))]
    pprint(elat)


if __name__ == '__main__':
    main()