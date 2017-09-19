#
# Copyright (c) 2016 Nordic Semiconductor ASA
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
#   3. Neither the name of Nordic Semiconductor ASA nor the names of other
#   contributors to this software may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
#   4. This software must only be used in or with a processor manufactured by Nordic
#   Semiconductor ASA, or in or with a processor manufactured by a third party that
#   is used in combination with a processor manufactured by Nordic Semiconductor.
#
#   5. Any software provided in binary or object form under this license must not be
#   reverse engineered, decompiled, modified and/or disassembled.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import logging
from enum import Enum
from types import NoneType

from pc_ble_driver_py.exceptions import NordicSemiException
from blatann.nrf.nrf_dll_load import driver
import blatann.nrf.nrf_driver_types as util

logger = logging.getLogger(__name__)


# TODO:
# * Implement _all_ structs from ble_gap.h, ble_common.h, ble_gattc.h, ...


#################### Common ################
class BLEHci(Enum):
    success = driver.BLE_HCI_STATUS_CODE_SUCCESS
    unknown_btle_command = driver.BLE_HCI_STATUS_CODE_UNKNOWN_BTLE_COMMAND
    unknown_connection_identifier = driver.BLE_HCI_STATUS_CODE_UNKNOWN_CONNECTION_IDENTIFIER
    authentication_failure = driver.BLE_HCI_AUTHENTICATION_FAILURE
    pin_or_key_missing = driver.BLE_HCI_STATUS_CODE_PIN_OR_KEY_MISSING
    memory_capacity_exceeded = driver.BLE_HCI_MEMORY_CAPACITY_EXCEEDED
    connection_timeout = driver.BLE_HCI_CONNECTION_TIMEOUT
    command_disallowed = driver.BLE_HCI_STATUS_CODE_COMMAND_DISALLOWED
    invalid_btle_command_parameters = driver.BLE_HCI_STATUS_CODE_INVALID_BTLE_COMMAND_PARAMETERS
    remote_user_terminated_connection = driver.BLE_HCI_REMOTE_USER_TERMINATED_CONNECTION
    remote_dev_termination_due_to_low_resources = driver.BLE_HCI_REMOTE_DEV_TERMINATION_DUE_TO_LOW_RESOURCES
    remote_dev_termination_due_to_power_off = driver.BLE_HCI_REMOTE_DEV_TERMINATION_DUE_TO_POWER_OFF
    local_host_terminated_connection = driver.BLE_HCI_LOCAL_HOST_TERMINATED_CONNECTION
    unsupported_remote_feature = driver.BLE_HCI_UNSUPPORTED_REMOTE_FEATURE
    invalid_lmp_parameters = driver.BLE_HCI_STATUS_CODE_INVALID_LMP_PARAMETERS
    unspecified_error = driver.BLE_HCI_STATUS_CODE_UNSPECIFIED_ERROR
    lmp_response_timeout = driver.BLE_HCI_STATUS_CODE_LMP_RESPONSE_TIMEOUT
    lmp_pdu_not_allowed = driver.BLE_HCI_STATUS_CODE_LMP_PDU_NOT_ALLOWED
    instant_passed = driver.BLE_HCI_INSTANT_PASSED
    pairintg_with_unit_key_unsupported = driver.BLE_HCI_PAIRING_WITH_UNIT_KEY_UNSUPPORTED
    differen_transaction_collision = driver.BLE_HCI_DIFFERENT_TRANSACTION_COLLISION
    controller_busy = driver.BLE_HCI_CONTROLLER_BUSY
    conn_interval_unacceptable = driver.BLE_HCI_CONN_INTERVAL_UNACCEPTABLE
    directed_advertiser_timeout = driver.BLE_HCI_DIRECTED_ADVERTISER_TIMEOUT
    conn_terminated_due_to_mic_failure = driver.BLE_HCI_CONN_TERMINATED_DUE_TO_MIC_FAILURE
    conn_failed_to_be_established = driver.BLE_HCI_CONN_FAILED_TO_BE_ESTABLISHED


