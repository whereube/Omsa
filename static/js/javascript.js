document.getElementById("validationTooltipUsername").value = getSavedValue("validationTooltipUsername");    // set the value to this input
document.getElementById("exampleInputPassword1").value = getSavedValue("exampleInputPassword1"); 
document.getElementById("exampleInputEmail1").value = getSavedValue("exampleInputEmail1");
document.getElementById("validationTooltip01").value = getSavedValue("validationTooltip01");
document.getElementById("validationTooltip02").value = getSavedValue("validationTooltip02");
document.getElementById("validationTooltip03").value = getSavedValue("validationTooltip03");
document.getElementById("validationTooltip04").value = getSavedValue("validationTooltip04");
document.getElementById("validationTooltip05").value = getSavedValue("validationTooltip05"); // set the value to this input
        /* Here you can add more inputs to set value. if it's saved */

        //Save the value function - save it to localStorage as (ID, VALUE)
function saveValue(e){
    var id = e.id;  // get the sender's id to save it . 
    var val = e.value; // get the value. 
    localStorage.setItem(id, val);// Every time user writing something, the localStorage's value will override . 
}

        //get the saved value function - return the value of "v" from localStorage. 
function getSavedValue  (v){
    if (!localStorage.getItem(v)) {
        return "";// You can change this to your defualt value. 
    }
    return localStorage.getItem(v);
    }

