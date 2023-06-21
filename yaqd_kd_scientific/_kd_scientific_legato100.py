__all__ = ["KdScientificLegato100"]

import asyncio
import serial  # type: ignore
from typing import Dict, Any, List

from yaqd_core import IsDaemon, HasPosition, UsesSerial, IsDiscrete, UsesUart


class KdScientificLegato100(IsDiscrete, HasPosition, UsesUart, UsesSerial, IsDaemon):
    _kind = "kd-scientific-legato100"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Perform any unique initialization
        self._ser = serial.Serial("/dev/cu.usbmodem11075471")
        # self._ser.baudrate = self._config["baud_rate"]

    def _set_position(self, position) -> None:
        if position >= 0.5:
            # send serial command to START
            self._state["position"] = self._state["destination"]
            self._state["position_identifier"] = "run"
            self._ser.write("run\r\n".encode())
        else:
            self._state["position"] = self._state["destination"]
            self._state["position_identifier"] = "stop"
            self._ser.write("stop\r\n".encode())
            # send serial command to STOP

    def direct_serial_write(self, bytes) -> None:
        self._ser.write(bytes)
