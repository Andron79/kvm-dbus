import asyncio
import os
import sys

import gmos_logging
from gmbox_kvm_dbus.kvm_dbus import (
    KvmDBusInterface,
    KvmDBusClient
)

kvm_interface = None


async def _main():
    kvm_client = await KvmDBusClient.create_and_run()
    global kvm_interface
    kvm_interface = await KvmDBusInterface.create_and_run(kvm_client)


def main():
    gmos_logging.log.init_logging(
        process_name="gmbox-kvm-dbus"
    )
    gmos_logging.exceptions.setup_exception_hook()
    loop = asyncio.get_event_loop()
    loop.create_task(_main())
    try:
        loop.run_forever()
    finally:
        loop.close()
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
