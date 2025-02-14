document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const sidebarCollapse = document.getElementById('sidebarCollapse');

    // Toggle sidebar on button click
    sidebarCollapse.addEventListener('click', function () {
        sidebar.classList.toggle('active');
    });

    // Close sidebar if clicked outside
    document.addEventListener('click', function (event) {
        if (!sidebar.contains(event.target) && !sidebarCollapse.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });

    // Handle user icon click for login/logout
    const userIcon = document.getElementById('userIcon');
    const userPopup = document.getElementById('userPopup');
    const headerLoginForm = document.getElementById('headerLoginForm');
    const headerRegisterForm = document.getElementById('headerRegisterForm');
    const sidebarLoginForm = document.getElementById('sidebarLoginForm');
    const sidebarRegisterForm = document.getElementById('sidebarRegisterForm');

    if (userIcon) {
        userIcon.addEventListener('click', function (event) {
            event.stopPropagation();
            userPopup.classList.toggle('d-none');
            positionUserPopup();
        });
    }

    // Hide user popup when clicking outside
    document.addEventListener('click', function (event) {
        if (!userPopup.contains(event.target) && !userIcon.contains(event.target)) {
            userPopup.classList.add('d-none');
        }
    });

    // Validate register form
    if (headerRegisterForm) {
        headerRegisterForm.addEventListener('submit', function (event) {
            const registerPassword = document.getElementById('headerRegisterPassword');
            const confirmPassword = document.getElementById('headerConfirmPassword');
            if (registerPassword.value !== confirmPassword.value) {
                event.preventDefault();
                document.getElementById('headerRegisterError').textContent = 'Passwords do not match!';
            }
        });
    }

    if (sidebarRegisterForm) {
        sidebarRegisterForm.addEventListener('submit', function (event) {
            const registerPassword = document.getElementById('sidebarRegisterPassword');
            const confirmPassword = document.getElementById('sidebarConfirmPassword');
            if (registerPassword.value !== confirmPassword.value) {
                event.preventDefault();
                document.getElementById('sidebarRegisterError').textContent = 'Passwords do not match!';
            }
        });
    }

    // Handle login form submissions and redirects
    if (headerLoginForm) {
        headerLoginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(headerLoginForm);
            fetch(headerLoginForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    document.getElementById('headerLoginError').textContent = data.message;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    if (sidebarLoginForm) {
        sidebarLoginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(sidebarLoginForm);
            fetch(sidebarLoginForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    document.getElementById('sidebarLoginError').textContent = data.message;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Function to position the user popup
    function positionUserPopup() {
        const iconRect = userIcon.getBoundingClientRect();
        const popupRect = userPopup.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
        const rightEdge = viewportWidth - scrollbarWidth;

        let left = iconRect.left + (iconRect.width / 2) - (popupRect.width / 2);
        if (left + popupRect.width > rightEdge) {
            left = rightEdge - popupRect.width;
        }
        userPopup.style.left = `${left}px`;
        userPopup.style.top = `${iconRect.bottom + window.scrollY}px`;
    }

    // Check authentication status on page load
    fetch('/auth_status', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_authenticated) {
            document.getElementById('headerLoginRegisterLink').style.display = 'none';
            document.getElementById('headerLogoutLink').style.display = 'block';
            document.getElementById('sidebarLoginRegisterLink').style.display = 'none';
            document.getElementById('sidebarLogoutLink').style.display = 'block';
        } else {
            document.getElementById('headerLoginRegisterLink').style.display = 'block';
            document.getElementById('headerLogoutLink').style.display = 'none';
            document.getElementById('sidebarLoginRegisterLink').style.display = 'block';
            document.getElementById('sidebarLogoutLink').style.display = 'none';
        }
    })
    .catch(error => console.error('Error:', error));
});