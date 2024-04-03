from enum import Enum


class EventChannels(str, Enum):
    read_service = 'read_service'
    data_changed = 'data_changed'
    snapshot_in = 'snapshot_in'
    snapshot_out = 'snapshot_out'
    smcp_in = 'smcp_in'
