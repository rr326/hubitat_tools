import re
from pathlib import Path

SAMPLE_DATA=["2018-11-26 00:35:16.378\tWARN \tdev|166|Sonos - Bedroom 2 |Connection refused (Connection refused)"
"2018-11-26 00:35:16.424\tWARN \tdev|166|Sonos - Bedroom 2 |Connection refused (Connection refused)"]


LEVEL_INT = {
    'error': 10,
    'warn': 20,
    'info': 30,
    'debug': 40
}

def parse_log_line(line):
    linemod = line.encode('utf-8').decode('unicode-escape')
    if linemod[-1] == '\n':
        linemod = linemod[0:-1]
    if linemod[0] == '"' and linemod[-1] == '"':
        linemod = linemod[1:-1]
    fields = linemod.split('\t')
    fields2 = fields[2].split('|')
    data = {
        'time': fields[0].strip(),
        'level': fields[1].strip().lower(),
        'type': fields2[0].strip(),
        'id': fields2[1].strip(),
        'name': fields2[2].strip(),
        'msg': fields2[3].strip()
    }
    data['levelInt'] = LEVEL_INT[data['level']]

    return data


def test():
    with (Path(__file__).parent / 'data' / 'log_sample.txt').open(mode='r') as fp:
        log_lines = fp.readlines()

    for line in log_lines:
        data = parse_log_line(line)
        assert re.match(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\.\d\d\d', data['time'])
        assert data['level'] in ['error', 'warn', 'info', 'debug']
        assert re.match(r'\d*',data['id'])
        assert data['type'] in ['dev', 'app']
    print(f'Tested log parser on {len(log_lines)} log lines')

if __name__ == '__main__':
    test()