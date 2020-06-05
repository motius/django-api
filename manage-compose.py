#!/usr/bin/env python3
import argparse
import sys
import shutil
import subprocess

import os

from libs.compose import call_compose

example_text = '''examples:
  %(prog)s migrate
  %(prog)s makemessages -l de --ignore "env"
  %(prog)s db_entrypoint'''


if __name__ == "__main__":
    p = argparse.ArgumentParser(description='Use this in place of the manage.py script with Docker',
                                epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    known, unknown = p.parse_known_args()

    docker = shutil.which("docker")
    if docker:
        s = subprocess.check_output([docker, 'ps'])
        if s.find(b'smartdrivingbackend_app_1'):
            args = ['exec', 'app', 'python3', 'manage.py'] + unknown
            call_compose(*args)
        else:
            sys.stderr.write('Error: No running app container found\n')
            exit(1)
    else:
        sys.stderr.write('Error: No docker executable found\n')
        exit(1)
