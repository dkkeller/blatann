import logging
from blatann.event_type import EventSource, Event
from blatann.nrf import nrf_types, nrf_events
from blatann import gatt
from blatann.waitables.event_waitable import EventWaitable
from blatann.exceptions import InvalidOperationException, InvalidStateException

logger = logging.getLogger(__name__)


class GattcWriter(object):
    _WRITE_OVERHEAD = 3
    _LONG_WRITE_OVERHEAD = 5
    _READ_OVERHEAD = 1

    def __init__(self, ble_device, peer):
        """
        :type ble_device: blatann.device.BleDevice
        :type peer: blatann.peer.Peer
        """
        self.ble_device = ble_device
        self.peer = peer
        self._on_write_complete = EventSource("On Write Complete", logger)
        self._busy = False
        self._data = ""
        self._handle = 0x0000
        self._offset = 0
        self.ble_device.ble_driver.event_subscribe(self._on_write_response, nrf_events.GattcEvtWriteResponse)
        self._len_bytes_written = 0

    @property
    def on_write_complete(self):
        """
        :rtype: Event
        """
        return self._on_write_complete

    def write(self, handle, data):
        if self._busy:
            raise InvalidStateException("Gattc Writer is busy")
        if len(data) == 0:
            raise ValueError("Data must be at least one byte")
        self._offset = 0
        self._handle = handle
        self._data = data
        logger.info("Starting write to handle {}, len: {}".format(self._handle, len(self._data)))
        self._write_next_chunk()
        self._busy = True
        return EventWaitable(self._on_write_complete)

    def _write_next_chunk(self):
        flags = nrf_types.BLEGattExecWriteFlag.unused
        if self._offset != 0 or len(self._data) > (self.peer.mtu_size - self._WRITE_OVERHEAD):
            write_operation = nrf_types.BLEGattWriteOperation.prepare_write_req
            self._len_bytes_written = self.peer.mtu_size - self._LONG_WRITE_OVERHEAD
            self._len_bytes_written = min(self._len_bytes_written, len(self._data)-self._offset)
            if self._len_bytes_written <= 0:
                write_operation = nrf_types.BLEGattWriteOperation.execute_write_req
                flags = nrf_types.BLEGattExecWriteFlag.prepared_write
        else:
            # Can write it all in a single
            write_operation = nrf_types.BLEGattWriteOperation.write_req
            self._len_bytes_written = len(self._data)

        data_to_write = self._data[self._offset:self._offset+self._len_bytes_written]
        write_params = nrf_types.BLEGattcWriteParams(write_operation, flags,
                                                     self._handle, data_to_write, self._offset)
        logger.info("Writing chunk: handle: {}, offset: {}, len: {}, op: {}".format(self._handle, self._offset,
                                                                                    len(data_to_write), write_operation))
        self.ble_device.ble_driver.ble_gattc_write(self.peer.conn_handle, write_params)

    def _on_write_response(self, driver, event):
        """
        :type event: nrf_events.GattcEvtWriteResponse
        """
        if event.conn_handle != self.peer.conn_handle or event.attr_handle != self._handle:
            return
        if event.status != nrf_events.BLEGattStatusCode.success:
            self._complete(event.status)

        # Write successful, update offset and check operation
        self._offset += self._len_bytes_written

        if event.write_op in [nrf_types.BLEGattWriteOperation.write_req, nrf_types.BLEGattWriteOperation.execute_write_req]:
            # Completed successfully
            self._complete()
        elif event.write_op == nrf_types.BLEGattWriteOperation.prepare_write_req:
            # Write next chunk (or execute if complete)
            self._write_next_chunk()
        else:
            logger.error("Got unknown write operation: {}".format(event))
            self._complete(nrf_types.BLEGattStatusCode.unknown)

    def _complete(self, status=nrf_events.BLEGattStatusCode.success):
        self._busy = False
        self._on_write_complete.notify(self._handle, status, self._data)


