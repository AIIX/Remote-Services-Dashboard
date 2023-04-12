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
import sys
import threading
import json
from flask_socketio import emit
from os import path, scandir, environ
from os.path import join, isdir

class SkillModelBuilderThread(threading.Thread):
    def __init__(self, sleep_interval=1):
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self._should_kill = False
        self.skills_model = list()
        self.skill_settings_model = dict()
        
    def get_xdg_data_dirs(self):
        user_data_dir = environ.get("XDG_DATA_HOME", join(environ["HOME"], ".local", "share"))
        xdg_data_dirs = ["/usr/share", "/usr/local/share"]
        if "XDG_DATA_DIRS" in environ:
            xdg_data_dirs = environ["XDG_DATA_DIRS"].split(":")
        xdg_data_dirs.append(user_data_dir)
        return xdg_data_dirs

    def get_skill_folders(self):
        skill_folders = list()
        xdg_skill_dirs = self.get_xdg_data_dirs()
        for p in xdg_skill_dirs:
            if isdir(join(p, "mycroft", "skills")):
                for subfolder in scandir(join(p, "mycroft", "skills")):
                    if subfolder.is_dir():
                        skill_folders.append(subfolder.path)

        python_version = ".".join(str(x) for x in sys.version_info[:2])
        python_sys_site_packages = environ.get("PYTHON_SYS_SITE_PACKAGES")
        if python_sys_site_packages is None:
            python_sys_site_packages = join("/usr", "lib", "python" + python_version, "site-packages")
        python_user_site_packages = environ.get("PYTHON_USER_SITE_PACKAGES")
        if python_user_site_packages is None:
            python_user_site_packages = join(environ["HOME"], ".local", "lib", "python" + python_version,
                                             "site-packages")
            
        for p in [python_sys_site_packages, python_user_site_packages]:
            for subfolder in scandir(p):
                print(subfolder.path)
                if subfolder.is_dir():
                    if path.exists(join(subfolder.path, "__init__.py")) and path.exists(join(subfolder.path, "settingsmeta.json")):
                        print("Found skill: " + subfolder.path)
                        skill_folders.append(subfolder.path)

        return skill_folders

    def run(self):
        self.skills_model.clear()
        skills_folders = self.get_skill_folders()
        skill_settings_file = "settingsmeta.json"
        for folder in skills_folders:
            if path.exists(join(folder, skill_settings_file)) \
                    and path.isfile(join(folder, skill_settings_file)):
                self.skill_settings_model = dict(skill_name=folder.rsplit('/', 1)[-1], skill_path=folder,
                                                 settings_meta=self.build_skill_settings_model(
                                                     join(folder, skill_settings_file)))
                self.skills_model.append(self.skill_settings_model)

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
