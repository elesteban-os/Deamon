from plyer import notification # pip install plyer

# notification function
def notify(title, message, app_icon=None):
    notification.notify(
        title=title,
        message=message,
        app_name='My Application',
        app_icon=app_icon,  
        timeout=5
    )