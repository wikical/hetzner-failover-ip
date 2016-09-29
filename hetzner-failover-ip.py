#!/usr/bin/python
# Copyright 2016 Ivan F. Villanueva B. <ivan@wikical.com>
# LICENSE: AGPLv3

from __future__ import print_function
import __main__ as main
import simplejson as json, base64, urllib2, sys, urllib, os
from optparse import OptionParser

parser = OptionParser(usage="HETZNER_USER='foo' HETZNER_PASS='bar' %prog -l | -f FAILOVER-IP | -f FAILOVER-IP -d DESTINATION-IP",
                      version="%prog 1.0")

parser.add_option("-l", "--list",
                  action="store_true", dest="list_action", default=False,
                  help="print current failover IPs and their destinations")
parser.add_option("-f", "--failover-ip",
                  dest="failover_ip",
                  help="the failover IP to query, or manipulate when used togehter with -d",
                  metavar="FAILOVER-IP")
parser.add_option("-d", "--destination-ip",
                  dest="destination_ip",
                  help="the IP to point to by the faiover IP defined with the -f parameter",
                  metavar="DESTINATION-IP")

(options, args) = parser.parse_args()

if len(args) != 0:
    parser.error("wrong number of arguments")

def request(url, key=None, value=None):
    assert key == value or (key and value)
    if url[0] == '/':
	url=url[1:]
    user = os.environ['HETZNER_USER']
    password = os.environ['HETZNER_PASS']
    request = urllib2.Request("https://robot-ws.your-server.de/{}".format(url))
    base64string = base64.b64encode('{}:{}'.format(user, password))
    request.add_header("Authorization", "Basic %s" % base64string)
    try:
        if key:
            data = urllib.urlencode({key:value})
	    return urllib2.urlopen(request, data)
	else:
	    return urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print("{} retuned error code {}: {}".format(url, e.code, e), file=sys.stderr)
        sys.exit(1)

def get_destination_ip(failover_ip):
    value = request('failover/{}'.format(failover_ip))
    return json.load(value)['failover']['active_server_ip']

def set_destination_ip(failover_ip, destination_ip):
    value = request('failover/{}'.format(failover_ip), 'active_server_ip', destination_ip)
    data = json.load(value)
    return data["failover"]["active_server_ip"]

if options.list_action:
    if options.failover_ip:
        print("{}: WARNING: failover IP ignored".format(main.__file__), file=sys.stderr)
    if options.destination_ip:
        print("{}: WARNING: destination IP ignored".format(main.__file__), file=sys.stderr)
    data = json.load(request('failover'))
    print(json.dumps(data, sort_keys=True, indent='    '))
    sys.exit(0)

if options.failover_ip:
    if not options.failover_ip in [i['failover']['ip'] for i in json.load(request('failover'))]:
        print("{}: ERROR: Given failover IP {} is not available.".format(main.__file__, options.failover_ip),
                file=sys.stderr)
        sys.exit(1)
    if options.destination_ip:
        if not options.destination_ip in [i['failover']['server_ip'] for i in json.load(request('failover'))]:
            print("{}: ERROR: Given destination IP {} is not available.".format(main.__file__, options.destination_ip),
                    file=sys.stderr)
            sys.exit(1)
        print(set_destination_ip(options.failover_ip, options.destination_ip))
        sys.exit(0)
    else:
        print(get_destination_ip(options.failover_ip))
        sys.exit(0)
else:
    if options.destination_ip:
        parser.error('destination IP was specified without a failover IP')
    else:
        parser.error('no parameter specified')
