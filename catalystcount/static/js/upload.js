var msgbox=document.querySelector('.msg');
var myfile=document.getElementById('filename');
var excelfile=document.getElementById('excelfile')
var submit=document.getElementById('submit')

if(msgbox){
    setTimeout(function(){
        msgbox.style.display='none';

    },2000)
}

excelfile.addEventListener('change',function(){
    var count=excelfile.ariaValueMax;
    var filename=count.split('\\').pop();
    myfile.value=filename;
    myfile.classList.remove('hidden');
})

submit.addEventListener('click',function(){
    myfile.classList.toggle('hidden');
})