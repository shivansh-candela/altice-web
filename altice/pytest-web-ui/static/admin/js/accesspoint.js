function check_AP(){
    document.getElementById("id_attached").style.pointerEvents =  "none";
    document.getElementById("id_attached").setAttribute("tabindex","-1");
    document.querySelectorAll('[for=id_attached]')[0].style.pointerEvents = "none";
    document.querySelectorAll('[for=id_attached]')[0].setAttribute("tabindex","-1");
    if(document.getElementById("id_attached").checked){
        for (let el of document.querySelectorAll('.submit-row')) el.style.display = 'none';
        alert("Cannot Change the Configuration of the Accesspoint as it is attached to a Testbed");
    }

    document.querySelector("#id_model").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_mode").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_serial").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_jumphost").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_ip").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_username").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_password").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_port").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_jumphost_tty").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_ap_username").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_ap_password").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_ap_prompt").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')



}
$(document).ready(check_AP);