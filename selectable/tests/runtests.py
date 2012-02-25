#!/usr/bin/env python
import os
import sys

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test.db',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'selectable',
        ),
        SITE_ID=1,
        ROOT_URLCONF='selectable.tests.urls',
    )


from django.test.utils import get_runner


def runtests(*test_args):
    if not test_args:
        test_args = ['selectable']
    parent = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", )
    sys.path.insert(0, parent)
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])