class NrfError(Enum):
    success = driver.NRF_SUCCESS
    svc_handler_missing = driver.NRF_ERROR_SVC_HANDLER_MISSING
    softdevice_not_enabled = driver.NRF_ERROR_SOFTDEVICE_NOT_ENABLED
    internal = driver.NRF_ERROR_INTERNAL
    no_mem = driver.NRF_ERROR_NO_MEM
    not_found = driver.NRF_ERROR_NOT_FOUND
    not_supported = driver.NRF_ERROR_NOT_SUPPORTED
    invalid_param = driver.NRF_ERROR_INVALID_PARAM
    invalid_state = driver.NRF_ERROR_INVALID_STATE
    invalid_length = driver.NRF_ERROR_INVALID_LENGTH
    invalid_flags = driver.NRF_ERROR_INVALID_FLAGS
    invalid_data = driver.NRF_ERROR_INVALID_DATA
    data_size = driver.NRF_ERROR_DATA_SIZE
    timeout = driver.NRF_ERROR_TIMEOUT
    null = driver.NRF_ERROR_NULL
    forbidden = driver.NRF_ERROR_FORBIDDEN
    invalid_addr = driver.NRF_ERROR_INVALID_ADDR
    busy = driver.NRF_ERROR_BUSY
    conn_count = driver.NRF_ERROR_CONN_COUNT
    resources = driver.NRF_ERROR_RESOURCES

    # sdm_lfclk_source_unknown                    = driver.NRF_ERROR_SDM_LFCLK_SOURCE_UNKNOWN
    # sdm_incorrect_interrupt_configuration       = driver.NRF_ERROR_SDM_INCORRECT_INTERRUPT_CONFIGURATION
    # sdm_incorrect_clenr0                        = driver.NRF_ERROR_SDM_INCORRECT_CLENR0

    # soc_mutex_already_taken                     = driver.NRF_ERROR_SOC_MUTEX_ALREADY_TAKEN
    # soc_nvic_interrupt_not_available            = driver.NRF_ERROR_SOC_NVIC_INTERRUPT_NOT_AVAILABLE
    # soc_nvic_interrupt_priority_not_allowed     = driver.NRF_ERROR_SOC_NVIC_INTERRUPT_PRIORITY_NOT_ALLOWED
    # soc_nvic_should_not_return                  = driver.NRF_ERROR_SOC_NVIC_SHOULD_NOT_RETURN
    # soc_power_mode_unknown                      = driver.NRF_ERROR_SOC_POWER_MODE_UNKNOWN
    # soc_power_pof_threshold_unknown             = driver.NRF_ERROR_SOC_POWER_POF_THRESHOLD_UNKNOWN
    # soc_power_off_should_not_return             = driver.NRF_ERROR_SOC_POWER_OFF_SHOULD_NOT_RETURN
    # soc_rand_not_enough_values                  = driver.NRF_ERROR_SOC_RAND_NOT_ENOUGH_VALUES
    # soc_ppi_invalid_channel                     = driver.NRF_ERROR_SOC_PPI_INVALID_CHANNEL
    # soc_ppi_invalid_group                       = driver.NRF_ERROR_SOC_PPI_INVALID_GROUP

    # ble_error_not_enabled                       = driver.BLE_ERROR_NOT_ENABLED
    # ble_error_invalid_conn_handle               = driver.BLE_ERROR_INVALID_CONN_HANDLE
    # ble_error_invalid_attr_handle               = driver.BLE_ERROR_INVALID_ATTR_HANDLE
    # ble_error_invalid_role                      = driver.BLE_ERROR_INVALID_ROLE

    # ble_error_gap_uuid_list_mismatch            = driver.BLE_ERROR_GAP_UUID_LIST_MISMATCH
    # ble_error_gap_discoverable_with_whitelist   = driver.BLE_ERROR_GAP_DISCOVERABLE_WITH_WHITELIST
    # ble_error_gap_invalid_ble_addr              = driver.BLE_ERROR_GAP_INVALID_BLE_ADDR
    # ble_error_gap_whitelist_in_use              = driver.BLE_ERROR_GAP_WHITELIST_IN_USE
    # ble_error_gap_device_identities_in_use      = driver.BLE_ERROR_GAP_DEVICE_IDENTITIES_IN_USE
    # ble_error_gap_device_identities_duplicate   = driver.BLE_ERROR_GAP_DEVICE_IDENTITIES_DUPLICATE

    # ble_error_gattc_proc_not_permitted          = driver.BLE_ERROR_GATTC_PROC_NOT_PERMITTED

    # ble_error_gatts_invalid_attr_type           = driver.BLE_ERROR_GATTS_INVALID_ATTR_TYPE
    # ble_error_gatts_sys_attr_missing            = driver.BLE_ERROR_GATTS_SYS_ATTR_MISSING


class BLEUUIDBase(object):
    def __init__(self, vs_uuid_base=None, uuid_type=None):
        assert isinstance(vs_uuid_base, (list, NoneType)), 'Invalid argument type'
        assert isinstance(uuid_type, (int, long, NoneType)), 'Invalid argument type'
        if vs_uuid_base is None:
            self.base = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00,
                         0x80, 0x00, 0x00, 0x80, 0x5F, 0x9B, 0x34, 0xFB]
            self.def_base = True
        else:
            self.base = vs_uuid_base
            self.def_base = False

        if uuid_type is None:
            self.type = driver.BLE_UUID_TYPE_BLE
        else:
            self.type = uuid_type

    def __eq__(self, other):
        if not isinstance(other, BLEUUIDBase):
            return False
        if self.base != other.base:
            return False
        if self.type != other.type:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_c(cls, uuid):
        if uuid.type == driver.BLE_UUID_TYPE_BLE:
            return cls(uuid_type=uuid.type)
        else:
            return cls([0] * 16, uuid_type=uuid.type)  # TODO: Hmmmm? [] or [None]*16? what?

    def to_c(self):
        lsb_list = self.base[::-1]
        self.__array = util.list_to_uint8_array(lsb_list)
        uuid = driver.ble_uuid128_t()
        uuid.uuid128 = self.__array.cast()
        return uuid


class BLEUUID(object):
    class Standard(Enum):
        unknown = 0x0000
        service_primary = 0x2800
        service_secondary = 0x2801
        characteristic = 0x2803
        cccd = 0x2902
        battery_level = 0x2A19
        heart_rate = 0x2A37

    def __init__(self, value, base=BLEUUIDBase()):
        assert isinstance(base, BLEUUIDBase), 'Invalid argument type'
        self.base = base
        if self.base.def_base:
            try:
                self.value = value if isinstance(value, BLEUUID.Standard) else BLEUUID.Standard(value)
            except ValueError:
                self.value = value
        else:
            self.value = value

    def get_value(self):
        if isinstance(self.value, BLEUUID.Standard):
            return self.value.value
        return self.value

    def as_array(self):
        base_and_value = self.base.base[:]
        base_and_value[2] = (self.get_value() >> 8) & 0xff
        base_and_value[3] = (self.get_value() >> 0) & 0xff
        return base_and_value

    def __str__(self):
        if isinstance(self.value, BLEUUID.Standard):
            return '0x{:04X} ({})'.format(self.value.value, self.value)
        elif self.base.type == driver.BLE_UUID_TYPE_BLE and self.base.def_base:
            return '0x{:04X}'.format(self.value)
        else:
            base_and_value = self.base.base[:]
            base_and_value[2] = (self.value >> 8) & 0xff
            base_and_value[3] = (self.value >> 0) & 0xff
            return '0x{}'.format(''.join(['{:02X}'.format(i) for i in base_and_value]))

    def __eq__(self, other):
        if not isinstance(other, BLEUUID):
            return False
        if not self.base == other.base:
            return False
        if not self.value == other.value:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_c(cls, uuid):
        return cls(value=uuid.uuid, base=BLEUUIDBase.from_c(uuid))  # TODO: Is this correct?

    def to_c(self):
        assert self.base.type is not None, 'Vendor specific UUID not registered'
        uuid = driver.ble_uuid_t()
        if isinstance(self.value, BLEUUID.Standard):
            uuid.uuid = self.value.value
        else:
            uuid.uuid = self.value
        uuid.type = self.base.type
        return uuid

    @classmethod
    def from_array(cls, uuid_array_lt):
        base = list(reversed(uuid_array_lt))
        uuid = (base[2] << 8) + base[3]
        base[2] = 0
        base[3] = 0
        return cls(value=uuid, base=BLEUUIDBase(base, 0))


