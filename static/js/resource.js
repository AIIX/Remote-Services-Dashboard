$.postJSON = function(url, data, func){ $.post(url+(url.indexOf("?") == -1 ? "?" : "&")+"callback=?", data, func, "json");};

var messagebus_process = {
    "process_name": "NA",
    "process_type": "NA",
    "process_pid": "NA"
}

var skills_process = {
    "process_name": "NA",
    "process_type": "NA",
    "process_pid": "NA"
}

var audio_process = {
    "process_name": "NA",
    "process_type": "NA",
    "process_pid": "NA"
}

var voice_process = {
    "process_name": "NA",
    "process_type": "NA",
    "process_pid": "NA"
}

var gui_process = {
    "process_name": "NA",
    "process_type": "NA",
    "process_pid": "NA"
}

var phal_process = {
    "process_name": "NA",
    "process_type": "NA",
    "process_pid": "NA"
}

$(function worker(){
    // don't cache ajax or content won't be fresh
    $.ajaxSetup ({
        cache: false,
        complete: function() {
          // Schedule the next request when the current one's complete
          setTimeout(worker, 6000);
        }
    });
    $.getJSON("/update/_sys_info",
    function(data) {
        $("#cpu_area").text(data.cpu+" %")
        $("#mem_area").text(data.ram+" %")
        $("#storage_area").text(data.disk+" %")
    });
});

//$(function worker_check_process(){
////    // don't cache ajax or content won't be fresh
//    $.ajaxSetup ({
//        cache: false,
//        complete: function() {
////          // Schedule the next request when the current one's complete
//          setTimeout(worker_check_process, 10000);
//        }
//    });
//    $.post("/update/_check_process_status", { process: "mycroft" },
//    function(data) {
//        console.log(data.process_running)
//    }, "json");
//});

$(function check_messagebus_service_status(){
    $.ajaxSetup ({
        cache: false,
        complete: function() {
          setTimeout(check_messagebus_service_status, 10000);
        }
    });
    $.post("/update/_check_process_status", { service: "messagebus" },
    function(data) {
        var e = document.getElementById("status-messagebus");
        var f = document.getElementById("messagebus-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
        messagebus_process.process_type = data.process_type
        messagebus_process.process_name = data.process_name
        messagebus_process.process_pid = data.process_pid
    }, "json");
});

$(function check_skills_service_status(){
    $.ajaxSetup ({
        cache: false,
        complete: function() {
          setTimeout(check_skills_service_status, 10000);
        }
    });
    $.post("/update/_check_process_status", { service: "skills" },
    function(data) {
        var e = document.getElementById("status-skills");
        var f = document.getElementById("skill-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
        skills_process.process_type = data.process_type
        skills_process.process_name = data.process_name
        skills_process.process_pid = data.process_pid
    }, "json");
});

$(function check_audio_service_status(){
    $.ajaxSetup ({
        cache: false,
        complete: function() {
          setTimeout(check_audio_service_status, 10000);
        }
    });
    $.post("/update/_check_process_status", { service: "audio" },
    function(data) {
        var e = document.getElementById("status-audio");
        var f = document.getElementById("audio-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
        audio_process.process_type = data.process_type
        audio_process.process_name = data.process_name
        audio_process.process_pid = data.process_pid
    }, "json");
});

$(function check_voice_service_status(){
    $.ajaxSetup ({
        cache: false,
        complete: function() {
          setTimeout(check_voice_service_status, 10000);
        }
    });
    $.post("/update/_check_process_status", { service: "voice" },
    function(data) {
        var e = document.getElementById("status-voice");
        var f = document.getElementById("voice-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
        voice_process.process_type = data.process_type
        voice_process.process_name = data.process_name
        voice_process.process_pid = data.process_pid
    }, "json");
});

$(function check_gui_service_status(){
    $.ajaxSetup ({
        cache: false,
        complete: function() {
          setTimeout(check_gui_service_status, 10000);
        }
    });
    $.post("/update/_check_process_status", { service: "gui" },
    function(data) {
        var e = document.getElementById("status-gui");
        var f = document.getElementById("gui-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
        gui_process.process_type = data.process_type
        gui_process.process_name = data.process_name
        gui_process.process_pid = data.process_pid
    }, "json");
});

$(function check_phal_service_status(){
    $.ajaxSetup ({
        cache: false,
        complete: function() {
          setTimeout(check_gui_service_status, 10000);
        }
    });
    $.post("/update/_check_process_status", { service: "phal" },
    function(data) {
        var e = document.getElementById("status-phal");
        var f = document.getElementById("phal-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
        phal_process.process_type = data.process_type
        phal_process.process_name = data.process_name
        phal_process.process_pid = data.process_pid
    }, "json");
});

$(function update_platform_info(){
    // don't cache ajax or content won't be fresh
    $.ajaxSetup ({
        cache: false,
        complete: function() {
          // Schedule the next request when the current one's complete
          setTimeout(update_platform_info, 600000);
        }
    });
    $.getJSON("/update/_platform_info",
    function(data) {
        document.getElementById('sys_info_platform').innerHTML = "Platform: " + data.plaform_type
        document.getElementById('sys_info_processor').innerHTML = "Processer: " + data.platform_info
        document.getElementById('sys_info_local_ip').innerHTML = "Local IP: " + data.platform_ip
    });
});

function run_myc_process(type_cmd){
    $.post("/myc/control", { command: type_cmd },
    function(data) {
        console.log(data.processed_myc)
        check_messagebus_service_status_m()
        check_skills_service_status_m()
        check_audio_service_status_m()
        check_voice_service_status_m()
        check_enclosure_service_status_m()
    }, "json");
};

function check_audio_service_status_m(){
    $.post("/update/_check_process_status", { process: "mycroft.audio" },
    function(data) {
        var e = document.getElementById("status-audio");
        var f = document.getElementById("audio-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
    }, "json");
}

function check_voice_service_status_m(){
    $.post("/update/_check_process_status", { process: "mycroft.client.speech" },
    function(data) {
        var e = document.getElementById("status-voice");
        var f = document.getElementById("voice-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
    }, "json");
}

function check_skills_service_status_m(){
    $.post("/update/_check_process_status", { process: "mycroft.skills" },
    function(data) {
        var e = document.getElementById("status-skills");
        var f = document.getElementById("skill-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
    }, "json");
}

function check_messagebus_service_status_m(){
    $.post("/update/_check_process_status", { process: "mycroft.messagebus.service" },
    function(data) {
        var e = document.getElementById("status-messagebus");
        var f = document.getElementById("messagebus-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
    }, "json");
}

function check_enclosure_service_status_m(){
    $.post("/update/_check_process_status", { process: "mycroft.client.enclosure" },
    function(data) {
        var e = document.getElementById("status-enclosure");
        var f = document.getElementById("enclosure-pid")
        f.innerHTML = data.process_pid
        if(data.process_running) {
            if (e.classList.contains('fa-times')) {
                e.classList.remove('fa-times')
                e.classList.add('fa-check')
                e.classList.remove('statusunticked')
                e.classList.add('statusticked')
            }
        } else {
            if (e.classList.contains('fa-check')) {
                e.classList.remove('fa-check')
                e.classList.add('fa-times')
                e.classList.remove('statusticked')
                e.classList.add('statusunticked')
            }
        }
    }, "json");
}