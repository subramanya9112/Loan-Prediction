function Login() {
    var url_to_change = window.location.href + "#";
    window.location.href = url_to_change.substr(0, url_to_change.indexOf("#") + 1) + "Login";
    $("#registermodal").modal('hide');
    $("#loginmodal").modal();
}

function Register() {
    var url_to_change = window.location.href + "#";
    window.location.href = url_to_change.substr(0, url_to_change.indexOf("#") + 1) + "Register";
    $("#loginmodal").modal('hide');
    $("#registermodal").modal();
}

function Close() {
    $("#loginmodal").modal('hide');
    $("#registermodal").modal('hide');
}