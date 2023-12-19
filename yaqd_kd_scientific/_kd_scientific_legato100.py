__all__ = ["KdScientificLegato100"]

import asyncio
import serial  # type: ignore
from typing import Dict, Any, List

from yaqd_core import IsDaemon, HasPosition, UsesSerial, IsDiscrete, UsesUart, aserial


class KdScientificLegato100(IsDiscrete, HasPosition, UsesUart, UsesSerial, IsDaemon):
    _kind = "kd-scientific-legato100"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._ser = aserial.ASerial(self._config["serial_port"])
        self._ser.baudrate = self._config["baud_rate"]
        self._ser.write("echo off\r\n".encode())
        self._loop.create_task(self.poll_status())

    def direct_serial_write(self, bytes) -> None:
        self._ser.write(bytes)

    async def poll_status(self):
        while True:
            self._ser.write("status\r\n".encode())
            await asyncio.sleep(1)

    def _set_position(self, position) -> None:
        if position >= 0.5:
            # send serial command to START
            self._state["position"] = 1.0
            self._state["position_identifier"] = "infusing"
            self._ser.write("run\r\n".encode())
        else:
            self._state["position"] = 0.0
            self._state["position_identifier"] = "paused"
            self._ser.write("stop\r\n".encode())
            # send serial command to STOP

    async def update_state(self):
        while True:
            line = (await self._ser.areadline()).decode().strip()
            if len(line) == 35:
                motor_direction = line[29]
                if motor_direction == "I":
                    self._state["position"] = 1.0
                    self._state["position_identifier"] = "infusing"
                else:
                    self._state["position"] = 0.0
                    self._state["position_identifier"] = "paused"
            await asyncio.sleep(0.1)
