# -*- encoding: utf-8 -*-
#
# Copyright © 2014 ZHAW SoE
#
# Authors: Lucas Graf <graflu0@students.zhaw.ch>
#          Toni Zehnder <zehndton@students.zhaw.ch>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Inspector for collecting data over SNMP"""

import urlparse

from ceilometer.hardware.inspector import base
from pysnmp.entity.rfc3413.oneliner import cmdgen


class SNMPException(Exception):
    pass


def parse_snmp_return(ret):
    """Check the return value of snmp operations

    :param ret: a tuple of (errorIndication, errorStatus, errorIndex, data)
                returned by pysnmp
    :return: a tuple of (err, data)
             err: True if error found, or False if no error found
             data: a string of error description if error found, or the
                   actual return data of the snmp operation
    """
    err = True
    (errIndication, errStatus, errIdx, varBinds) = ret
    if errIndication:
        data = errIndication
    elif errStatus:
        data = "%s at %s" % (errStatus.prettyPrint(),
                             errIdx and varBinds[int(errIdx) - 1] or "?")
    else:
        err = False
        data = varBinds
    return (err, data)

NETWORK_RX_COUNTER = 'net:received:average'
NETWORK_TX_COUNTER = 'net:transmitted:average'
NETWORK_RX_PACKET_COUNTER = 'net:received:packet:average'
NETWORK_TX_PACKET_COUNTER = 'net:transmitted:packet:average'