class GattcCharacteristic(gatt.Characteristic):
    def __init__(self, ble_device, peer, uuid, properties, declaration_handle, value_handle, cccd_handle=None):
        super(GattcCharacteristic, self).__init__(ble_device, peer, uuid, properties)
        self._on_notification = EventSource("On Notification", logger)
        self.declaration_handle = declaration_handle
        self.value_handle = value_handle
        self.cccd_handle = cccd_handle
        self.writer = GattcWriter(ble_device, peer)
        self._on_write_complete_event = EventSource("Write Complete", logger)
        self._on_ccd_write_complete_event = EventSource("CCCD Write Complete", logger)
        self.writer.on_write_complete.register(self._write_complete)
        self._value = ""

    @property
    def subscribable(self):
        return self._properties.notify or self._properties.indicate

    def subscribe(self, on_notification_handler, prefer_indications=False):
        if not self.subscribable:
            raise InvalidOperationException("Characteristic {} is not subscribable".format(self.uuid))
        if prefer_indications and self._properties.indicate or not self._properties.notify:
            value = gatt.SubscriptionState.INDICATION
        else:
            value = gatt.SubscriptionState.NOTIFY
        self._on_notification.register(on_notification_handler)
        self.writer.write(self.cccd_handle, gatt.SubscriptionState.to_buffer(value))
        return EventWaitable(self._on_ccd_write_complete_event)

    def unsubscribe(self):
        if not self.subscribable:
            raise InvalidOperationException("Characteristic {} is not subscribable".format(self.uuid))
        value = gatt.SubscriptionState.NOT_SUBSCRIBED
        self.writer.write(self.cccd_handle, gatt.SubscriptionState.to_buffer(value))
        return EventWaitable(self._on_ccd_write_complete_event)

    def _write_complete(self, handle, status, data):
        # Success, update the local value
        if handle == self.value_handle:
            if status == nrf_types.BLEGattStatusCode.success:
                self._value = data
            self._on_write_complete_event.notify(self, status, self._value)
        elif handle == self.cccd_handle:
            if status == nrf_types.BLEGattStatusCode.success:
                self.cccd_state = gatt.SubscriptionState.from_buffer(bytearray(data))
            self._on_ccd_write_complete_event.notify(self, status, self.cccd_state)

    @classmethod
    def from_discovered_characteristic(cls, ble_device, peer, nrf_characteristic):
        """
        :type nrf_characteristic: nrf_types.BLEGattCharacteristic
        """
        char_uuid = ble_device.uuid_manager.nrf_uuid_to_uuid(nrf_characteristic.uuid)
        properties = gatt.CharacteristicProperties.from_nrf_properties(nrf_characteristic.char_props)
        cccd_handle_list = [d.handle for d in nrf_characteristic.descs
                            if d.uuid == nrf_types.BLEUUID.Standard.cccd]
        cccd_handle = cccd_handle_list[0] if cccd_handle_list else None
        return GattcCharacteristic(ble_device, peer, char_uuid, properties,
                                   nrf_characteristic.handle_decl, nrf_characteristic.handle_value, cccd_handle)


class GattcService(gatt.Service):
    @property
    def characteristics(self):
        """
        :rtype: list of GattcCharacteristic
        """
        return self._characteristics

    @classmethod
    def from_discovered_service(cls, ble_device, peer, nrf_service):
        """
        :type ble_device: blatann.device.BleDevice
        :type peer: blatann.peer.Peripheral
        :type nrf_service: nrf_types.BLEGattService
        """
        service_uuid = ble_device.uuid_manager.nrf_uuid_to_uuid(nrf_service.uuid)
        service = GattcService(ble_device, peer, service_uuid, gatt.ServiceType.PRIMARY,
                               nrf_service.start_handle, nrf_service.end_handle)
        for c in nrf_service.chars:
            service.characteristics.append(GattcCharacteristic.from_discovered_characteristic(ble_device, peer, c))
        return service


class GattcDatabase(gatt.GattDatabase):
    def __init__(self, ble_device, peer):
        super(GattcDatabase, self).__init__(ble_device, peer)

    @property
    def services(self):
        """
        :rtype: list of GattcService
        """
        return self._services

    def iter_characteristics(self):
        for s in self.services:
            for c in s.characteristics:
                yield c

    def add_discovered_services(self, nrf_services):
        """
        :type nrf_services: list of nrf_types.BLEGattService
        """
        for service in nrf_services:
            self.services.append(GattcService.from_discovered_service(self.ble_device, self.peer, service))
