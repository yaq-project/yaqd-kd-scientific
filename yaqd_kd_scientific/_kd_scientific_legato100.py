__all__ = ["KdScientificLegato100"]

import asyncio
import serial
from typing import Dict, Any, List

from yaqd_core import IsDaemon, HasPosition, UsesSerial


class KdScientificLegato100(HasPosition, UsesSerial, IsDaemon):
    _kind = "kd-scientific-legato100"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Perform any unique initialization
        self._ser = serial.Serial("/dev/cu.usbmodem11075471")
        self._ser.baudrate = 115200


    def _set_position(self, position) -> None:

        if position >= 0.5:
            # send serial command to START
            self._ser.write("run\r\n".encode())
        else:
            self._ser.write("stop\r\n".encode())
            # send serial command to STOP

    def direct_serial_write(self, bytes) -> None:
        pass

    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        # If there is no state to monitor continuously, delete this function
        while True:
            # Perform any updates to internal state
            self._busy = False
            # There must be at least one `await` in this loop
            # This one waits for something to trigger the "busy" state
            # (Setting `self._busy = True)
            # Otherwise, you can simply `await asyncio.sleep(0.01)`
            await self._busy_sig.wait()
