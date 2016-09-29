# hetzner-failover-ip
Simple Python script to get and set the failover IPs you have for your Hetzner's servers.

	Usage: HETZNER_USER='foo' HETZNER_PASS='bar' failoverip-hetzner.py -l | -f FAILOVER-IP | -f FAILOVER-IP -d DESTINATION-IP

	Options:
	--version             show program's version number and exit
	-h, --help            show this help message and exit
	-l, --list            print current failover IPs and their destinations
	-f FAILOVER-IP, --failover-ip=FAILOVER-IP
							the failover IP to query, or manipulate when used
							togehter with -d
	-d DESTINATION-IP, --destination-ip=DESTINATION-IP
							the IP to point to by the faiover IP defined with the
							-f parameter

	ivan@laptop% HETZNER_USER="foo" HETZNER_PASS="bar" ./failoverip-hetzner.py -l
	[
		{
			"failover": {
				"active_server_ip": "1.2.3.4",
				"ip": "5.6.7.8",
				"netmask": "255.255.255.255",
				"server_ip": "1.2.3.4",
				"server_number": 123456
			}
		},
		{
			"failover": {
				"active_server_ip": "1.2.3.4",
				"ip": "6.5.4.3",
				"netmask": "255.255.255.255",
				"server_ip": "2.3.4.5",
				"server_number": 654321
			}
		}
	]

	ivan@laptop% HETZNER_USER="foo" HETZNER_PASS="bar" ./failoverip-hetzner.py -f 5.6.7.8
	1.2.3.4

	ivan@laptop% HETZNER_USER="foo" HETZNER_PASS="bar" ./failoverip-hetzner.py -f 6.5.4.3
	1.2.3.4

	ivan@laptop% HETZNER_USER="foo" HETZNER_PASS="bar" ./failoverip-hetzner.py -f 6.5.4.3 -d 2.3.4.5
	2.3.4.5

	ivan@laptop% HETZNER_USER="foo" HETZNER_PASS="bar" ./failoverip-hetzner.py -f 6.5.4.3
	2.3.4.5

	ivan@laptop% HETZNER_USER="foo" HETZNER_PASS="bar" ./failoverip-hetzner.py -f 6.5.4.3 -d 1.2.3.4
	1.2.3.4

	ivan@laptop% HETZNER_USER="foo" HETZNER_PASS="bar" ./failoverip-hetzner.py -f 6.5.4.3
	1.2.3.4
