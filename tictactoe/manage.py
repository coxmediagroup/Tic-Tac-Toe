#!/usr/bin/env python
import os
import sys

project_root_dir = os.path.dirname(__file__)
apps_dir = os.path.join(project_root_dir,"apps")

if not apps_dir in sys.path:
    sys.path.insert(0,apps_dir)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
