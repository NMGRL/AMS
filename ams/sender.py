# ===============================================================================
# Copyright 2020 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import time

from serial import Serial, SerialException

from ams.loggable import Loggable


class Sender(Loggable):
    name = 'sender'

    _dev = None

    def open(self, address):
        try:
            self._dev = Serial(address, baudrate=115200)
            return True
        except SerialException as e:
            self.warning(e)

    def wakeup(self):
        self._write(bytes('\r\n\r\n', 'utf8'))  
        time.sleep(2) 
        self._dev.flushInput()  # Flush startup text in serial input
       
    def send(self, msg):
        if self._validate(msg):
            msg = f'{msg}\n'
            self._write(bytes(msg, 'utf8'))
            resp = self._read()
            self._log_response(msg, resp)
            return resp

    def _validate(self, msg):
        return True

    def _write(self, msg):
        if self._dev:
            self._dev.write(msg)

    def _read(self):
        if self._dev:
            resp = self._dev.readline()
            return resp

    def _log_response(self, msg, resp):
        self.debug(f'{msg}>>{resp}')

# ============= EOF =============================================
