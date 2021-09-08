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
import json
from flask_socketio import SocketIO, emit
from os import path, environ, scandir
from os.path import join


class SkillModelBuilderThread(threading.Thread):
    def __init__(self, sleep_interval=1):
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self._should_kill = False
        self.skills_model = list()
        self.skill_settings_model = dict()

    def run(self):
        self.skills_model.clear()
        skills_folder_path = "/opt/mycroft/skills/"  # environ['MYCROFT_SKILLS_LOCATION']
        subfolders = [f.path for f in scandir(skills_folder_path) if f.is_dir()]
        skill_settings_file = "settingsmeta.json"
        for folder in subfolders:
            print(folder)
            if path.exists(join(folder, skill_settings_file)) \
                    and path.isfile(join(folder, skill_settings_file)):
                self.skill_settings_model = dict(skill_name=folder.rsplit('/', 1)[-1], skill_path=folder,
                                                 settings_meta=self.build_skill_settings_model(
                                                     join(folder, skill_settings_file)))
                self.skills_model.append(self.skill_settings_model)

        print(self.skills_model)
        emit("skills_model_changed", {"data": self.skills_model})

        self.kill()

    def build_skill_settings_model(self, settings_meta_path):
        with open(settings_meta_path, "r") as f:
            parsed_json = json.load(f)
        return parsed_json

    def kill(self):
        self._should_kill = True
        self._kill.set()

    def reset_kill(self):
        self._should_kill = False
