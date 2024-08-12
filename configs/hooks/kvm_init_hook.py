#! /usr/bin/python3
import json
import logging
from dataclasses import dataclass

import gmos_logging

from gmbox_kvm_dbus.settings import KvmState

logger = logging.getLogger(__name__)

gmos_logging.log.init_logging(
    process_name="update-hook"
)
gmos_logging.exceptions.setup_exception_hook()


@dataclass
class Icon:
    SWITCH_1_TO_2: str = '/opt/getmobit/share/icons/kvm/switch1to2.svg'
    SWITCH_2_TO_1: str = '/opt/getmobit/share/icons/kvm/switch2to1.svg'
    FIRST_MOTHERBOARD: str = '/opt/getmobit/share/icons/kvm/circuit_1.svg'
    SECOND_MOTHERBOARD: str = '/opt/getmobit/share/icons/kvm/circuit_2.svg'


@dataclass
class SwitchIcon1to2:
    ERROR: str = '/opt/getmobit/share/icons/kvm/switch1to2_error.svg'
    WARNING: str = '/opt/getmobit/share/icons/kvm/switch1to2_warning.svg'


@dataclass
class SwitchIcon2to1:
    ERROR: str = '/opt/getmobit/share/icons/kvm/switch2to1_error.svg'
    WARNING: str = '/opt/getmobit/share/icons/kvm/switch2to1_warning.svg'


# switch kvm command
@dataclass
class Command:
    NONE: str = ""
    SWITCH: str = ("dbus-send --system --print-reply=literal --dest=org.getmobit.kvm "
                   "/ org.getmobit.kvm.switchMotherboard")


kvm = KvmState()
icon = ""
command = ""
status_icon = ""

logger.debug(f'Value of is_first_motherboard: {kvm.is_first_motherboard()}')
logger.debug(f'Value of is_locked: {kvm.is_locked()}')
logger.debug(f'Value of is_integrity_check_in_progress: {kvm.is_integrity_check_in_progress()}')

if kvm.is_first_motherboard():
    status_icon = Icon.FIRST_MOTHERBOARD
    if kvm.is_locked() and kvm.is_integrity_check_in_progress():
        icon = SwitchIcon1to2.WARNING
        command = Command.NONE
    elif kvm.is_locked() and not kvm.is_integrity_check_in_progress():
        icon = SwitchIcon1to2.ERROR
        command = Command.NONE
    elif not kvm.is_locked() and not kvm.is_integrity_check_in_progress():
        icon = Icon.SWITCH_1_TO_2
        command = Command.SWITCH
else:
    status_icon = Icon.SECOND_MOTHERBOARD
    if kvm.is_locked() and kvm.is_integrity_check_in_progress():
        icon = SwitchIcon2to1.WARNING
        command = Command.NONE
    elif kvm.is_locked() and not kvm.is_integrity_check_in_progress():
        icon = SwitchIcon2to1.ERROR
        command = Command.NONE
    elif not kvm.is_locked() and not kvm.is_integrity_check_in_progress():
        icon = Icon.SWITCH_2_TO_1
        command = Command.SWITCH

state = {
    "icon": icon,
    "command": command,
    "visible": kvm.is_duo(),
    "enable": kvm.is_locked(),
    "status_icon": status_icon
}

print(json.dumps(state, indent=4))
