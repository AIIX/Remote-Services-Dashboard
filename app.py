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

import platform
import socket
import os
import cpuinfo
import psutil
import subprocess
from flask import Flask, render_template, jsonify, request, make_response
from flask_fontawesome import FontAwesome
from flask_socketio import SocketIO, emit

from lthreads.buslogthread import BusLogThread
from lthreads.skilllogthread import SkillLogThread
from lthreads.audiologthread import AudioLogThread
from lthreads.voicelogthread import VoiceLogThread
from lthreads.enclosurelogthread import EnclosureLogThread


app = Flask(__name__)
fa = FontAwesome(app)
socketio = SocketIO(app)

bs_thread = BusLogThread()
sk_thread = SkillLogThread()
au_thread = AudioLogThread()
vu_thread = VoiceLogThread()
enc_thread = EnclosureLogThread()


@app.route("/")
def home():
    return render_template("index.html")


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})


@app.route("/logging")
def dashlog():
    return render_template("log.html")


@app.route("/docs/rs/introduction")
def dashdocintro():
    return render_template("rs-intro.html")


@app.route("/docs/rs/connection-guide")
def dashdocconnect():
    return render_template("rs-connection.html")


@app.route("/docs/rs/dashboard-guide")
def dashdocdash():
    return render_template("rs-dashboard.html")


@app.route("/logging/messsagebus")
def show_bus_log():
    resp = make_response(render_template("bus.html"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers['Cache-Control'] = 'public, max-age=0'
    resp.set_cookie('SameSite=', 'Lax')
    return resp


@app.route("/logging/skills")
def show_skills_log():
    resp = make_response(render_template("skills.html"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers['Cache-Control'] = 'public, max-age=0'
    resp.set_cookie('SameSite=', 'Lax')
    return resp


@app.route("/logging/audio")
def show_audio_log():
    resp = make_response(render_template("audio.html"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers['Cache-Control'] = 'public, max-age=0'
    resp.set_cookie('SameSite=', 'Lax')
    return resp


@app.route("/logging/voice")
def show_voice_log():
    resp = make_response(render_template("voice.html"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers['Cache-Control'] = 'public, max-age=0'
    resp.set_cookie('SameSite=', 'Lax')
    return resp


@app.route("/logging/enclosure")
def show_enclosure_log():
    resp = make_response(render_template("enclosure.html"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers['Cache-Control'] = 'public, max-age=0'
    resp.set_cookie('SameSite=', 'Lax')
    return resp


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


@app.route("/update/_check_process_status", methods=['POST'])
def check_if_process_is_running():
    """
    Check if there is any running process that contains the given name processName.
    """
    proc = request.form.to_dict()
    process_name = proc["process"]
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            proc_cmd = proc.cmdline()
            if process_name.lower() in proc_cmd[2]:
                # print("Process Check True")
                # print(proc.pid)
                return jsonify(process_running=True, process_pid=str(proc.pid))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, IndexError):
            pass
    # print("Process Check Failed")
    return jsonify(process_running=False, process_pid=str("NA"))


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


@socketio.on('connect_event')
def handle_connect_event(json):
    current_log_requested = json['data']['from']
    if current_log_requested == "bus":
        print("Opening Type Bus Log")
        bs_thread.run()
    elif current_log_requested == "skills":
        print("Opening Type Skills Log")
        sk_thread.run()
    elif current_log_requested == "audio":
        print("Opening Type Audio Log")
        au_thread.run()
    elif current_log_requested == "voice":
        print("Opening Type Voice Log")
        vu_thread.run()
    elif current_log_requested == "enclosure":
        print("Opening Type Enclosure Log")
        enc_thread.run()
    else:
        print("unknown log display requested")


@app.route('/logging/_close_log', methods=['POST'])
def logging_close_log():
    prequest = request.form.to_dict()
    log_type = prequest["d_type"]
    if log_type == "bus":
        print("Closing Type Bus Log")
        bs_thread.kill()
    elif log_type == "skills":
        print("Closing Type Skills Log")
        sk_thread.kill()
    elif log_type == "audio":
        print("Closing Type Audio Log")
        au_thread.kill()
    elif log_type == "voice":
        print("Closing Type Voice Log")
        vu_thread.kill()
    elif log_type == "enclosure":
        print("Closing Type Enclosure Log")
        enc_thread.kill()
    else:
        print("unknown log closure")

    return jsonify(ClosedLog=True)


@app.route("/myc/control", methods=['POST'])
def control_myc():
    prereq = request.form.to_dict()
    proc_cmd = prereq["command"]
    if proc_cmd == "start":
        command = os.path.join(os.path.dirname(__file__) + "/static/assets/scripts/start-myc.sh")
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=None)

    elif proc_cmd == "stop":
        command = os.path.join(os.path.dirname(__file__) + "/static/assets/scripts/stop-myc.sh")
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=None)
    elif proc_cmd == "restart":
        command = os.path.join(os.path.dirname(__file__) + "/static/assets/scripts/restart-myc.sh")
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=None)
    else:
        print("Invalid Move")

    return jsonify(processed_myc=True)


if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)