class BLEEnableParams(object):
    def __init__(self,
                 vs_uuid_count,
                 service_changed,
                 periph_conn_count,
                 central_conn_count,
                 central_sec_count,
                 attr_tab_size=driver.BLE_GATTS_ATTR_TAB_SIZE_DEFAULT):
        self.vs_uuid_count = vs_uuid_count
        self.attr_tab_size = attr_tab_size
        self.service_changed = service_changed
        self.periph_conn_count = periph_conn_count
        self.central_conn_count = central_conn_count
        self.central_sec_count = central_sec_count

    def to_c(self):
        ble_enable_params = driver.ble_enable_params_t()
        ble_enable_params.common_enable_params.p_conn_bw_counts = None
        ble_enable_params.common_enable_params.vs_uuid_count = self.vs_uuid_count
        ble_enable_params.gatts_enable_params.attr_tab_size = self.attr_tab_size
        ble_enable_params.gatts_enable_params.service_changed = self.service_changed
        ble_enable_params.gap_enable_params.periph_conn_count = self.periph_conn_count
        ble_enable_params.gap_enable_params.central_conn_count = self.central_conn_count
        ble_enable_params.gap_enable_params.central_sec_count = self.central_sec_count

        return ble_enable_params


class BLEGapSecStatus(Enum):
    success = driver.BLE_GAP_SEC_STATUS_SUCCESS
    timeout = driver.BLE_GAP_SEC_STATUS_TIMEOUT
    pdu_invalid = driver.BLE_GAP_SEC_STATUS_PDU_INVALID
    passkey_entry_failed = driver.BLE_GAP_SEC_STATUS_PASSKEY_ENTRY_FAILED
    oob_not_available = driver.BLE_GAP_SEC_STATUS_OOB_NOT_AVAILABLE
    auth_req = driver.BLE_GAP_SEC_STATUS_AUTH_REQ
    confirm_value = driver.BLE_GAP_SEC_STATUS_CONFIRM_VALUE
    pairing_not_supp = driver.BLE_GAP_SEC_STATUS_PAIRING_NOT_SUPP
    enc_key_size = driver.BLE_GAP_SEC_STATUS_ENC_KEY_SIZE
    smp_cmd_unsupported = driver.BLE_GAP_SEC_STATUS_SMP_CMD_UNSUPPORTED
    unspecified = driver.BLE_GAP_SEC_STATUS_UNSPECIFIED
    repeated_attempts = driver.BLE_GAP_SEC_STATUS_REPEATED_ATTEMPTS
    invalid_params = driver.BLE_GAP_SEC_STATUS_INVALID_PARAMS
    dhkey_failure = driver.BLE_GAP_SEC_STATUS_DHKEY_FAILURE
    num_comp_failure = driver.BLE_GAP_SEC_STATUS_NUM_COMP_FAILURE
    br_edr_in_prog = driver.BLE_GAP_SEC_STATUS_BR_EDR_IN_PROG
    x_trans_key_disallowed = driver.BLE_GAP_SEC_STATUS_X_TRANS_KEY_DISALLOWED


#################### Gap ##################
class BLEGapAdvType(Enum):
    connectable_undirected = driver.BLE_GAP_ADV_TYPE_ADV_IND
    connectable_directed = driver.BLE_GAP_ADV_TYPE_ADV_DIRECT_IND
    scanable_undirected = driver.BLE_GAP_ADV_TYPE_ADV_SCAN_IND
    non_connectable_undirected = driver.BLE_GAP_ADV_TYPE_ADV_NONCONN_IND


class BLEGapRoles(Enum):
    invalid = driver.BLE_GAP_ROLE_INVALID
    periph = driver.BLE_GAP_ROLE_PERIPH
    central = driver.BLE_GAP_ROLE_CENTRAL


class BLEGapTimeoutSrc(Enum):
    advertising = driver.BLE_GAP_TIMEOUT_SRC_ADVERTISING
    security_req = driver.BLE_GAP_TIMEOUT_SRC_SECURITY_REQUEST
    scan = driver.BLE_GAP_TIMEOUT_SRC_SCAN
    conn = driver.BLE_GAP_TIMEOUT_SRC_CONN


class BLEGapAdvParams(object):
    def __init__(self, interval_ms, timeout_s):
        self.interval_ms = interval_ms
        self.timeout_s = timeout_s

    def to_c(self):
        adv_params = driver.ble_gap_adv_params_t()
        adv_params.type = BLEGapAdvType.connectable_undirected.value
        adv_params.p_peer_addr = None  # Undirected advertisement.
        adv_params.fp = driver.BLE_GAP_ADV_FP_ANY
        adv_params.p_whitelist = None
        adv_params.interval = util.msec_to_units(self.interval_ms,
                                                 util.UNIT_0_625_MS)
        adv_params.timeout = self.timeout_s

        return adv_params


