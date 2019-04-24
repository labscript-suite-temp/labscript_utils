#####################################################################
#                                                                   #
# remote.py                                                         #
#                                                                   #
# Copyright 2013, Monash University                                 #
#                                                                   #
# This file is part of the labscript suite (see                     #
# http://labscriptsuite.org) and is licensed under the Simplified   #
# BSD License. See the license.txt file in the root of the project  #
# for the full license.                                             #
#                                                                   #
#####################################################################

from __future__ import division, unicode_literals, print_function, absolute_import
from labscript_utils import PY2

if PY2:
    str = unicode

import sys
import subprocess
from labscript_utils.ls_zprocess import get_config
from zprocess import start_daemon

"""Script to run a zprocess.remote server configured according to LabConfig. Run with:

    python -m labscript_utils.remote [--daemon]

if --daemon is specified, the server will be started in the background.
"""


def main():
    config = get_config()

    cmd = [
        sys.executable,
        '-m',
        'zprocess.remote',
        '--port',
        str(config['zprocess_remote_port']),
        '-tui'
    ]
    if config['shared_secret_file'] is not None:
        cmd += ['--shared-secret-file', config['shared_secret_file']]
    if config['allow_insecure']:
        cmd += ['--allow-insecure']

    if '--daemon' in sys.argv:
        cmd.remove('-tui')
        start_daemon(cmd)
    else:
        subprocess.call(cmd)

if __name__ == '__main__':
    main()
