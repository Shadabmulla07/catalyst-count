document.getElementById("togbutton").addEventListener('click',function(){
    var fileinput=document.getElementById("hidden");
    fileinput.classList.remove("hidden");
})

var msgbox=document.querySelector('.msg')
if (msgbox){
    console.log("hiiiiiiiiiiiiii");
    setTimeout(function(){
        msgbox.style.display='none';
    },2000);
}