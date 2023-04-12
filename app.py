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

import json
import platform
import socket
import subprocess

import cpuinfo
import psutil
from flask import Flask, jsonify, render_template, request
from flask_fontawesome import FontAwesome
from flask_simplelogin import SimpleLogin, login_required
from flask_socketio import SocketIO, emit

from lthreads.skillmodelbuilderthread import SkillModelBuilderThread

app = Flask(__name__)
fa = FontAwesome(app)
socketio = SocketIO(app)

sm_thread = SkillModelBuilderThread()
app.config['SECRET_KEY'] = '0V0$D@$HB0RD'


def get_messagebus_services():
    messagebus_proc_list = ["mycroft-systemd_messagebus", "ovos-systemd_messagebus", "ovos-bus-server", "mycroft-messagebus", "ovos-messagebus", "neon-messagebus",
                            "mycroft-systemd-messagebus", "ovos-systemd-messagebus", "neon-systemd-messagebus", "mycroft-systemd-bus", "ovos-systemd-bus", "neon-systemd-bus"]
    messagebus_service_list = ["mycroft-messagebus.service", "ovos-messagebus.service",
                               "neon-messagebus.service", "mycroft-bus.service", "ovos-bus.service", "neon-bus.service"]
    return [messagebus_proc_list, messagebus_service_list]


def get_skills_services():
    skills_proc_list = ["mycroft-systemd_skills", "ovos-systemd_skills", "neon-systemd_skills", "mycroft-skills",
                        "ovos-skills", "neon-skills", "mycroft-systemd-skills", "ovos-systemd-skills", "neon-systemd-skills"]
    skills_service_list = ["mycroft-skills.service",
                           "ovos-skills.service", "neon-skills.service"]
    return [skills_proc_list, skills_service_list]


def get_gui_services():
    gui_proc_list = ["mycroft-systemd_gui", "ovos-systemd_gui", "neon-systemd_gui",
                     "mycroft-systemd-gui", "ovos-systemd-gui", "neon-systemd-gui"]
    gui_service_list = ["mycroft-enclosure-gui.service",
                        "ovos-enclosure-gui.service", "neon-gui.service"]
    return [gui_proc_list, gui_service_list]


def get_audio_services():
    audio_proc_list = ["mycroft-systemd_audio", "ovos-systemd_audio", "neon-systemd_audio",
                       "mycroft-systemd-audio", "ovos-systemd-audio", "neon-systemd-audio"]
    audio_service_list = ["mycroft-audio.service",
                          "ovos-audio.service", "neon-audio.service"]
    return [audio_proc_list, audio_service_list]


def get_voice_services():
    voice_proc_list = ["mycroft-systemd_voice", "ovos-systemd_voice", "neon-systemd_voice",
                       "mycroft-systemd-voice", "ovos-systemd-voice", "neon-systemd-voice"]
    voice_service_list = ["mycroft-voice.service",
                          "ovos-voice.service", "neon-voice.service"]
    return [voice_proc_list, voice_service_list]


def get_phal_services():
    phal_proc_list = ["mycroft-systemd_phal", "ovos-systemd_phal", "neon-systemd_phal",
                      "mycroft-systemd-phal", "ovos-systemd-phal", "neon-systemd-phal"]
    phal_service_list = ["mycroft-phal.service",
                         "ovos-phal.service", "neon-phal.service"]
    return [phal_proc_list, phal_service_list]


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})


@app.route("/skills-settings")
@login_required()
def dashskilllocalsettings():
    return render_template("skills-settings.html")


@app.route("/docs/rs/introduction")
@login_required
def dashdocintro():
    return render_template("rs-intro.html")


@app.route("/docs/rs/connection-guide")
@login_required
def dashdocconnect():
    return render_template("rs-connection.html")


@app.route("/docs/rs/dashboard-guide")
@login_required
def dashdocdash():
    return render_template("rs-dashboard.html")


@app.route("/update/_sys_info", methods=['GET'])
def update_sys_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent
    return jsonify(cpu=cpu_usage, ram=ram_usage, disk=disk_usage)


@app.context_processor
def get_current_mem_usage():
    usage = psutil.virtual_memory().percent
    return dict(get_current_mem_usage=usage)


@app.context_processor
def get_current_cpu_usage():
    usage = psutil.cpu_percent(interval=1)
    return dict(get_current_mem_usage=usage)


@app.context_processor
def get_current_storage_usage():
    usage = psutil.disk_usage("/").percent
    return dict(get_current_mem_usage=usage)


@app.route("/update/_platform_info", methods=['GET'])
def get_platform_information():
    p_type = platform.system()
    p_info = cpuinfo.get_cpu_info()['brand_raw']
    ip_info = get_ip_address()
    return jsonify(plaform_type=p_type, platform_info=p_info, platform_ip=ip_info)


def check_if_service_is_running(service_name):
    """
    Check if the given service is running.
    """
    cmd = ['systemctl', '--user', 'is-active', service_name]
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        pass

    cmd = ['systemctl', 'is-active', service_name]
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        pass

    return False


