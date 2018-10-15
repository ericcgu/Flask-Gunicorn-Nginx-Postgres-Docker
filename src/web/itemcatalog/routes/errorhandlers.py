from flask import Blueprint, render_template

errorhandlers = Blueprint('errorhandlers', __name__)


@errorhandlers.app_errorhandler(404)
def error_404(error):
    """Custom 404 Not Found"""
    return render_template('errors/404.html'), 404


@errorhandlers.app_errorhandler(403)
def error_403(error):
    """Custom 403 Not Authorized"""
    return render_template('errors/403.html'), 403


@errorhandlers.app_errorhandler(500)
def error_500(error):
    """Custom 500 Server Error"""
    return render_template('errors/500.html'), 500
