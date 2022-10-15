window.onload=function() {
    var button=document.querySelector('#submit');
    button.onclick=runLoader;
}

function runLoader()
{
    var load=document.querySelector('#loader');
    load.classList.remove('hidden');
}