class BLEGapScanParams(object):
    def __init__(self, interval_ms, window_ms, timeout_s):
        self.interval_ms = interval_ms
        self.window_ms = window_ms
        self.timeout_s = timeout_s

    def to_c(self):
        scan_params = driver.ble_gap_scan_params_t()
        scan_params.active = True
        scan_params.selective = False
        scan_params.p_whitelist = None
        scan_params.interval = util.msec_to_units(self.interval_ms,
                                                  util.UNIT_0_625_MS)
        scan_params.window = util.msec_to_units(self.window_ms,
                                                util.UNIT_0_625_MS)
        scan_params.timeout = self.timeout_s

        return scan_params


class BLEGapConnParams(object):
    def __init__(self, min_conn_interval_ms, max_conn_interval_ms, conn_sup_timeout_ms, slave_latency):
        self.min_conn_interval_ms = min_conn_interval_ms
        self.max_conn_interval_ms = max_conn_interval_ms
        self.conn_sup_timeout_ms = conn_sup_timeout_ms
        self.slave_latency = slave_latency

    @classmethod
    def from_c(cls, conn_params):
        return cls(min_conn_interval_ms=util.units_to_msec(conn_params.min_conn_interval,
                                                           util.UNIT_1_25_MS),
                   max_conn_interval_ms=util.units_to_msec(conn_params.max_conn_interval,
                                                           util.UNIT_1_25_MS),
                   conn_sup_timeout_ms=util.units_to_msec(conn_params.conn_sup_timeout,
                                                          util.UNIT_10_MS),
                   slave_latency=conn_params.slave_latency)

    def to_c(self):
        conn_params = driver.ble_gap_conn_params_t()
        conn_params.min_conn_interval = util.msec_to_units(self.min_conn_interval_ms,
                                                           util.UNIT_1_25_MS)
        conn_params.max_conn_interval = util.msec_to_units(self.max_conn_interval_ms,
                                                           util.UNIT_1_25_MS)
        conn_params.conn_sup_timeout = util.msec_to_units(self.conn_sup_timeout_ms,
                                                          util.UNIT_10_MS)
        conn_params.slave_latency = self.slave_latency

        return conn_params

    def __str__(self):
        return "%s(interval: [%r-%r] ms, timeout: %r ms, latency: %r)" % (
            self.__class__.__name__, self.min_conn_interval_ms, self.max_conn_interval_ms,
            self.conn_sup_timeout_ms, self.slave_latency
        )


class BLEGapAddr(object):
    class Types(Enum):
        public = driver.BLE_GAP_ADDR_TYPE_PUBLIC
        random_static = driver.BLE_GAP_ADDR_TYPE_RANDOM_STATIC
        random_private_resolvable = driver.BLE_GAP_ADDR_TYPE_RANDOM_PRIVATE_RESOLVABLE
        random_private_non_resolvable = driver.BLE_GAP_ADDR_TYPE_RANDOM_PRIVATE_NON_RESOLVABLE

    def __init__(self, addr_type, addr):
        assert isinstance(addr_type, BLEGapAddr.Types), 'Invalid argument type'
        self.addr_type = addr_type
        self.addr = addr

    @classmethod
    def from_c(cls, addr):
        addr_list = util.uint8_array_to_list(addr.addr, driver.BLE_GAP_ADDR_LEN)
        addr_list.reverse()
        return cls(addr_type=BLEGapAddr.Types(addr.addr_type),
                   addr=addr_list)

    @classmethod
    def from_string(cls, addr_string):
        addr, addr_flag = addr_string.split(',')
        addr_list = [int(i, 16) for i in addr.split(':')]

        # print addr_string, addr_list[-1], addr_list[-1] & 0b11000000, 0b11000000
        # print addr_string, addr_list[-1], addr_list[-1] & 0b10000000, 0b10000000
        if addr_flag in ['p', 'public']:
            addr_type = BLEGapAddr.Types.public
        elif (addr_list[0] & 0b11000000) == 0b00000000:
            addr_type = BLEGapAddr.Types.random_private_non_resolvable
        elif (addr_list[0] & 0b11000000) == 0b01000000:
            addr_type = BLEGapAddr.Types.random_private_resolvable
        elif (addr_list[0] & 0b11000000) == 0b11000000:
            addr_type = BLEGapAddr.Types.random_static
        else:
            raise ValueError("Provided random address do not follow rules")  # TODO: Improve error message

        return cls(addr_type, addr_list)

    def to_c(self):
        addr_array = util.list_to_uint8_array(self.addr[::-1])
        addr = driver.ble_gap_addr_t()
        addr.addr_type = self.addr_type.value
        addr.addr = addr_array.cast()
        return addr

    def get_addr_type_str(self):
        if self.addr_type == BLEGapAddr.Types.public:
            return 'public'
        elif self.addr_type == BLEGapAddr.Types.random_private_non_resolvable:
            return 'nonres'
        elif self.addr_type == BLEGapAddr.Types.random_private_resolvable:
            return 'res'
        elif self.addr_type == BLEGapAddr.Types.random_static:
            return 'static'
        else:
            return 'err {0:02b}'.format((self.AddressLtlEnd[-1] >> 6) & 0b11)

    def get_addr_str(self):
        return '"%s" (% 6s)' % (self, self.get_addr_type_str())

    def __eq__(self, other):
        if not isinstance(other, BLEGapAddr):
            other = BLEGapAddr.from_string(str(other))
        return str(self) == str(other)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return str(self)

    def get_addr_flag(self):
        return 'p' if self.addr_type == BLEGapAddr.Types.public else 'r'

    def __str__(self):
        return '%s,%s' % (':'.join(['%02X' % i for i in self.addr]), self.get_addr_flag())

    def __repr__(self):
        return "%s.from_string('%s,%s')" % (self.__class__.__name__,
                                            ':'.join(['%02X' % i for i in self.addr]), self.get_addr_flag())


