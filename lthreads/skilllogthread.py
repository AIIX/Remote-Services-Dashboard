"""
Copyright 2020 Aditya Mehra (aix.m@outlook.com).

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

import threading
import tailhead
import time
from flask_socketio import SocketIO, emit


class SkillLogThread(threading.Thread):
    def __init__(self, sleep_interval=1):
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self._should_kill = False

    def run(self):
        while True:
            line1 = tailhead.tail(open('/var/log/mycroft/skills.log', "rb"), 3)
            line1sant = str(line1[0].decode("utf-8"))
            emit('my_response', {'data': line1sant})
            for line2 in tailhead.follow_path('/var/log/mycroft/skills.log'):
                if line2 is not None:
                    emit('my_response', {'data': line2})
                else:
                    if self._should_kill:
                        break
                    time.sleep(1)

            if self._should_kill:
                break
        
        self.reset_kill()

    def kill(self):
        self._should_kill = True
        self._kill.set() 

    def reset_kill(self):
        self._should_kill = False
