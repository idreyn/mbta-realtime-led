import requests
import json
import math
import time

from data import *
from util import *


class APIRequest(object):
    API_KEY = read('../API_KEY.txt').strip()

    @staticmethod
    def make_request(method, parameters=None):
        parameters = parameters or {}
        parameters['api_key'] = APIRequest.API_KEY
        parameters['format'] = 'json'
        t = json.loads(requests.get(
            'http://realtime.mbta.com/developer/api/v2/' + method + '/',
            params=parameters
        ).text)
        return t

    @staticmethod
    def stops_by_route(route):
        return APIRequest.make_request('stopsbyroute', {'route': route})


class Route(object):
    def __init__(self, stations, name, api_name=None, train_filter=None):
        self.name = name
        self.api_name = api_name or name
        self.stations = map(stations.get, ROUTES[name])
        self.stations_dict = {}
        for st in self.stations:
            self.stations_dict[st.name] = st
        self.train_filter = train_filter

    def get_trains(self):
        trains = []
        req = APIRequest.make_request(
            'vehiclesbyroute', {'route': self.api_name})
        if not req.get('direction'):
            return []
        for direction in req['direction']:
            for trip in direction['trip']:
                trains.append(Train(
                    trip['trip_name'],
                    trip['trip_id'],
                    (
                        float(trip['vehicle']['vehicle_lat']),
                        float(trip['vehicle']['vehicle_lon'])
                    ),
                    int(direction.get('direction_id') or '0'),
                    int(trip['vehicle']['vehicle_timestamp'])
                ))
        if self.train_filter:
            trains = filter(self.train_filter, trains)
        return trains

    def locate_train(self, train):
        between = min(
            pairwise(
                self.stations),
            key=lambda a_b: point_line_segment_distance(
                a_b[0].location,
                a_b[1].location,
                train.location))
        progress = point_distance(
            train.location,
            between[0].location
        ) / point_distance(
            between[0].location,
            between[1].location
        )
        if train.direction == 1:
            between = tuple(reversed(between))
            progress = 1 - progress
        return (between[0], between[1], progress)


class Routes(object):
    def __init__(self, stations):
        self.routes = {}
        for k in API_ROUTE_NAMES:
            self.routes[k] = Route(stations, k, API_ROUTE_NAMES[k])
        for k in API_ROUTE_FILTERS:
            self.routes[k].train_filter = API_ROUTE_FILTERS[k]

    def all(self):
        for k in self.routes:
            yield self.routes[k]

    def get(self, name):
        return self.routes[name]


class Train(object):
    def __init__(self, name, id, location, direction, timestamp):
        self.name = name
        self.id = id
        self.location = location
        self.direction = direction
        self.measurements = 1
        self.last_velocity = 0
        self.average_velocity = 0
        self.timestamp = timestamp


class Station(object):
    def __init__(self, name, location):
        self.lines = set()
        self.name = name
        self.location = location

    def __str__(self):
        return self.name

    def transfer_station(self):
        return len(self.lines) > 1


class Stations(object):
    def __init__(self):
        self.stations = {}
        govt_center = Station('Government Center', (42.359444, -71.059444))
        self.stations['Government Center'] = govt_center
        self.stations['Government Center'].lines = set(['Green', 'Blue'])
        for route in API_ROUTE_NAMES.values():
            res = APIRequest.stops_by_route(route)
            # print res
            stops = res['direction'][0]['stop']
            for s in stops:
                name = s['parent_station_name']
                station = Station(
                    name, (float(s['stop_lat']), float(s['stop_lon'])))
                if not self.stations.get(name):
                    self.stations[name] = station
                self.stations[name].lines.add(route.split('-')[0])

    def get(self, name):
        return self.stations.get(name)

    def get_location(self, name):
        station = self.stations.get(name)
        if not station:
            return False
        else:
            return station.location
