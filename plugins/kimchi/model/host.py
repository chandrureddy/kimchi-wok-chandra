#
# Project Kimchi
#
# Copyright IBM, Corp. 2014-2015
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import libvirt
import psutil

from wok.exception import InvalidOperation, InvalidParameter
from wok.exception import NotFoundError, OperationFailed
from wok.xmlutils.utils import xpath_get_text

import hostdev
from config import CapabilitiesModel
from tasks import TaskModel


HOST_STATS_INTERVAL = 1


class HostModel(object):
    def __init__(self, **kargs):
        self.conn = kargs['conn']
        self.objstore = kargs['objstore']
        self.task = TaskModel(**kargs)

    def lookup(self, *name):
        cpus = psutil.NUM_CPUS

        # psutil is unstable on how to get the number of
        # cpus, different versions call it differently
        if hasattr(psutil, 'cpu_count'):
            cpus = psutil.cpu_count()

        elif hasattr(psutil, '_psplatform'):
            for method_name in ['_get_num_cpus', 'get_num_cpus']:

                method = getattr(psutil._psplatform, method_name, None)
                if method is not None:
                    cpus = method()
                    break

        self.host_info['cpus'] = cpus
        self.host_info['memory'] = psutil.phymem_usage().total
        return self.host_info


class DevicesModel(object):
    def __init__(self, **kargs):
        self.conn = kargs['conn']
        self.caps = CapabilitiesModel(**kargs)
        self.cap_map = \
            {'net': libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_NET,
             'pci': libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_PCI_DEV,
             'scsi': libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_SCSI,
             'scsi_host': libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_SCSI_HOST,
             'storage': libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_STORAGE,
             'usb_device': libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_USB_DEV,
             'usb':
             libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_USB_INTERFACE}
        # TODO: when no longer supporting Libvirt < 1.0.5 distros
        # (like RHEL6) remove this verification and insert the
        # key 'fc_host' with the libvirt variable in the hash
        # declaration above.
        try:
            self.cap_map['fc_host'] = \
                libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_FC_HOST
        except AttributeError:
            self.cap_map['fc_host'] = None

    def get_list(self, _cap=None, _passthrough=None,
                 _passthrough_affected_by=None):
        if _passthrough_affected_by is not None:
            # _passthrough_affected_by conflicts with _cap and _passthrough
            if (_cap, _passthrough) != (None, None):
                raise InvalidParameter("KCHHOST0004E")
            return sorted(
                self._get_passthrough_affected_devs(_passthrough_affected_by))

        if _cap == 'fc_host':
            dev_names = self._get_devices_fc_host()
        else:
            dev_names = self._get_devices_with_capability(_cap)

        if _passthrough is not None and _passthrough.lower() == 'true':
            conn = self.conn.get()
            passthrough_names = [
                dev['name'] for dev in hostdev.get_passthrough_dev_infos(conn)]
            dev_names = list(set(dev_names) & set(passthrough_names))

        dev_names.sort()
        return dev_names

    def _get_devices_with_capability(self, cap):
        conn = self.conn.get()
        if cap is None:
            cap_flag = 0
        else:
            cap_flag = self.cap_map.get(cap)
            if cap_flag is None:
                return []
        return [name.name() for name in conn.listAllDevices(cap_flag)]

    def _get_passthrough_affected_devs(self, dev_name):
        conn = self.conn.get()
        info = DeviceModel(conn=self.conn).lookup(dev_name)
        affected = hostdev.get_affected_passthrough_devices(conn, info)
        return [dev_info['name'] for dev_info in affected]

    def _get_devices_fc_host(self):
        conn = self.conn.get()
        # Libvirt < 1.0.5 does not support fc_host capability
        if not self.caps.fc_host_support:
            ret = []
            scsi_hosts = self._get_devices_with_capability('scsi_host')
            for host in scsi_hosts:
                xml = conn.nodeDeviceLookupByName(host).XMLDesc(0)
                path = '/device/capability/capability/@type'
                if 'fc_host' in xpath_get_text(xml, path):
                    ret.append(host)
            return ret
        # Double verification to catch the case where the libvirt
        # supports fc_host but does not, for some reason, recognize
        # the libvirt.VIR_CONNECT_LIST_NODE_DEVICES_CAP_FC_HOST
        # attribute.
        if not self.cap_map['fc_host']:
            return conn.listDevices('fc_host', 0)
        return self._get_devices_with_capability('fc_host')


class DeviceModel(object):
    def __init__(self, **kargs):
        self.conn = kargs['conn']

    def lookup(self, nodedev_name):
        conn = self.conn.get()
        try:
            dev = conn.nodeDeviceLookupByName(nodedev_name)
        except:
            raise NotFoundError('KCHHOST0003E', {'name': nodedev_name})
        return hostdev.get_dev_info(dev)

