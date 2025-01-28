$(document).ready(function() {
    $('#set-password-button').click(function() {
        const password = $('#master-password').val();
        $.ajax({
            url: '/set_master_password',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ password: password }),
            success: function(response) {
                alert(response.result);
            },
            error: function(response) {
                alert(response.responseJSON.error);
            }
        });
    });

    $('#login-button').click(function() {
        const password = $('#login-password').val();
        $.ajax({
            url: '/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ password: password }),
            success: function(response) {
                alert(response.result);
                $('#data-section').show();
            },
            error: function(response) {
                alert(response.responseJSON.error);
            }
        });
    });

    $('#add-data-button').click(function() {
        const dataType = $('#data-type').val();
        const data = $('#data-input').val();
        const password = $('#login-password').val();
        $.ajax({
            url: '/add_secure_data',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ data_type: dataType, data: data, password: password }),
            success: function(response) {
                alert(response.result);
            },
            error: function(response) {
                alert(response.responseJSON.error);
            }
        });
    });

    $('#get-data-button').click(function() {
        const dataType = $('#data-type').val();
        const password = $('#login-password').val();
        $.ajax({
            url: '/get_secure_data',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ data_type: dataType, password: password }),
            success: function(response) {
                $('#data-output').text(JSON.stringify(response.data));
            },
            error: function(response) {
                alert(response.responseJSON.error);
            }
        });
    });
});