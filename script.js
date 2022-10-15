window.onload=function() {
    var submit=document.querySelector('#submit');
    submit.onclick=runLoader;
}

//Function starts onclick as expected but stops and undoes everything immediately
function runLoader()
{
    document.querySelector('#loader').style.display = "block";

    var elem = document.getElementById("progress");
    var width = 1;
    var id = setInterval(frame, 10); //placeholder
    if (width >= 100) {
        clearInterval(id);
    } else {
        width++;
        elem.style.width = width + "%";
    }
}
