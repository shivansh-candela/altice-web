function check_TB(){
    document.querySelector("#id_accesspoint").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_trafficgenerator").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_testbedname").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    if(window.location.href.indexOf("change")>-1){
        document.getElementById("id_testbedname").style.pointerEvents = "none";
        document.getElementById("id_testbedname").setAttribute("tabindex","-1");
        document.querySelectorAll('[for=id_testbedname]')[0].style.pointerEvents = "none";
        document.querySelectorAll('[for=id_testbedname]')[0].setAttribute("tabindex","-1");
        document.getElementById("id_accesspoint").style.pointerEvents = "none";
        document.getElementById("id_accesspoint").setAttribute("tabindex","-1");
        document.querySelectorAll('[for=id_accesspoint]')[0].style.pointerEvents = "none";
        document.querySelectorAll('[for=id_accesspoint]')[0].setAttribute("tabindex","-1");
        document.getElementById("id_trafficgenerator").style.pointerEvents = "none";
        document.getElementById("id_trafficgenerator").setAttribute("tabindex","-1");
        document.querySelectorAll('[for=id_trafficgenerator]')[0].style.pointerEvents = "none";
        document.querySelectorAll('[for=id_trafficgenerator]')[0].setAttribute("tabindex","-1");
        document.getElementById("add_id_accesspoint").style.display = "none";
        document.getElementById("add_id_accesspoint").setAttribute("tabindex","-1");
        document.getElementById("add_id_trafficgenerator").style.display = "none";
        document.getElementById("add_id_trafficgenerator").setAttribute("tabindex","-1");
        document.getElementById("id_status").style.pointerEvents =  "none";
        document.getElementById("id_status").setAttribute("tabindex","-1");
        document.querySelectorAll('[for=id_status]')[0].style.pointerEvents = "none";
        document.querySelectorAll('[for=id_status]')[0].style.setAttribute("tabindex","-1");
        document.querySelectorAll('[for=id_availability]')[0].style.pointerEvents = "none";
        document.querySelectorAll('[for=id_availability]')[0].setAttribute("tabindex","-1");
        document.querySelector('#change_id_accesspoint > img:nth-child(1)').src = "/static/admin/img/icon-viewlink.svg"
        document.querySelector('#change_id_accesspoint > img:nth-child(1)').title = "View Configuration"
        document.querySelector('#change_id_trafficgenerator > img:nth-child(1)').src = "/static/admin/img/icon-viewlink.svg"
        document.querySelector('#change_id_trafficgenerator > img:nth-child(1)').title = "View Configuration"
        var options = document.getElementById("id_accesspoint");
        for(i=0;i<options.length;i++){
            option = options[i];
            if(option.innerText.indexOf("attached")>-1){
                data = document.querySelector("#id_accesspoint > option:nth-child(" + (i+1).toString() + ")");
                data.innerText = data.innerText.replace(" : attached","");
            }
        }
        var options = document.getElementById("id_trafficgenerator");
        for(i=0;i<options.length;i++){
            option = options[i];
            if(option.innerText.indexOf("attached")>-1){
                data = document.querySelector("#id_trafficgenerator > option:nth-child(" + (i+1).toString() + ")");
                data.innerText = data.innerText.replace(" : attached","");
            }
        }
        if(!document.getElementById("id_status").checked){
            document.getElementById("id_availability").style.pointerEvents = "none";
            document.getElementById("id_availability").setAttribute("tabindex","-1");
            for (let el of document.querySelectorAll('.submit-row')) el.style.display = 'none';
        }
        element = document.querySelector(".deletelink-box");
            element.addEventListener('click', function(event) {
               if(document.getElementById("id_availability").checked) {
                alert("Cannot delete a testbed which is in available state");
                event.preventDefault();
               } 
            });
    }
    if(window.location.href.indexOf("add")>-1){
        document.getElementById("id_testbedname").setAttribute("autocomplete","off");
        document.getElementById("id_status").style.pointerEvents =  "none";
        document.getElementById("id_status").setAttribute("tabindex","-1");
        document.querySelectorAll('[for=id_status]')[0].style.pointerEvents = "none"; 
        document.querySelectorAll('[for=id_status]')[0].setAttribute("tabindex","-1");
        document.querySelector('#id_accesspoint > option:nth-child(1)').innerHTML = "Select an Accesspoint"
        document.querySelector('#id_trafficgenerator > option:nth-child(1)').innerHTML = "Select a Traffic Generator"
        var options = document.getElementById("id_accesspoint");
        for(i=0;i<options.length;i++){
            option = options[i];
            if(option.innerText.indexOf("attached")>-1){    
                data = document.querySelector("#id_accesspoint > option:nth-child(" + (i+1).toString() + ")");
                data.innerText = data.innerText.replace(" : attached","");
                data.disabled = true;
                // attached.push(option.value);
                // options.remove("option[value='" + (option.value).toString() + "']");               
            }
        }
        var options = document.getElementById("id_trafficgenerator");
        for(i=0;i<options.length;i++){
            option = options[i];
            if(option.innerText.indexOf("attached")>-1){
                data = document.querySelector("#id_trafficgenerator > option:nth-child(" + (i+1).toString() + ")");
                data.innerText = data.innerText.replace(" : attached","");
                data.disabled = true;
            }
        }
        fetch('/static/data_files/testbeds.json').then((response) => response.json()).then((json) => data=json);
        // data = data.value;
        document.querySelector("#id_testbedname").addEventListener('change', function(){
            if(data['testbed names'].includes(document.querySelector("#id_testbedname").value)){
                document.querySelector("div.form-row:nth-child(1) > div:nth-child(1) > div:nth-child(3)").innerHTML = "Testbed with this name already exists.";
                document.querySelector("div.form-row:nth-child(1) > div:nth-child(1) > div:nth-child(3)").style.color = "Red";
                for (let el of document.querySelectorAll('.submit-row')) el.style.display = 'none';
            }
            else{
                document.querySelector("div.form-row:nth-child(1) > div:nth-child(1) > div:nth-child(3)").innerHTML = "";  
                for (let el of document.querySelectorAll('.submit-row')) el.style.display = 'block';
            }
        });      
    }
}
$(document).ready(check_TB);
// #id_accesspoint > option:nth-child(2)