class BLEAdvData(object):
    class Types(Enum):
        flags = driver.BLE_GAP_AD_TYPE_FLAGS
        service_16bit_uuid_more_available = driver.BLE_GAP_AD_TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE
        service_16bit_uuid_complete = driver.BLE_GAP_AD_TYPE_16BIT_SERVICE_UUID_COMPLETE
        service_32bit_uuid_more_available = driver.BLE_GAP_AD_TYPE_32BIT_SERVICE_UUID_MORE_AVAILABLE
        service_32bit_uuid_complete = driver.BLE_GAP_AD_TYPE_32BIT_SERVICE_UUID_COMPLETE
        service_128bit_uuid_more_available = driver.BLE_GAP_AD_TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE
        service_128bit_uuid_complete = driver.BLE_GAP_AD_TYPE_128BIT_SERVICE_UUID_COMPLETE
        short_local_name = driver.BLE_GAP_AD_TYPE_SHORT_LOCAL_NAME
        complete_local_name = driver.BLE_GAP_AD_TYPE_COMPLETE_LOCAL_NAME
        tx_power_level = driver.BLE_GAP_AD_TYPE_TX_POWER_LEVEL
        class_of_device = driver.BLE_GAP_AD_TYPE_CLASS_OF_DEVICE
        simple_pairing_hash_c = driver.BLE_GAP_AD_TYPE_SIMPLE_PAIRING_HASH_C
        simple_pairing_randimizer_r = driver.BLE_GAP_AD_TYPE_SIMPLE_PAIRING_RANDOMIZER_R
        security_manager_tk_value = driver.BLE_GAP_AD_TYPE_SECURITY_MANAGER_TK_VALUE
        security_manager_oob_flags = driver.BLE_GAP_AD_TYPE_SECURITY_MANAGER_OOB_FLAGS
        slave_connection_interval_range = driver.BLE_GAP_AD_TYPE_SLAVE_CONNECTION_INTERVAL_RANGE
        solicited_sevice_uuids_16bit = driver.BLE_GAP_AD_TYPE_SOLICITED_SERVICE_UUIDS_16BIT
        solicited_sevice_uuids_128bit = driver.BLE_GAP_AD_TYPE_SOLICITED_SERVICE_UUIDS_128BIT
        service_data = driver.BLE_GAP_AD_TYPE_SERVICE_DATA
        public_target_address = driver.BLE_GAP_AD_TYPE_PUBLIC_TARGET_ADDRESS
        random_target_address = driver.BLE_GAP_AD_TYPE_RANDOM_TARGET_ADDRESS
        appearance = driver.BLE_GAP_AD_TYPE_APPEARANCE
        advertising_interval = driver.BLE_GAP_AD_TYPE_ADVERTISING_INTERVAL
        le_bluetooth_device_address = driver.BLE_GAP_AD_TYPE_LE_BLUETOOTH_DEVICE_ADDRESS
        le_role = driver.BLE_GAP_AD_TYPE_LE_ROLE
        simple_pairng_hash_c256 = driver.BLE_GAP_AD_TYPE_SIMPLE_PAIRING_HASH_C256
        simple_pairng_randomizer_r256 = driver.BLE_GAP_AD_TYPE_SIMPLE_PAIRING_RANDOMIZER_R256
        service_data_32bit_uuid = driver.BLE_GAP_AD_TYPE_SERVICE_DATA_32BIT_UUID
        service_data_128bit_uuid = driver.BLE_GAP_AD_TYPE_SERVICE_DATA_128BIT_UUID
        uri = driver.BLE_GAP_AD_TYPE_URI
        information_3d_data = driver.BLE_GAP_AD_TYPE_3D_INFORMATION_DATA
        manufacturer_specific_data = driver.BLE_GAP_AD_TYPE_MANUFACTURER_SPECIFIC_DATA

    def __init__(self, **kwargs):
        self.records = dict()
        for k in kwargs:
            self.records[BLEAdvData.Types[k]] = kwargs[k]

    def to_c(self):
        data_list = list()
        for k in self.records:
            data_list.append(len(self.records[k]) + 1)  # add type length
            data_list.append(k.value)
            if isinstance(self.records[k], str):
                data_list.extend([ord(c) for c in self.records[k]])

            elif isinstance(self.records[k], list):
                data_list.extend(self.records[k])

            else:
                raise NordicSemiException('Unsupported value type: 0x{:02X}'.format(type(self.records[k])))

        data_len = len(data_list)
        if data_len == 0:
            return data_len, None
        else:
            self.__data_array = util.list_to_uint8_array(data_list)
            return data_len, self.__data_array.cast()

    @classmethod
    def from_c(cls, adv_report_evt):
        ad_list = util.uint8_array_to_list(adv_report_evt.data, adv_report_evt.dlen)
        ble_adv_data = cls()
        index = 0
        while index < len(ad_list):
            try:
                ad_len = ad_list[index]
                ad_type = ad_list[index + 1]
                offset = index + 2
                key = BLEAdvData.Types(ad_type)
                ble_adv_data.records[key] = ad_list[offset: offset + ad_len - 1]
            except ValueError:
                logger.error('Invalid advertising data type: 0x{:02X}'.format(ad_type))
                pass
            except IndexError:
                logger.error('Invalid advertising data: {}'.format(ad_list))
                return ble_adv_data
            index += (ad_len + 1)

        return ble_adv_data


#################### SMP ##################

class BLEGapSecMode(object):
    def __init__(self, sec_mode, level):
        self.sm = sec_mode
        self.level = level

    def to_c(self):
        params = driver.ble_gap_conn_sec_mode_t()
        params.sm = self.sm
        params.lv = self.level
        return params

    @classmethod
    def from_c(cls, params):
        return cls(params.sm, params.lv)


class BLEGapSecModeType(object):
    NO_ACCESS = BLEGapSecMode(0, 0)
    OPEN = BLEGapSecMode(1, 1)
    ENCRYPTION = BLEGapSecMode(1, 2)
    MITM = BLEGapSecMode(1, 3)
    LESC_MITM = BLEGapSecMode(1, 4)
    SIGN_OR_ENCRYPT = BLEGapSecMode(2, 1)
    SIGN_OR_ENCRYPT_MITM = BLEGapSecMode(2, 2)


