const config = {
    apiBaseUrl: '/',
    commands: {
        setMasterPassword: 'setMasterPassword',
        login: 'login',
        addSecureData: 'addSecureData',
        getSecureData: 'getSecureData',
        encryptFile: 'encryptFile',
        decryptFile: 'decryptFile'
    },
    selectors: {
        masterPasswordInput: '#master-password',
        loginPasswordInput: '#login-password',
        dataTypeInput: '#data-type',
        dataInput: '#data-input',
        dataOutput: '#data-output',
        fileInput: '#file-input'
    }
};

$(document).ready(function() {
    // Main function to handle AJAX calls
    function ajaxCall(command, params) {
        let url;
        switch (command) {
            case config.commands.setMasterPassword:
                url = `${config.apiBaseUrl}set_master_password`;
                break;
            case config.commands.login:
                url = `${config.apiBaseUrl}login`;
                break;
            case config.commands.addSecureData:
                url = `${config.apiBaseUrl}add_secure_data`;
                break;
            case config.commands.getSecureData:
                url = `${config.apiBaseUrl}get_secure_data`;
                break;
            case config.commands.encryptFile:
                url = `${config.apiBaseUrl}encrypt_file`;
                break;
            case config.commands.decryptFile:
                url = `${config.apiBaseUrl}decrypt_file`;
                break;
            default:
                console.error('Invalid command');
                return;
        }

        $.ajax({
            url: url,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(params),
            success: function(response) {
                if (response.result) {
                    alert(response.result);
                } else if (response.data) {
                    $(config.selectors.dataOutput).text(JSON.stringify(response.data));
                }
            },
            error: function(response) {
                alert(response.responseJSON.error);
            }
        });
    }

    // Event listeners
    $(config.selectors.masterPasswordInput).on('click', function() {
        const password = $(config.selectors.masterPasswordInput).val();
        ajaxCall(config.commands.setMasterPassword, { password: password });
    });

    $(config.selectors.loginPasswordInput).on('click', function() {
        const password = $(config.selectors.loginPasswordInput).val();
        ajaxCall(config.commands.login, { password: password });
    });

    $('#add-data-button').click(function() {
        const dataType = $(config.selectors.dataTypeInput).val();
        const data = $(config.selectors.dataInput).val();
        const password = $(config.selectors.loginPasswordInput).val();
        ajaxCall(config.commands.addSecureData, { data_type: dataType, data: data, password: password });
    });

    $('#get-data-button').click(function() {
        const dataType = $(config.selectors.dataTypeInput).val();
        const password = $(config.selectors.loginPasswordInput).val();
        ajaxCall(config.commands.getSecureData, { data_type: dataType, password: password });
    });

    // Example for file encryption
    $('#encrypt-file-button').click(function() {
        const fileData = $(config.selectors.fileInput).prop('files')[0]; // Assuming you have a file input
        const password = $(config.selectors.loginPasswordInput).val();
        const formData = new FormData();
        formData.append('file', fileData);
        formData.append('password', password);
        ajaxCall(config.commands.encryptFile, formData);
    });

    // Example for file decryption
    $('#decrypt-file-button').click(function() {
        const fileData = $(config.selectors.fileInput).prop('files')[0]; // Assuming you have a file input
        const password = $(config.selectors.loginPasswordInput).val();
        const formData = new FormData();
        formData.append('file', fileData);
        formData.append('password', password);
        ajaxCall(config.commands.decryptFile, formData);
    });
});