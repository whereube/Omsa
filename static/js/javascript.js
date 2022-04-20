document.getElementById("us").value = getSavedValue("us");    // set the value to this input
document.getElementById("ps").value = getSavedValue("ps"); 
document.getElementById("el").value = getSavedValue("el");
document.getElementById("fn").value = getSavedValue("fn");
document.getElementById("ln").value = getSavedValue("ln");
document.getElementById("as").value = getSavedValue("as");
document.getElementById("zp").value = getSavedValue("zp");
document.getElementById("pn").value = getSavedValue("pn"); // set the value to this input
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


