# dbus settings
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union, Tuple

# dbus interface gmbox-kvm-switcher-daemon
KVM_DBUS_NAME = 'org.getmobit.gmboxKvm'
KVM_INTERFACE_NAME = 'org.getmobit.gmboxKvm'
KVM_PATH = '/'

# dbus interface gmbox-kvm-dbus
GMBOX_KVM_DBUS_NAME = 'org.getmobit.kvm'
GMBOX_KVM_INTERFACE_NAME = 'org.getmobit.kvm'
GMBOX_KVM_PATH = '/'

# KVM side-link confIg
SIDE_LINKS_CONFIGS_FOLDER = Path('/opt/getmobit/gm-sidebar/side-link/kvm')
PERSISTENT_SIDE_LINKS_CONFIGS_FOLDER = Path('/persistent/configs/gm-sidebar/side-link/kvm')
SIDE_LINK_CONFIG_FILE = 'config.json'


@dataclass
class KvmSidelink:
    name: str
    update_notify: str
    update_hook: str
    init_hook: str


@dataclass
class BooleanValues:
    TRUE: Tuple[str, ...] = ('true', 'yes')
    FALSE: Tuple[str, ...] = ('false', 'no')


def to_bool(value: Optional[Union[str, int, float]]) -> bool:
    """Parses string to boolean"""
    if value:
        if isinstance(value, int):
            return bool(value)
        if value.lower() in BooleanValues.TRUE:
            return True
        if value.lower() in BooleanValues.FALSE:
            return False
    return False


INTEGRITY_CHECK_TIMEOUT = 60


class KvmState:
    @staticmethod
    def is_duo() -> bool:
        _is_duo = subprocess.check_output(
            'dbus-send --system --print-reply=literal --dest=org.getmobit.kvm / org.getmobit.kvm.isDuo',
            shell=True
        )
        return to_bool(_is_duo.decode("utf-8").split()[1])

    @staticmethod
    def is_locked() -> bool:
        _is_locked = subprocess.check_output(
            'dbus-send --system --print-reply=literal --dest=org.getmobit.kvm / org.getmobit.kvm.isLocked',
            shell=True
        )
        return to_bool(_is_locked.decode("utf-8").split()[1])

    @staticmethod
    def is_first_motherboard() -> bool:
        _is_first_motherboard = subprocess.check_output(
            'dbus-send --system --print-reply=literal --dest=org.getmobit.kvm / org.getmobit.kvm.isOnFirstMotherboard',
            shell=True
        )
        return to_bool(_is_first_motherboard.decode("utf-8").split()[1])

    @staticmethod
    def is_integrity_check_in_progress() -> bool:
        _is_integrity_check_in_progress = subprocess.check_output(
            'dbus-send --system --print-reply=literal --dest=org.getmobit.kvm / '
            'org.getmobit.kvm.isIntegrityCheckInProgress',
            shell=True
        )
        return to_bool(_is_integrity_check_in_progress.decode("utf-8").split()[1])
