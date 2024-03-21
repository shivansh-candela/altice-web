function check_TG(){
    document.getElementById("id_attached").style.pointerEvents =  "none";
    document.getElementById("id_attached").setAttribute("tabindex","-1");
    document.querySelectorAll('[for=id_attached]')[0].style.pointerEvents = "none";
    document.querySelectorAll('[for=id_attached]')[0].setAttribute("tabindex","-1");
    if(document.getElementById("id_attached").checked){
        for (let el of document.querySelectorAll('.submit-row')) el.style.display = 'none';
        alert("Cannot Change the Configuration of the Traffic Generator as it is attached to a Testbed");
    }

    document.querySelector("#id_name").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        document.querySelector("#id_ip").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        document.querySelector("#id_port").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        document.querySelector("#id_ssh_port").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        document.querySelector("#id_twog_radio").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        document.querySelector("#id_fiveg_radio").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        document.querySelector("#id_upstream").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        // document.querySelector("#id_lan_upstream").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        document.querySelector("#id_twog_station_name").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
        document.querySelector("#id_fiveg_station_name").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')

}
$(document).ready(check_TG);