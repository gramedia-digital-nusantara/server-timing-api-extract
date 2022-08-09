import argparse
import json
import re
from typing import Dict, List
import requests
from prettytable import PrettyTable, MARKDOWN

import urllib3
urllib3.disable_warnings()


def doRequest(endpoint: str, host: str = None, method='GET'):
    hostHeaders = {'Host': host} if host != None else {}
    resp = requests.request(method=method, url=endpoint,
                            headers=hostHeaders, verify=False)

    if resp.status_code != 200:
        raise Exception(
            f'Error! Got response code {resp.status_code} instead 200.')

    if 'server-timing' not in resp.headers:
        raise Exception(
            '"server-timing" header is not found in response. Header key must in lowercase.')

    return resp.headers['server-timing'], len(resp.content)


def parseServerTiming(valueString: str):
    splitMetric = valueString.split(',')
    mapped = []
    regex = r'(?P<name>.*);desc="(?P<description>.*)";dur=(?P<duration>\d+)'

    for m in splitMetric:
        match = re.match(regex, m)
        if match == None:
            raise Exception(f'Failed to parse metric data: "{m}"')
        mapped.append(match.groupdict())
    return mapped


def toTable(data: List[Dict]):
    t = PrettyTable(['Name', 'Duration', 'Description'])
    t.align = 'l'
    t.align['Duration'] = 'r'
    for l in data:
        t.add_row([l['name'], f"{l['duration']} ms", l['description']])
    return str(t)


def customTable(data: List, headers=None):
    t = PrettyTable(headers)
    t.align = 'l'
    if headers is None:
        t.header = False
    for l in data:
        t.add_row(l)
    return str(t)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', help="Endpoints config path.", type=argparse.FileType('r'), required=True, metavar="FILE")
    args = parser.parse_args()

    # with open(args.config) as f:
    endpoints = json.load(args.config)

    for e in endpoints:
        print("#"*(len(e['name'])+8))
        print(f"##  {e['name']}  ##")
        print("#"*(len(e['name'])+8))
        print()

        svrTimData, bodySize = doRequest(
            e['url'],
            e['host'] if 'host' in e else None
        )
        parsed = parseServerTiming(svrTimData)

        info_data = [
            ['URL', e['url']],
            ['Body Size', f'{round(bodySize/1000)} kB'],
        ]

        if 'host' in e:
            info_data.insert(0, ['Host', e['host']])

        print('Info :')
        print(customTable(info_data))
        print()
        print('Timing Metrics :')
        print(toTable(parsed))
        print()
        print()
