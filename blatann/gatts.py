from collections import namedtuple
import threading
from blatann.nrf import nrf_types, nrf_events, nrf_observers
from blatann import gatt

_security_mapping = {
    gatt.SecurityLevel.NO_ACCESS: nrf_types.BLEGapSecModeType.NO_ACCESS,
    gatt.SecurityLevel.OPEN: nrf_types.BLEGapSecModeType.OPEN,
    gatt.SecurityLevel.JUST_WORKS: nrf_types.BLEGapSecModeType.ENCRYPTION,
    gatt.SecurityLevel.MITM: nrf_types.BLEGapSecModeType.MITM,

}


class GattsCharacteristic(gatt.Characteristic):
    def __init__(self, ble_device, peer, uuid, properties, value="", prefer_indications=True):
        super(GattsCharacteristic, self).__init__(ble_device, peer, uuid)
        self.properties = properties
        self.value = value
        self.prefer_indications = prefer_indications
        self._handler_lock = threading.Lock()
        self._on_write_handlers = []
        self._on_read_handlers = []
        self.ble_device.ble_driver.event_subscribe(self._on_gatts_write, nrf_events.GattsEvtWrite)
        self.ble_device.ble_driver.event_subscribe(self._on_rw_auth_request, nrf_events.GattsEvtReadWriteAuthorizeRequest)
        self._write_queued = False
        self._queued_write_chunks = []
        self.QueuedChunk = namedtuple("QueuedChunk", ["offset", "data"])

    def set_value(self, value, notify_client=False):
        pass

    def register_on_write(self, on_write):
        with self._handler_lock:
            self._on_write_handlers.append(on_write)

    def deregister_on_write(self, on_write):
        with self._handler_lock:
            if on_write in self._on_write_handlers:
                self._on_write_handlers.remove(on_write)

    def _handle_in_characteristic(self, attribute_handle):
        return attribute_handle in [self.value_handle, self.cccd_handle]

    def _execute_queued_write(self, write_op):
        self._write_queued = False
        if write_op == nrf_events.BLEGattsWriteOperation.exec_write_req_cancel:
            print("Cancelling write request")
        else:
            print("Executing write request")
            # TODO Assume that it was assembled properly. Error handling should go here
            new_value = bytearray()
            for chunk in self._queued_write_chunks:
                new_value += bytearray(chunk.data)
            print("New value: 0x{}".format(str(new_value).encode("hex")))
        self._queued_write_chunks = []

    def _on_gatts_write(self, driver, event):
        print("Got gatts write: {}".format(event))

    def _on_write_auth_request(self, write_event):
        """
        :type write_event: nrf_events.GattsEvtWrite
        """
        if write_event.write_op in [nrf_events.BLEGattsWriteOperation.exec_write_req_cancel,
                                    nrf_events.BLEGattsWriteOperation.exec_write_req_now] and self._write_queued:
            self._execute_queued_write(write_event.write_op)
            return

        if not self._handle_in_characteristic(write_event.attribute_handle):
            return
        params = nrf_types.BLEGattsAuthorizeParams(nrf_types.BLEGattStatusCode.success, True, write_event.offset, write_event.data)
        reply = nrf_types.BLEGattsRwAuthorizeReplyParams(write=params)

        if write_event.write_op == nrf_events.BLEGattsWriteOperation.prep_write_req:
            self._write_queued = True
            self._queued_write_chunks.append(self.QueuedChunk(write_event.offset, write_event.data))
        elif write_event.write_op == nrf_events.BLEGattsWriteOperation.write_req:
            self._on_gatts_write(None, write_event)
            return  # reply handled by function since it needs to be called first

        # TODO More logic

        return reply

    def _on_read_auth_request(self, read_event):
        """
        :type read_event: nrf_events.GattsEvtRead
        """
        if not self._handle_in_characteristic(read_event.attribute_handle):
            return
        params = nrf_types.BLEGattsAuthorizeParams(nrf_types.BLEGattStatusCode.success, False, read_event.offset)
        reply = nrf_types.BLEGattsRwAuthorizeReplyParams(read=params)
        if read_event.offset > len(self.value):
            params.gatt_status = nrf_types.BLEGattStatusCode.invalid_offset
        else:
            params.data = self.value[params.offset:]
        return reply

    def _on_rw_auth_request(self, driver, event):
        print("Got rw_auth_request: {}".format(event))
        if self.peer.conn_handle != event.conn_handle:
            print("incorrect conn_handle: {}".format(event.conn_handle))
            return
        if event.read:
            reply = self._on_read_auth_request(event.read)
        elif event.write:
            reply = self._on_write_auth_request(event.write)
        else:
            print("auth request was not read or write???")
            return
        if reply:
            self.ble_device.ble_driver.ble_gatts_rw_authorize_reply(event.conn_handle, reply)


