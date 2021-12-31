# No comment
import json
import re


def check_line(db: 'list of dicts') -> tuple:
    result = [0, 0, 0, 0, 0, 0]
    for line in db:
        if line['bus_id'] == '' or type(line['bus_id']) != int:
            result[0] += 1
        if line['stop_id'] == '' or type(line['stop_id']) != int:
            result[1] += 1
        if type(line['stop_name']) != str or not re.match(r'([A-Z][a-z]+ )+(Road|Avenue|Street|Boulevard)$',
                                                          line['stop_name']):
            result[2] += 1
        if line['next_stop'] == '' or type(line['next_stop']) != int:
            result[3] += 1
        if type(line['stop_type']) != str or not (re.match(r'S$|O$|F$', line['stop_type']) or line['stop_type'] == ''):
            result[4] += 1
        if type(line['a_time']) != str or not re.match(r'([0-1][0-9]|2[0-3]):[0-5][0-9]$', line['a_time']):
            result[5] += 1
    return tuple([sum(result)] + result)


def print_errors(errors: tuple):
    print(f'Format validation: {errors[0]} errors')
    print(f'bus_id: {errors[1]}')
    print(f'stop_id: {errors[2]}')
    print(f'stop_name: {errors[3]}')
    print(f'next_stop: {errors[4]}')
    print(f'stop_type: {errors[5]}')
    print(f'a_time: {errors[6]}')


def find_lines_and_stops(db: 'list of dicts') -> dict:
    stops_of_buses = dict()
    for line in db:
        stops_of_buses[line['bus_id']] = stops_of_buses.get(line['bus_id'], 0) + 1
    return stops_of_buses


def print_stops_of_buses(stops_of_buses: dict):
    print('Line names and number of stops:')
    for key in stops_of_buses:
        print(f'bus_id: {key}, stops: {stops_of_buses[key]}')


def start_end_transfer_checker(db: 'list of dicts'):
    stops, transfer_stops, finish_stops = [], [], []
    db = sorted(db, key=lambda d: d['bus_id'])
    bus_id = None
    for i in range(len(db)):
        if bus_id != db[i]['bus_id']:
            if i == 0:
                if db[i]['stop_type'] == 'S':
                    stops.append(db[i]['stop_name'])
                    bus_id = db[i]['bus_id']
                else:
                    print(f'There is no start or end stop for the line: {db[i]["bus_id"]}.')
                    return
            elif db[i - 1]['stop_type'] == 'F' and db[i]['stop_type'] == 'S':
                finish_stops.append(db[i - 1]['stop_name'])
                stops.append(db[i]['stop_name'])
                bus_id = db[i]['bus_id']
            elif db[i - 1]['stop_type'] != 'F':
                print(f'There is no start or end stop for the line: {db[i - 1]["bus_id"]}.')
                return
            elif db[i]['stop_type'] != 'S':
                print(f'There is no start or end stop for the line: {db[i]["bus_id"]}.')
                return
        else:
            transfer_stops.append(db[i]['stop_name'])
    else:
        if db[i]['stop_type'] != 'F':
            print(f'There is no start or end stop for the line: {db[i]["bus_id"]}.')
            return
        else:
            finish_stops.append(db[i]['stop_name'])
    stops = list(set(stops))
    transfer_stops = [i for i in set(transfer_stops) if transfer_stops.count(i) > 1]
    finish_stops = list(set(finish_stops))
    return stops, transfer_stops, finish_stops


def time_test(db: 'list of tuple'):
    db = sorted(db, key=lambda d: d['bus_id'])
    errors = []

    def already_there(d: dict):
        for i in errors:
            if i['bus_id'] == d['bus_id']:
                return False
        return True

    def time_checker(time1: str, time2: str) -> bool:
        time1, time2 = time1.split(':'), time2.split(':')
        time1 = time1[0] * 60 + time1[1]
        time2 = time2[0] * 60 + time2[1]
        return time1 < time2

    for i in range(1, len(db)):
        if db[i - 1]['bus_id'] == db[i]['bus_id']:
            if not time_checker(db[i - 1]['a_time'], db[i]['a_time']) and already_there(db[i]):
                errors.append(db[i])
    print('Arrival time test:')
    if errors:
        for i in errors:
            print(f'bus_id line {i["bus_id"]}: wrong time on station {i["stop_name"]}')
    else:
        print('OK')


def on_demands_test(db: 'list of dict'):
    res = set()
    for i in db:
        if i['stop_type'] == 'O':
            res.update([i['stop_name']])
    for i in start_end_transfer_checker(db)[1:-1]:
        res &= set(i)
    print('On demand stops test:')
    if res:
        print('Wrong stop type:', sorted(res))
    else:
        print('OK')


if __name__ == '__main__':
    bus_data = json.loads(input())
    on_demands_test(bus_data)
