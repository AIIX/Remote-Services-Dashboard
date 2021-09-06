"""
Copyright 2020 Aditya Mehra (aix.m@outlook.com).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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
