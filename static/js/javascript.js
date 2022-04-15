/*
let username = document.getElementById('user_name');
let password = document.getElementById('user_password');
let email = document.getElementById('user_email');
let firstname = document.getElementById('user_f_name');
let lastname = document.getElementById('user_l_name');
let adress = document.getElementById('user_adress');
let zip_code = document.getElementById('user_zip_code'); 
let city = document.getElementById('city');
let number = document.getElementById('user_phone_number');

localStorage.setItem('username', username);
localStorage.setItem('password', password);
localStorage.setItem('email', email);
localStorage.setItem('firstname', firstname);
localStorage.setItem('lastnme', lastname);
localStorage.setItem('adress', adress);
localStorage.setItem('zip_code', zip_code);
localStorage.setItem('city', city);
localStorage.setItem('number', number);



let create_users = [];
        // example {id:1592304983049, title: 'Deadpool', year: 2015}
        const user = (ev)=>{
            ev.preventDefault();  //to stop the form submitting
            let create_user = {
                id:Date.now(),
                username: document.getElementById('us').value,
                password: document.getElementById('ps').value,
                email: document.getElementById('el').value,
                firstname: document.getElementById('fn').value,
                lastname: document.getElementById('ln').value,
                adress: document.getElementById('as').value,
                zip_code: document.getElementById('zp').value, 
                city: document.getElementById('city').value,
                number: document.getElementById('pn'.value)
            }
            create_users.push(create_user);
            document.forms[0].reset(); // to clear the form for the next entries
            //document.querySelector('form').reset();

            //for display purposes only
            console.warn('added' , {create_users} );
            let pre = document.querySelector('#msg pre');
            pre.textContent = '\n' + JSON.stringify(create_users, '\t', 2);

            //saving to localStorage
            localStorage.setItem('create', JSON.stringify(create_users) );
        };*/

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
        
        function saveValue(e){
            var id = e.id;  // get the sender's id to save it . 
            var val = e.value; // get the value. 
            localStorage.removeItem(id, val);// Every time user writing something, the localStorage's value will override . 
        }
        