class BLEGapSecLevels(object):
    def __init__(self, lv1, lv2, lv3, lv4):
        self.lv1 = lv1
        self.lv2 = lv2
        self.lv3 = lv3
        self.lv4 = lv4

    @classmethod
    def from_c(cls, sec_level):
        return cls(lv1=sec_level.lv1,
                   lv2=sec_level.lv2,
                   lv3=sec_level.lv3,
                   lv4=sec_level.lv4)

    def to_c(self):
        sec_level = driver.ble_gap_sec_levels_t()
        sec_level.lv1 = self.lv1
        sec_level.lv2 = self.lv2
        sec_level.lv3 = self.lv3
        sec_level.lv4 = self.lv4
        return sec_level

    def __repr__(self):
        return "%s(lv1=%r, lv2=%r, lv3=%r, lv4=%r)" % (self.__class__.__name__,
                                                       self.lv1, self.lv2, self.lv3, self.lv4)


class BLEGapSecKeyDist(object):
    def __init__(self, enc_key=False, id_key=False, sign_key=False, link_key=False):
        self.enc_key = enc_key
        self.id_key = id_key
        self.sign_key = sign_key
        self.link_key = link_key

    @classmethod
    def from_c(cls, kdist):
        return cls(enc_key=kdist.enc,
                   id_key=kdist.id,
                   sign_key=kdist.sign,
                   link_key=kdist.link)

    def to_c(self):
        kdist = driver.ble_gap_sec_kdist_t()
        kdist.enc = self.enc_key
        kdist.id = self.id_key
        kdist.sign = self.sign_key
        kdist.link = self.link_key
        return kdist

    def __repr__(self):
        return "%s(enc_key=%r, id_key=%r, sign_key=%r, link_key=%r)" % (self.__class__.__name__,
                                                                        self.enc_key, self.id_key, self.sign_key,
                                                                        self.link_key)


class BLEGapSecParams(object):
    def __init__(self, bond, mitm, le_sec_pairing, keypress_noti, io_caps, oob, min_key_size, max_key_size, kdist_own,
                 kdist_peer):
        self.bond = bond
        self.mitm = mitm
        self.le_sec_pairing = le_sec_pairing
        self.keypress_noti = keypress_noti
        self.io_caps = io_caps
        self.oob = oob
        self.min_key_size = min_key_size
        self.max_key_size = max_key_size
        self.kdist_own = kdist_own
        self.kdist_peer = kdist_peer

    @classmethod
    def from_c(cls, sec_params):
        return cls(bond=sec_params.bond,
                   mitm=sec_params.mitm,
                   le_sec_pairing=sec_params.lesc,
                   keypress_noti=sec_params.keypress,
                   io_caps=sec_params.io_caps,
                   oob=sec_params.oob,
                   min_key_size=sec_params.min_key_size,
                   max_key_size=sec_params.max_key_size,
                   kdist_own=BLEGapSecKeyDist.from_c(sec_params.kdist_own),
                   kdist_peer=BLEGapSecKeyDist.from_c(sec_params.kdist_peer))

    def to_c(self):
        sec_params = driver.ble_gap_sec_params_t()
        sec_params.bond = self.bond
        sec_params.mitm = self.mitm
        sec_params.lesc = self.le_sec_pairing
        sec_params.keypress = self.keypress_noti
        sec_params.io_caps = self.io_caps
        sec_params.oob = self.oob
        sec_params.min_key_size = self.min_key_size
        sec_params.max_key_size = self.max_key_size
        sec_params.kdist_own = self.kdist_own.to_c()
        sec_params.kdist_peer = self.kdist_peer.to_c()
        return sec_params

    def __repr__(self):
        return "%s(bond=%r, mitm=%r, le_sec_pairing=%r, keypress_noti=%r, io_caps=%r, oob=%r, min_key_size=%r, max_key_size=%r, kdist_own=%r, kdist_peer=%r)" % (
            self.__class__.__name__, self.bond, self.mitm, self.le_sec_pairing, self.keypress_noti, self.io_caps,
            self.oob, self.min_key_size, self.max_key_size, self.kdist_own, self.kdist_peer,)


class BLEGapSecKeyset(object):
    def __init__(self):
        self.sec_keyset = driver.ble_gap_sec_keyset_t()
        keys_own = driver.ble_gap_sec_keys_t()
        self.sec_keyset.keys_own = keys_own

        keys_peer = driver.ble_gap_sec_keys_t()
        keys_peer.p_enc_key = driver.ble_gap_enc_key_t()
        keys_peer.p_enc_key.enc_info = driver.ble_gap_enc_info_t()
        keys_peer.p_enc_key.master_id = driver.ble_gap_master_id_t()
        keys_peer.p_id_key = driver.ble_gap_id_key_t()
        keys_peer.p_id_key.id_info = driver.ble_gap_irk_t()
        keys_peer.p_id_key.id_addr_info = driver.ble_gap_addr_t()
        # keys_peer.p_sign_key            = driver.ble_gap_sign_info_t()
        # keys_peer.p_pk                  = driver.ble_gap_lesc_p256_pk_t()
        self.sec_keyset.keys_peer = keys_peer

    @classmethod
    def from_c(cls, sec_params):
        raise NotImplemented()

    def to_c(self):
        return self.sec_keyset


#################### Gatt ##################


class BLEGattWriteOperation(Enum):
    invalid = driver.BLE_GATT_OP_INVALID
    write_req = driver.BLE_GATT_OP_WRITE_REQ
    write_cmd = driver.BLE_GATT_OP_WRITE_CMD
    singed_write_cmd = driver.BLE_GATT_OP_SIGN_WRITE_CMD
    prepare_write_req = driver.BLE_GATT_OP_PREP_WRITE_REQ
    execute_write_req = driver.BLE_GATT_OP_EXEC_WRITE_REQ


