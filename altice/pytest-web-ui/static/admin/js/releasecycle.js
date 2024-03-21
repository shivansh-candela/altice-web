function check_releasecycle() {
    
    document.querySelector("#id_release_cycle_name").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_start_date_0").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    document.querySelector("#id_end_date_0").insertAdjacentHTML('afterend','<sup style="color:red;font-size:2re;">*</sup>')
    
}
$(document).ready(check_releasecycle);