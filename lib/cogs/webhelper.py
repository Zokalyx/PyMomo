"""Helper functions for web rendering"""

import time
import math


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


def card_graph(card):
    """Returns a list of twoples representing the coordinates
    of the vertices of the polyline to be drawn"""
    data = card.stats["value"]
    twoples = []
    now = time.time()
    old = data[0][0]
    diff = now - old
    now_tuple = (now, card.value)
    full_data = [*data, now_tuple]
    max_bal = max(full_data, key=lambda x: x[1])[1]
    max_bal = 1 if max_bal == 0 else max_bal
    for raw_time, raw_bal in full_data:
        twoples.append(
            (round(100*(raw_time - old)/diff), 100 - round(100*raw_bal/max_bal))
        )
    return twoples


def time_ago_formatter(seconds):
    options = [
        {
            "name": "año",
            "seconds": 31556952
        },
        {
            "name": "mes",
            "seconds": 2592000
        },
        {
            "name": "semana",
            "seconds": 604800
        },
        {
            "name": "día",
            "seconds": 86400
        },
        {
            "name": "hora",
            "seconds": 3600
        },
        {
            "name": "minuto",
            "seconds": 60
        },
        {
            "name": "segundo",
            "seconds": 1
        },
    ]
    diff = time.time() - seconds

    for option in options:
        t_diff = math.floor(diff / option["seconds"])
        if t_diff != 0:
            unit = option["name"]
            break

    return f"{t_diff} {unit}{'' if t_diff == 1 else 's'}"