class SNMPInspector(base.Inspector):
    #CPU OIDs
    _cpu_1_min_load_oid = "1.3.6.1.4.1.2021.10.1.3.1"
    _cpu_5_min_load_oid = "1.3.6.1.4.1.2021.10.1.3.2"
    _cpu_15_min_load_oid = "1.3.6.1.4.1.2021.10.1.3.3"

    _cpu_user_time_oid = "1.3.6.1.4.1.2021.11.50.0"
    _cpu_nice_time_oid = "1.3.6.1.4.1.2021.11.51.0"
    _cpu_system_time_oid = "1.3.6.1.4.1.2021.11.52.0"
    _cpu_idle_time_percent_oid = "1.3.6.1.4.1.2021.11.11.0"

    #Memory OIDs
    _memory_total_oid = "1.3.6.1.4.1.2021.4.5.0"
    _memory_used_oid = "1.3.6.1.4.1.2021.4.6.0"

    #Disk OIDs
    _disk_index_oid = "1.3.6.1.4.1.2021.9.1.1"
    _disk_path_oid = "1.3.6.1.4.1.2021.9.1.2"
    _disk_device_oid = "1.3.6.1.4.1.2021.9.1.3"
    _disk_size_oid = "1.3.6.1.4.1.2021.9.1.6"
    _disk_used_oid = "1.3.6.1.4.1.2021.9.1.8"

    #Network Interface OIDs
    _interface_index_oid = "1.3.6.1.2.1.2.2.1.1"
    _interface_type_oid = "1.3.6.1.2.1.2.2.1.3"
    _interface_name_oid = "1.3.6.1.2.1.2.2.1.2"
    _interface_bandwidth_oid = "1.3.6.1.2.1.2.2.1.5"
    _interface_mac_oid = "1.3.6.1.2.1.2.2.1.6"
    _interface_ip_oid = "1.3.6.1.2.1.4.20.1.2"
    _interface_received_oid = "1.3.6.1.2.1.2.2.1.10"
    _interface_transmitted_oid = "1.3.6.1.2.1.2.2.1.16"
    _interface_error_oid = "1.3.6.1.2.1.2.2.1.20"
    _interface_inpak_oid = "1.3.6.1.2.1.2.2.1.11"
    _interface_outpak_oid = "1.3.6.1.2.1.2.2.1.17"

    #Default port and security name
    _port = 161
    _security_name = 'public'

    def __init__(self):
        super(SNMPInspector, self).__init__()
        self._cmdGen = cmdgen.CommandGenerator()

    def _get_or_walk_oid(self, oid, host, get=True):
        if get:
            func = self._cmdGen.getCmd
            ret_func = lambda x: x[0][1]
        else:
            func = self._cmdGen.nextCmd
            ret_func = lambda x: x
        ret = \
            func(cmdgen.CommunityData('server',
                                      self._get_security_name(host),
                                      1),
                 cmdgen.UdpTransportTarget((host.hostname,
                                           host.port or self._port)),
                 oid)
        (error, data) = parse_snmp_return(ret)
        if error:
            raise SNMPException("An error occurred, oid %(oid)s, "
                                "host %(host)s, %(err)s" % dict(oid=oid,
                                host=host.hostname, err=data))
        else:
            return ret_func(data)

    def _get_value_from_oid(self, oid, host):
        return self._get_or_walk_oid(oid, host, True)

    def _walk_oid(self, oid, host):
        return self._get_or_walk_oid(oid, host, False)

    def inspect_cpu(self, host):
        #get 1 minute load
        cpu_1_min_load = \
            str(self._get_value_from_oid(self._cpu_1_min_load_oid, host))
        #get 5 minute load
        cpu_5_min_load = \
            str(self._get_value_from_oid(self._cpu_5_min_load_oid, host))
        #get 15 minute load
        cpu_15_min_load = \
            str(self._get_value_from_oid(self._cpu_15_min_load_oid, host))
        #get cpu_used /100s to /s
        cpu_used = \
            (int(self._get_value_from_oid(self._cpu_user_time_oid, host)) +
             int(self._get_value_from_oid(self._cpu_nice_time_oid, host)) +
             int(self._get_value_from_oid(self._cpu_system_time_oid, host))
             ) / 100

        #get cpu_usage
        cpu_usage = \
            100 - (self._get_value_from_oid(self._cpu_idle_time_percent_oid,
                                            host))

        yield base.CPUStats(cpu_1_min=float(cpu_1_min_load),
                            cpu_5_min=float(cpu_5_min_load),
                            cpu_15_min=float(cpu_15_min_load),
                            cpu_used=float(cpu_used),
                            cpu_usage=float(cpu_usage))

    def inspect_memory(self, host):
        #get total memory
        total = self._get_value_from_oid(self._memory_total_oid, host)
        #get used memory
        used = self._get_value_from_oid(self._memory_used_oid, host)
        #usage memory
        usage = float(used) / float(total)
        usage = float(usage)
        usage = "%.2f" % usage
        usage = float(usage)
        usage = int(usage * 100)

        yield base.MemoryStats(total=int(total),
                               used=int(used),
                               usage=int(usage))

    def inspect_disk(self, host):
        disks = self._walk_oid(self._disk_index_oid, host)

        for disk in disks:
            for object_name, value in disk:
                path_oid = "%s.%s" % (self._disk_path_oid, str(value))
                path = self._get_value_from_oid(path_oid, host)
                device_oid = "%s.%s" % (self._disk_device_oid, str(value))
                device = self._get_value_from_oid(device_oid, host)
                size_oid = "%s.%s" % (self._disk_size_oid, str(value))
                size = self._get_value_from_oid(size_oid, host)
                used_oid = "%s.%s" % (self._disk_used_oid, str(value))
                used = self._get_value_from_oid(used_oid, host)

                disk = base.Disk(device=str(device),
                                 path=str(path))

                #usage disk
                usage = float(used) / float(size)
                usage = float(usage)
                usage = "%.2f" % usage
                usage = float(usage)
                usage = int(usage * 100)
                stats = base.DiskStats(size=int(size),
                                       used=int(used),
                                       usage=int(usage))

                yield (disk, stats)

    def inspect_network(self, host):
        #IF-MIB::ifTyp   softwareLoopback(24)  ethernetCsmacd(6)
        net_types = self._walk_oid(self._interface_type_oid, host)
        i = 0
        flag = 0
        for type in net_types:
            if flag == 1:
                break
            for object_name, value in type:
                if value == 24:
                    flag = 1
                    break
            i += 1

        sum_bandwidth = 0
        sum_rx_bytes = 0
        sum_tx_bytes = 0
        sum_error = 0
        sum_rx_packets = 0
        sum_tx_packets = 0
        sum_interface = base.Interface(name="", mac="", ip="")

        net_interfaces = self._walk_oid(self._interface_index_oid, host)
        j = 0
        for interface in net_interfaces:
            for object_name, value in interface:
                if j != i:
                    ip = self._get_ip_for_interface(host, value)
                    name_oid = "%s.%s" % (self._interface_name_oid,
                                          str(value))
                    name = self._get_value_from_oid(name_oid, host)
                    mac_oid = "%s.%s" % (self._interface_mac_oid,
                                         str(value))
                    mac = self._get_value_from_oid(mac_oid, host)
                    bw_oid = "%s.%s" % (self._interface_bandwidth_oid,
                                        str(value))
                    # bits/s to byte/s
                    bandwidth = self._get_value_from_oid(bw_oid, host) / 8
                    rx_oid = "%s.%s" % (self._interface_received_oid,
                                        str(value))
                    rx_bytes = self._get_value_from_oid(rx_oid, host)
                    tx_oid = "%s.%s" % (self._interface_transmitted_oid,
                                        str(value))
                    tx_bytes = self._get_value_from_oid(tx_oid, host)
                    error_oid = "%s.%s" % (self._interface_error_oid,
                                           str(value))
                    error = self._get_value_from_oid(error_oid, host)

                    inpak_oid = "%s.%s" % (self._interface_inpak_oid,
                                           str(value))
                    rx_packets = self._get_value_from_oid(inpak_oid, host)

                    outpak_oid = "%s.%s" % (self._interface_outpak_oid,
                                            str(value))
                    tx_packets = self._get_value_from_oid(outpak_oid, host)

                    adapted_mac = mac.prettyPrint().replace('0x', '')

                    interface = base.Interface(name=str(name),
                                               mac=adapted_mac,
                                               ip=str(ip))
                    sum_bandwidth += bandwidth
                    sum_rx_bytes += rx_bytes
                    sum_tx_bytes += tx_bytes
                    sum_error += error
                    sum_rx_packets += rx_packets
                    sum_tx_packets += tx_packets
                    sum_interface = interface
                j += 1
        stats = base.InterfaceStats(bandwidth=int(sum_bandwidth),
                                    rx_bytes=int(sum_rx_bytes),
                                    tx_bytes=int(sum_tx_bytes),
                                    error=int(sum_error),
                                    rx_packets=int(sum_rx_packets),
                                    tx_packets=int(sum_tx_packets))
        yield (sum_interface, stats)

    def _get_security_name(self, host):
        options = urlparse.parse_qs(host.query)
        return options.get('security_name', [self._security_name])[-1]

    def _get_ip_for_interface(self, host, interface_id):
        ip_addresses = self._walk_oid(self._interface_ip_oid, host)
        for ip in ip_addresses:
            for name, value in ip:
                if value == interface_id:
                    return str(name).replace(self._interface_ip_oid + ".", "")