class BLEGattHVXType(Enum):
    invalid = driver.BLE_GATT_HVX_INVALID
    notification = driver.BLE_GATT_HVX_NOTIFICATION
    indication = driver.BLE_GATT_HVX_INDICATION


class BLEGattStatusCode(Enum):
    success = driver.BLE_GATT_STATUS_SUCCESS
    unknown = driver.BLE_GATT_STATUS_UNKNOWN
    invalid = driver.BLE_GATT_STATUS_ATTERR_INVALID
    invalid_handle = driver.BLE_GATT_STATUS_ATTERR_INVALID_HANDLE
    read_not_permitted = driver.BLE_GATT_STATUS_ATTERR_READ_NOT_PERMITTED
    write_not_permitted = driver.BLE_GATT_STATUS_ATTERR_WRITE_NOT_PERMITTED
    invalid_pdu = driver.BLE_GATT_STATUS_ATTERR_INVALID_PDU
    insuf_authentication = driver.BLE_GATT_STATUS_ATTERR_INSUF_AUTHENTICATION
    request_not_supported = driver.BLE_GATT_STATUS_ATTERR_REQUEST_NOT_SUPPORTED
    invalid_offset = driver.BLE_GATT_STATUS_ATTERR_INVALID_OFFSET
    insuf_authorization = driver.BLE_GATT_STATUS_ATTERR_INSUF_AUTHORIZATION
    prepare_queue_full = driver.BLE_GATT_STATUS_ATTERR_PREPARE_QUEUE_FULL
    attribute_not_found = driver.BLE_GATT_STATUS_ATTERR_ATTRIBUTE_NOT_FOUND
    attribute_not_long = driver.BLE_GATT_STATUS_ATTERR_ATTRIBUTE_NOT_LONG
    insuf_enc_key_size = driver.BLE_GATT_STATUS_ATTERR_INSUF_ENC_KEY_SIZE
    invalid_att_val_length = driver.BLE_GATT_STATUS_ATTERR_INVALID_ATT_VAL_LENGTH
    unlikely_error = driver.BLE_GATT_STATUS_ATTERR_UNLIKELY_ERROR
    insuf_encryption = driver.BLE_GATT_STATUS_ATTERR_INSUF_ENCRYPTION
    unsupported_group_type = driver.BLE_GATT_STATUS_ATTERR_UNSUPPORTED_GROUP_TYPE
    insuf_resources = driver.BLE_GATT_STATUS_ATTERR_INSUF_RESOURCES
    rfu_range1_begin = driver.BLE_GATT_STATUS_ATTERR_RFU_RANGE1_BEGIN
    rfu_range1_end = driver.BLE_GATT_STATUS_ATTERR_RFU_RANGE1_END
    app_begin = driver.BLE_GATT_STATUS_ATTERR_APP_BEGIN
    app_end = driver.BLE_GATT_STATUS_ATTERR_APP_END
    rfu_range2_begin = driver.BLE_GATT_STATUS_ATTERR_RFU_RANGE2_BEGIN
    rfu_range2_end = driver.BLE_GATT_STATUS_ATTERR_RFU_RANGE2_END
    rfu_range3_begin = driver.BLE_GATT_STATUS_ATTERR_RFU_RANGE3_BEGIN
    rfu_range3_end = driver.BLE_GATT_STATUS_ATTERR_RFU_RANGE3_END
    cps_cccd_config_error = driver.BLE_GATT_STATUS_ATTERR_CPS_CCCD_CONFIG_ERROR
    cps_proc_alr_in_prog = driver.BLE_GATT_STATUS_ATTERR_CPS_PROC_ALR_IN_PROG
    cps_out_of_range = driver.BLE_GATT_STATUS_ATTERR_CPS_OUT_OF_RANGE


class BLEGattExecWriteFlag(Enum):
    prepared_cancel = driver.BLE_GATT_EXEC_WRITE_FLAG_PREPARED_CANCEL
    prepared_write = driver.BLE_GATT_EXEC_WRITE_FLAG_PREPARED_WRITE
    unused = 0x00


class BLEGattsCharHandles(object):
    def __init__(self, value_handle=0, user_desc_handle=0, cccd_handle=0, sccd_handle=0):
        self.value_handle = value_handle
        self.user_desc_handle = user_desc_handle
        self.cccd_handle = cccd_handle
        self.sccd_handle = sccd_handle

    def to_c(self):
        handle_params = driver.ble_gatts_char_handles_t()
        handle_params.value_handle = self.value_handle
        handle_params.user_desc_handle = self.user_desc_handle
        handle_params.cccd_handle = self.cccd_handle
        handle_params.sccd_handle = self.sccd_handle
        return handle_params

    @classmethod
    def from_c(cls, handle_params):
        return cls(handle_params.value_handle,
                   handle_params.user_desc_handle,
                   handle_params.cccd_handle,
                   handle_params.sccd_handle)


class BLEGattsAttribute(object):
    def __init__(self, uuid, attr_metadata, max_len, value=""):
        self.uuid = uuid
        self.attribute_metadata = attr_metadata
        self.max_len = max_len
        self.value = [1]

    def to_c(self):
        params = driver.ble_gatts_attr_t()
        params.p_uuid = self.uuid.to_c()
        params.p_attr_md = self.attribute_metadata.to_c()
        params.init_len = len(self.value)
        params.init_offs = 0
        params.max_len = self.max_len
        # TODO
        # if self.value:
        #     params.p_value = util.list_to_uint8_array(self.value)
        return params


class BLEGattsAttrMetadata(object):
    def __init__(self, read_permissions=BLEGapSecModeType.OPEN, write_permissions=BLEGapSecModeType.OPEN,
                 variable_length=False):
        self.read_perm = read_permissions
        self.write_perm = write_permissions
        self.vlen = variable_length

    def to_c(self):
        params = driver.ble_gatts_attr_md_t()
        params.read_perm = self.read_perm.to_c()
        params.write_perm = self.write_perm.to_c()
        params.vlen = self.vlen
        params.vloc = 1  # STACK
        params.rd_auth = 1
        params.wr_auth = 1
        return params

    @classmethod
    def from_c(cls, params):
        read_perm = BLEGapSecMode.from_c(params.read_perm)
        write_perm = BLEGapSecMode.from_c(params.write_perm)
        vlen = params.vlen
        return cls(read_perm, write_perm, vlen)


