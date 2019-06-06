var login = document.querySelector("#login");
var loginPanel = document.querySelector(".nav-links .login");
if (login) {
    login.onclick = function () {
        loginPanel.classList.toggle("open");
    }
}


var xmlhttp;
var ajt;
if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
}
else {
    xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
}
xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        ajt.innerHTML = xmlhttp.responseText;
    }
}
var s = document.querySelector('.user-items');
if (s) {
    s.onclick = function (e) {

        if (e.target.getAttribute('class') === 'more' || e.target.getAttribute('class') === 'aj') {
            e.preventDefault();//阻止跳转
            xmlhttp.open('GET', e.target.href, true);//true为异步请求
            xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");//django通过Header的X-Requested-With判断是否是ajax请求
            xmlhttp.send();
            ajt = this;
        }

    }
}