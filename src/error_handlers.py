from flask import render_template
import logging

def handle_error(error_code):
    """Handle errors based on the error code."""
    logging.error(f"Error occurred with code: {error_code}")

    if error_code == 401:
        return render_template('errors/401.html'), 401
    elif error_code == 403:
        return render_template('errors/403.html'), 403
    elif error_code == 404:
        return render_template('errors/404.html'), 404
    elif error_code == 500:
        return render_template('errors/500.html'), 500
    else:
        return render_template('errors/generic_error.html'), error_code  # A generic error page for other codes