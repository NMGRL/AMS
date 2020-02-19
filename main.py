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

import logging
from ams.sender import Sender
import curses


def setup_logging():
    logger = logging.getLogger('ams')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('ams.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


def terminal(s):
    while 1:
        cmd = input('>>')
        cmd = f'G0 X{cmd}'
        s.send(cmd)


def joystick(sender):

    sender.send('G91')

    def key_up():
        return 'G0 Y10'

    def key_down():
        return 'G0 Y-10'

    def key_left():
        return 'G0 X-10'

    def key_right():
        return 'G0 X10'

    def closure(std):
        std.clear()
        std.keypad(True)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        funcs = {curses.KEY_UP: key_up,
                 curses.KEY_DOWN: key_down,
                 curses.KEY_LEFT: key_left,
                 curses.KEY_RIGHT: key_right
                 }

        while 1:
            ch = std.getch()
            func = funcs.get(ch)
            if func:
                cmd = func()
                std.clear()
                std.addstr(cmd, curses.color_pair(1))
                std.refresh()
                if sender:
                    sender.send(cmd)

    return closure


def main():
    setup_logging()

    s = Sender()

    if s.open('/dev/tty.usbmodem1451101'):
        s.wakeup()
        curses.wrapper(joystick(s))
    #    terminal(s)


if __name__ == '__main__':
    main()

# ============= EOF =============================================