class GattsService(gatt.Service):
    def add_characteristic(self, uuid, properties, initial_value=""):
        """

        :type uuid: blatann.uuid.Uuid
        :type properties: gatt.CharacteristicProperties
        :param initial_value:
        :return:
        """
        c = GattsCharacteristic(self.ble_device, self.peer, uuid, properties, initial_value)
        # Register UUID
        self.ble_device.uuid_manager.register_uuid(uuid)

        # Create property structure
        props = nrf_types.BLECharacteristicProperties(properties.broadcast, properties.read, False, properties.write,
                                                      properties.notify, properties.indicate, False)
        # Create cccd metadata if notify/indicate enabled
        if properties.notify or properties.indicate:
            cccd_metadata = nrf_types.BLEGattsAttrMetadata(read_auth=False, write_auth=False)
        else:
            cccd_metadata = None

        char_md = nrf_types.BLEGattsCharMetadata(props, cccd_metadata=cccd_metadata)
        security = _security_mapping[properties.security_level]
        attr_metadata = nrf_types.BLEGattsAttrMetadata(security, security, properties.variable_length,
                                                       read_auth=False, write_auth=True)
        attribute = nrf_types.BLEGattsAttribute(uuid.nrf_uuid, attr_metadata, properties.max_len, initial_value)

        handles = nrf_types.BLEGattsCharHandles()  # Populated in call
        self.ble_device.ble_driver.ble_gatts_characteristic_add(self.start_handle, char_md, attribute, handles)

        c.value_handle = handles.value_handle
        c.cccd_handle = handles.cccd_handle

        if c.cccd_handle != gatt.BLE_GATT_HANDLE_INVALID:
            self.end_handle = c.cccd_handle
        else:
            self.end_handle = c.value_handle

        self.characteristics.append(c)


class GattsDatabase(gatt.GattDatabase):
    def __init__(self, ble_device, peer):
        super(GattsDatabase, self).__init__(ble_device, peer)
        self.ble_device.ble_driver.event_subscribe(self._on_rw_auth_request,
                                                   nrf_events.GattsEvtReadWriteAuthorizeRequest)

    def add_service(self, uuid, service_type=gatt.ServiceType.PRIMARY):
        # Register UUID
        self.ble_device.uuid_manager.register_uuid(uuid)
        handle = nrf_types.BleGattHandle()
        # Call code to add service to driver
        self.ble_device.ble_driver.ble_gatts_service_add(service_type.value, uuid.nrf_uuid, handle)
        service = GattsService(self.ble_device, self.peer, uuid, service_type, handle.handle)
        service.start_handle = handle.handle
        service.end_handle = handle.handle
        self.services.append(service)
        return service

    def _on_rw_auth_request(self, driver, event):
        if not event.write:
            return
        if event.write.write_op not in [nrf_events.BLEGattsWriteOperation.exec_write_req_now, nrf_events.BLEGattsWriteOperation.exec_write_req_cancel]:
            return
        params = nrf_types.BLEGattsAuthorizeParams(nrf_types.BLEGattStatusCode.success, False)
        reply = nrf_types.BLEGattsRwAuthorizeReplyParams(write=params)
        self.ble_device.ble_driver.ble_gatts_rw_authorize_reply(event.conn_handle, reply)
