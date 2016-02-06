#!/usr/bin/env python
import os
import sys

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        MIDDLEWARE_CLASSES=(),
        INSTALLED_APPS=(
            'selectable',
        ),
        SITE_ID=1,
        SECRET_KEY='super-secret',
        ROOT_URLCONF='selectable.tests.urls',
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.path.normpath(os.path.join(
                os.path.dirname(__file__), 'selectable')), 'templates')]}])


from django import setup
from django.test.utils import get_runner


def runtests():
    setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    args = sys.argv[1:] or ['selectable', ]
    failures = test_runner.run_tests(args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
