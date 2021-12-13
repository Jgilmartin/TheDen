function login() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://localhost:5000/login", true);
    xhttp.send();

    xhttp.onload = function () {


    };
}

function signUp() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://localhost:5000/login", true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send();

    xhttp.onload = function () {


    };
}