def check_process_is_running(process_name):
    """
    Check if there is any running process that contains the given name processName.
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == "python3":
                proc_cmd = proc.cmdline()
                process_n = process_name.lower() + ".py"
                if process_n in proc_cmd:
                    return [True, proc.pid]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, IndexError):
            pass

    return [False, str("NA")]


@app.route("/update/_check_process_status", methods=['POST'])
def check_service():
    """
    Check if there is any running process or service.
    """
    service_request = request.form.to_dict()
    service_name = service_request["service"]

    if service_name == "messagebus":
        bus_running = False
        bus_pid = str("NA")
        bus_service_type = str("NA")
        bus_service_name = str("NA")
        bus_list = get_messagebus_services()
        bus_services_list = bus_list[1]
        bus_process_list = bus_list[0]
        for bus_service in bus_services_list:
            if check_if_service_is_running(bus_service):
                bus_running = True
                bus_service_type = "systemd"
                bus_service_name = bus_service
                bus_pid = str("SYS-D")
                break

        for bus_process in bus_process_list:
            proc_running = check_process_is_running(bus_process)
            if proc_running[0]:
                bus_running = True
                bus_pid = proc_running[1]
                bus_service_type = "process"
                bus_service_name = bus_process + ".py"
                break

        return jsonify(process_running=bus_running,
                       process_pid=bus_pid, process_type=bus_service_type,
                       process_name=bus_service_name)

    if service_name == "skills":
        skills_running = False
        skills_pid = str("NA")
        skills_service_type = str("NA")
        skills_service_name = str("NA")
        skills_list = get_skills_services()
        skills_services_list = skills_list[1]
        skills_process_list = skills_list[0]
        for skills_service in skills_services_list:
            if check_if_service_is_running(skills_service):
                skills_running = True
                skills_service_type = "systemd"
                skills_service_name = skills_service
                skills_pid = str("SYS-D")
                break

        for skills_process in skills_process_list:
            proc_running = check_process_is_running(skills_process)
            if proc_running[0]:
                skills_running = True
                skills_pid = proc_running[1]
                skills_service_type = "process"
                skills_service_name = skills_process + ".py"
                break

        return jsonify(process_running=skills_running,
                       process_pid=skills_pid, process_type=skills_service_type,
                       process_name=skills_service_name)

    if service_name == "gui":
        gui_running = False
        gui_pid = str("NA")
        gui_service_type = str("NA")
        gui_service_name = str("NA")
        gui_list = get_gui_services()
        gui_services_list = gui_list[1]
        gui_process_list = gui_list[0]
        for gui_service in gui_services_list:
            if check_if_service_is_running(gui_service):
                gui_running = True
                gui_service_type = "systemd"
                gui_service_name = gui_service
                gui_pid = str("SYS-D")
                break

        for gui_process in gui_process_list:
            proc_running = check_process_is_running(gui_process)
            if proc_running[0]:
                gui_running = True
                gui_pid = proc_running[1]
                gui_service_type = "process"
                gui_service_name = gui_process + ".py"
                break

        return jsonify(process_running=gui_running,
                       process_pid=gui_pid, process_type=gui_service_type,
                       process_name=gui_service_name)

    if service_name == "voice":
        voice_running = False
        voice_pid = str("NA")
        voice_service_type = str("NA")
        voice_service_name = str("NA")
        voice_list = get_voice_services()
        voice_services_list = voice_list[1]
        voice_process_list = voice_list[0]
        for voice_service in voice_services_list:
            if check_if_service_is_running(voice_service):
                voice_running = True
                voice_service_type = "systemd"
                voice_service_name = voice_service
                voice_pid = str("SYS-D")
                break

        for voice_process in voice_process_list:
            proc_running = check_process_is_running(voice_process)
            if proc_running[0]:
                voice_running = True
                voice_pid = proc_running[1]
                voice_service_type = "process"
                voice_service_name = voice_process + ".py"
                break

        return jsonify(process_running=voice_running,
                       process_pid=voice_pid, process_type=voice_service_type,
                       process_name=voice_service_name)

    if service_name == "audio":
        audio_running = False
        audio_pid = str("NA")
        audio_service_type = str("NA")
        audio_service_name = str("NA")
        audio_list = get_audio_services()
        audio_services_list = audio_list[1]
        audio_process_list = audio_list[0]
        for audio_service in audio_services_list:
            if check_if_service_is_running(audio_service):
                audio_running = True
                audio_service_type = "systemd"
                audio_service_name = audio_service
                audio_pid = str("SYS-D")
                break

        for audio_process in audio_process_list:
            proc_running = check_process_is_running(audio_process)
            if proc_running[0]:
                audio_running = True
                audio_pid = proc_running[1]
                audio_service_type = "process"
                audio_service_name = audio_process + ".py"
                break

        return jsonify(process_running=audio_running,
                       process_pid=audio_pid, process_type=audio_service_type,
                       process_name=audio_service_name)

    if service_name == "phal":
        phal_running = False
        phal_pid = str("NA")
        phal_service_type = str("NA")
        phal_service_name = str("NA")
        phal_list = get_phal_services()
        phal_services_list = phal_list[1]
        phal_process_list = phal_list[0]
        for phal_service in phal_services_list:
            if check_if_service_is_running(phal_service):
                phal_running = True
                phal_service_type = "systemd"
                phal_service_name = phal_service
                phal_pid = str("SYS-D")
                break

        for phal_process in phal_process_list:
            proc_running = check_process_is_running(phal_process)
            if proc_running[0]:
                phal_running = True
                phal_pid = proc_running[1]
                phal_service_type = "process"
                phal_service_name = phal_process + ".py"
                break

        return jsonify(process_running=phal_running,
                       process_pid=phal_pid, process_type=phal_service_type,
                       process_name=phal_service_name)

    return jsonify(process_running=False, process_pid=str("NA"))


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


@socketio.on('collect_skills_model')
def handle_collect_skills_model_event():
    sm_thread.run()


@app.route('/skill_settings_changed', methods=['POST'])
def on_skill_settings_changed():
    form_request = request.form.to_dict()
    form_skill_name = form_request["skill_name"]
    build_json_response = json.loads(form_request["form_data"])
    print(form_skill_name, build_json_response)

    # TODO: Make Save Settings Work After Getting Response
    return jsonify(Success=True)


if __name__ == "__main__":
    # app.run(debug=True)
    SimpleLogin(app)
    socketio.run(app, host="0.0.0.0", debug=True, use_reloader=False)
