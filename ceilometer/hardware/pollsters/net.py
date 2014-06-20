# -*- encoding: utf-8 -*-
#
# Copyright © 2013 ZHAW SoE
# Copyright © 2014 Intel Corp.
#
# Authors: Lucas Graf <graflu0@students.zhaw.ch>
#          Toni Zehnder <zehndton@students.zhaw.ch>
#          Lianhao Lu <lianhao.lu@intel.com>
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

from ceilometer.hardware import plugin
from ceilometer.hardware.pollsters import util
from ceilometer import sample


class _Base(plugin.HardwarePollster):

    CACHE_KEY = 'nic'
    INSPECT_METHOD = 'inspect_network'


class BandwidthBytesPollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.bandwidth.bytes',
                                          type=sample.TYPE_CUMULATIVE,
                                          unit='B',
                                          volume=info.bandwidth,
                                          res_metadata=nic,
                                          )


class IncomingBytesPollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.incoming.bytes',
                                          type=sample.TYPE_CUMULATIVE,
                                          unit='B',
                                          volume=info.rx_bytes,
                                          res_metadata=nic,
                                          )


class OutgoingBytesPollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.outgoing.bytes',
                                          type=sample.TYPE_CUMULATIVE,
                                          unit='B',
                                          volume=info.tx_bytes,
                                          res_metadata=nic,
                                          )


class OutgoingErrorsPollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.outgoing.errors',
                                          type=sample.TYPE_CUMULATIVE,
                                          unit='packet',
                                          volume=info.error,
                                          res_metadata=nic,
                                          )


class IncomingBytesRatePollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.incoming.bytes.rate',
                                          type=sample.TYPE_GAUGE,
                                          unit='B/s',
                                          volume=info.rx_bytes_rate,
                                          res_metadata=nic,
                                          )


class OutgoingBytesRatePollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.outgoing.bytes.rate',
                                          type=sample.TYPE_GAUGE,
                                          unit='B/s',
                                          volume=info.tx_bytes_rate,
                                          res_metadata=nic,
                                          )

                                          
class IncomingPacketsPollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.incoming.packets',
                                          type=sample.TYPE_CUMULATIVE,
                                          unit='packet',
                                          volume=info.rx_packets,
                                          res_metadata=nic,
                                          )


class OutgoingPacketsPollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.outgoing.packets',
                                          type=sample.TYPE_CUMULATIVE,
                                          unit='packet',
                                          volume=info.tx_packets,
                                          res_metadata=nic,
                                          )


class IncomingPacketsRatePollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.incoming.packets.rate',
                                          type=sample.TYPE_GAUGE,
                                          unit='packet/s',
                                          volume=info.rx_packets_rate,
                                          res_metadata=nic,
                                          )


class OutgoingPacketsRatePollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (nic, info) = c_data
        return util.make_sample_from_host(host,
                                          name='network.incoming.packets.rate',
                                          type=sample.TYPE_GAUGE,
                                          unit='packet/s',
                                          volume=info.tx_packets_rate,
                                          res_metadata=nic,
                                          )
