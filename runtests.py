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
        INSTALLED_APPS=(
            'selectable',
        ),
        SITE_ID=1,
        SECRET_KEY='super-secret',
        ROOT_URLCONF='selectable.tests.urls',
    )


from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    args = sys.argv[1:] or ['selectable', ]
    failures = test_runner.run_tests(args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()

