$(document).ready(function () {
    'use-strict';
    
    $('#id_upload_field').on('click', function(){
        $('#id_url_field').val('');
        $('#id_url_field').removeAttr('required');
        $('#id_upload_field').attr('required', 'required');
    });

    $('#id_url_field').on('focus', function(){
        $('#id_upload_field').removeAttr('required');
        $('#id_url_field').attr('required', 'required');
    });
    
    $('#id_url_field').keydown(function (event) {
        if (event.keyCode == 13) {
            $("form").submit();
        }
    });

    $('#id_upload_field').change(function(){
        $('form').submit();
    });
});
