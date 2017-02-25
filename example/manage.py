#!/usr/bin/env python
import os
import sys


# add parent path to PYTHONPATH so we can use current selectable package instead of installing it from pipy
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
