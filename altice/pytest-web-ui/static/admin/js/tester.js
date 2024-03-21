function check_Tester() {
    if(window.location.href.indexOf("change")>-1){
        document.querySelector('[for=id_email]').style.pointerEvents = "none";
        document.getElementById("id_email").style.pointerEvents = "none";
        document.getElementById("id_email").setAttribute("tabindex","-1");
        document.querySelector('[for=id_email]').setAttribute("tabindex","-1"); 

        document.querySelector('[for=id_name]').style.pointerEvents = "none";
        document.getElementById("id_name").style.pointerEvents = "none";
        document.getElementById("id_name").setAttribute("tabindex","-1");
        document.querySelector('[for=id_name]').setAttribute("tabindex","-1"); 
    }
    document.querySelector("#id_email").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_password").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_name").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    
}
$(document).ready(check_Tester);