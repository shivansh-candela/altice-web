"""
WSGI config for pytest_web_ui project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os,time,traceback,signal,sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pytest_web_ui.settings')

try:

        application = get_wsgi_application()
except Exception:
        if 'mod_wsgi' in sys.modules:
                traceback.print_exec()
                os.kill(os.getpid(),signal.SIGNIT)
                time.sleep(2.5)

