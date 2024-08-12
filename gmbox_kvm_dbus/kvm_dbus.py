import asyncio
import logging

from dbus_next import BusType
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, signal

from gmbox_kvm_dbus.settings import (
    KVM_DBUS_NAME,
    KVM_PATH,
    KVM_INTERFACE_NAME,
    GMBOX_KVM_DBUS_NAME,
    GMBOX_KVM_INTERFACE_NAME,
    GMBOX_KVM_PATH,
    INTEGRITY_CHECK_TIMEOUT
)

logger = logging.getLogger(__name__)

events = None


class KvmDBusInterface(ServiceInterface):
    def __init__(self, kvm_client=None) -> None:
        super().__init__(name=GMBOX_KVM_INTERFACE_NAME)
        self.kvm = kvm_client
        self.locked_changed = asyncio.Event()
        self.kvm.set_locked_changed_callback(self.on_locked_changed)
        self.integrity_check_in_progress = False

    @signal(name='lockedChanged')
    def emit_locked_changed(self):
        """Send message of isLocked property update"""

    @method(name='isIntegrityCheckInProgress')
    def is_integrity_check(self) -> 'b':  # noqa: F821
        return self.integrity_check_in_progress

    async def run_integrity_check(self):
        logger.info('Integrity check has been run')
        self.integrity_check_in_progress = True
        self.emit_locked_changed()
        await asyncio.sleep(INTEGRITY_CHECK_TIMEOUT)
        self.integrity_check_in_progress = False
        self.emit_locked_changed()
        logger.info('Integrity check failed')

    async def poll_events(self):
        task = None
        while True:
            await self.locked_changed.wait()
            self.locked_changed.clear()
            logger.info(f'State changed, new state: {await self.kvm.is_locked}')
            if await self.kvm.is_locked:
                if not task or task.done():
                    task = asyncio.create_task(self.run_integrity_check())
                continue
            if task and not task.done():
                task.cancel()
            if self.integrity_check_in_progress:
                self.integrity_check_in_progress = False
                logger.info('Integrity check done')
            self.emit_locked_changed()

    def on_locked_changed(self):
        logger.info('Signal lockedChanged caught')
        self.locked_changed.set()

    @staticmethod
    async def create_and_run(kvm_client):
        logger.info('Running GM-Box D-Bus interface daemon...')
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        interface = KvmDBusInterface(kvm_client)
        bus.export(GMBOX_KVM_PATH, interface)
        await bus.request_name(GMBOX_KVM_DBUS_NAME)
        global events
        events = asyncio.create_task(interface.poll_events())
        return interface

    @method(name='isLocked')
    async def is_locked(self) -> 'b':  # noqa: F821
        return await self.kvm.is_locked

    @method(name='isDuo')
    async def is_duo(self) -> 'b':  # noqa: F821
        return await self.kvm.is_duo

    @method(name='isOnFirstMotherboard')
    async def is_first_motherboard(self) -> 'b':  # noqa: F821
        return await self.kvm.is_first_motherboard

    @method(name='switchMotherboard')
    async def toggle(self):
        return await self.kvm.toggle


class KvmDBusClient:
    def __init__(self, interface):
        self.interface = interface

    @staticmethod
    async def create_and_run():
        logger.info('Running D-Bus client...')
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        introspection = await bus.introspect(KVM_DBUS_NAME, KVM_PATH)
        proxy_object = bus.get_proxy_object(KVM_DBUS_NAME, KVM_PATH, introspection)
        interface = proxy_object.get_interface(KVM_INTERFACE_NAME)
        return KvmDBusClient(interface=interface)

    @property
    async def is_locked(self) -> 'b':  # noqa: F821
        return await self.interface.call_is_locked()

    @property
    async def is_first_motherboard(self) -> 'b':  # noqa: F821
        return await self.interface.call_is_on_first_motherboard()

    @property
    async def is_duo(self) -> 'b':  # noqa: F821
        return await self.interface.call_is_duo()

    @property
    async def toggle(self) -> None:  # noqa: F821
        return await self.interface.call_switch_motherboard()

    def set_locked_changed_callback(self, foo):
        self.interface.on_locked_changed(foo)
