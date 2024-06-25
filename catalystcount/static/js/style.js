var msgbox=document.querySelector('.msg')
if (msgbox){
    console.log("hiiiiiiiiiiiiii");
    setTimeout(function(){
        msgbox.style.display='none';
    },2000);
}

$(document).ready(function() {
    $('#queryForm').submit(function(event) {
        event.preventDefault();
        console.log("inside queryform");
        var formData = {
            'Companyname': $('#Companyname').val(),
            'Domain': $('#Domain').val(),
            'Yearfounded': $('#Yearfounded').val(),
            'Country': $('#Country').val(),
            'Currenteployees': $('#Currenteployees').val(),
            'Totalemployees': $('#Totalemployees').val()
        };
        console.log(formData);
        $.ajax({
            type: 'POST',
            url: '/api/querybuilder/',
            data: formData,
            success: function(response) {
                console.log('success');
                console.log(response);
                $('#results').html('<p>Row count: ' + response + '</p>');
                if (response.data && response.data.length > 0) {
                    $('#results').append('<p>Data:</p>');
                    response.data.forEach(function(item) {
                        $('#results').append('<p>' + JSON.stringify(item) + '</p>');
                    });
                }
            },
            error: function(xhr, errmsg, err) {
                $('#results').html('<p>Error: ' + xhr.status + ' - ' + errmsg + '</p>');
            }
        });
    });
});