class BLEGattsCharMetadata(object):
    def __init__(self, char_props, user_description="", user_description_max_size=0,
                 user_desc_metadata=None, cccd_metadata=None, sccd_metadata=None):
        self.char_props = char_props
        self.user_description = user_description
        self.user_description_max_len = user_description_max_size
        self.user_desc_metadata = user_desc_metadata
        self.cccd_metadata = cccd_metadata
        self.sccd_metadata = sccd_metadata

    def to_c(self):
        params = driver.ble_gatts_char_md_t()
        params.char_props = self.char_props.to_c()
        # if self.user_description:
        #     params.p_char_user_desc = util.list_to_char_array(self.user_description)
        #     params.char_user_desc_size = len(self.user_description)
        # else:
        #     params.char_user_desc_size = 0
        # params.char_user_desc_max_size = self.user_description_max_len
        # if self.user_desc_metadata:
        #     params.p_user_desc_md = self.user_desc_metadata.to_c()
        # if self.cccd_metadata:
        #     params.p_cccd_md = self.cccd_metadata.to_c()
        # if self.sccd_metadata:
        #     params.p_sccd_md = self.sccd_metadata.to_c()
        return params

    @classmethod
    def from_c(cls, params):
        pass


class BLEGattcWriteParams(object):
    def __init__(self, write_op, flags, handle, data, offset):
        assert isinstance(write_op, BLEGattWriteOperation), 'Invalid argument type'
        assert isinstance(flags, BLEGattExecWriteFlag), 'Invalid argument type'
        self.write_op = write_op
        self.flags = flags
        self.handle = handle
        self.data = data
        self.offset = offset

    @classmethod
    def from_c(cls, gattc_write_params):
        return cls(write_op=BLEGattWriteOperation(gattc_write_params.write_op),
                   flags=gattc_write_params.flags,
                   handle=gattc_write_params.handle,
                   data=util.uint8_array_to_list(gattc_write_params.p_value,
                                                 gattc_write_params.len))

    def to_c(self):
        self.__data_array = util.list_to_uint8_array(self.data)
        write_params = driver.ble_gattc_write_params_t()
        write_params.p_value = self.__data_array.cast()
        write_params.flags = self.flags.value
        write_params.handle = self.handle
        write_params.offset = self.offset
        write_params.len = len(self.data)
        write_params.write_op = self.write_op.value

        return write_params


class BLEDescriptor(object):
    def __init__(self, uuid, handle, data=None):
        self.handle = handle
        self.uuid = uuid
        self.data = data

    @classmethod
    def from_c(cls, gattc_desc):
        return cls(uuid=BLEUUID.from_c(gattc_desc.uuid),
                   handle=gattc_desc.handle)


class BLECharacteristicProperties(object):
    def __init__(self, broadcast=False, read=False, write_wo_resp=False,
                 write=False, notify=False, indicate=False, auth_signed_wr=False):
        self.broadcast = broadcast
        self.read = read
        self.write_wo_resp = write_wo_resp
        self.write = write
        self.notify = notify
        self.indicate = indicate
        self.auth_signed_wr = auth_signed_wr

    @classmethod
    def from_c(cls, gattc_char_props):
        return cls(gattc_char_props.broadcast == 1,
                   gattc_char_props.read == 1,
                   gattc_char_props.write_wo_resp == 1,
                   gattc_char_props.write == 1,
                   gattc_char_props.notify == 1,
                   gattc_char_props.indicate == 1,
                   gattc_char_props.auth_signed_wr == 1)

    def to_c(self):
        params = driver.ble_gatt_char_props_t()
        params.broadcast = int(self.broadcast)
        params.read = int(self.read)
        params.write_wo_resp = int(self.write_wo_resp)
        params.write = int(self.write)
        params.notify = int(self.notify)
        params.indicate = int(self.indicate)
        params.auth_signed_wr = int(self.auth_signed_wr)
        return params


class BLECharacteristic(object):
    char_uuid = BLEUUID(BLEUUID.Standard.characteristic)

    def __init__(self, uuid, handle_decl, handle_value, data_decl=None, data_value=None, char_props=None):
        self.uuid = uuid
        self.handle_decl = handle_decl
        self.handle_value = handle_value
        self.data_decl = data_decl
        self.data_value = data_value
        self.char_props = char_props  # TODO: if None, parse first byte of data_decl?
        self.end_handle = None
        self.descs = list()

    @classmethod
    def from_c(cls, gattc_char):
        return cls(uuid=BLEUUID.from_c(gattc_char.uuid),
                   handle_decl=gattc_char.handle_decl,
                   handle_value=gattc_char.handle_value,
                   char_props=BLECharacteristicProperties.from_c(gattc_char.char_props))


class BLEService(object):
    srvc_uuid = BLEUUID(BLEUUID.Standard.service_primary)

    def __init__(self, uuid, start_handle, end_handle):
        self.uuid = uuid
        self.start_handle = start_handle
        self.end_handle = end_handle
        self.chars = list()

    @classmethod
    def from_c(cls, gattc_service):
        return cls(uuid=BLEUUID.from_c(gattc_service.uuid),
                   start_handle=gattc_service.handle_range.start_handle,
                   end_handle=gattc_service.handle_range.end_handle)

    def char_add(self, char):
        char.end_handle = self.end_handle
        self.chars.append(char)
        if len(self.chars) > 1:
            self.chars[-2].end_handle = char.handle_decl - 1


class BleGattHandle(object):
    def __init__(self, handle=-1):
        self.handle = handle
