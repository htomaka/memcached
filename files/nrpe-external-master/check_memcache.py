#!/usr/bin/python

#---------------------------------------------------
# This file is Juju managed
#---------------------------------------------------

import memcache
import nagios_plugin
import sys
from optparse import OptionParser


def check_version(hosts_ports):
    output, errors = [], []
    mc = memcache.Client(hosts_ports)
    for host in mc.servers:
        host.connect()
        try:
            host.send_cmd("version")
            output.append(host.readline())
        except:
            errors.append(str(host))
    if errors:
        raise nagios_plugin.CriticalError("Problems with: %s" % ", ".join(errors))
    print ", ".join(output)


def main():
    usage = "%s [-H HOST] [-p PORT] -c check_type\n\n" \
        "For options, run '%s --help'" % (sys.argv[0], sys.argv[0])
    parser = OptionParser(usage)

    parser.add_option(
        '-H', '--hosts', type="string", nargs=1,
        dest="hosts", help="Comma separated list of hosts to check - defaults to 'localhost'"
    )
    parser.add_option(
        '-p', '--ports', type="string", nargs=1,
        dest="ports", help="Comma separated list of ports to check - defaults to 11211"
    )
    parser.add_option(
        '-c', '--check-type', type="string", nargs=1,
        dest="check_type", help="The type of check - Mandatory!"
    )

    (options, args) = parser.parse_args()

    if not options.hosts:
        options.hosts = 'localhost'
    if not options.ports:
        options.ports = '11211'

    hosts = options.hosts.split(",")
    ports = options.ports.split(",")

    if len(hosts) != len(ports):
        parser.error("You haven't specified the same number of hosts and ports")
    else:
        hosts_ports = []
        for num in range(len(hosts)):
            hosts_ports.append('%s:%s' % (hosts[num], ports[num]))

    if not options.check_type:
        parser.error("You must specify a type of check to perform")
    else:
        if options.check_type == 'version':
            nagios_plugin.try_check(check_version, hosts_ports)
        else:
            # Add to this list as other check types are implemented
            parser.error("Check types currently accepted: version")


if __name__ == "__main__":
    main()
