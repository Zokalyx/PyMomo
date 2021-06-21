"""Helper functions for web rendering"""

import time


def user_graph(user):
    """Returns a list of twoples representing the coordinates
    of the vertices of the polyline to be drawn"""
    data = user.stats["bal"]
    twoples = []
    now = time.time()
    old = data[0][0]
    diff = now - old
    now_tuple = (now, user.bal)
    full_data = [*data, now_tuple]
    max_bal = max(full_data, key=lambda x: x[1])[1]
    for raw_time, raw_bal in full_data:
        twoples.append((
            round(100*(raw_time - old)/diff), 100 - round(100*raw_bal/max_bal)
        ))
    return twoples