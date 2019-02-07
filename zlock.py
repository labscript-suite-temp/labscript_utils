#####################################################################
#                                                                   #
# zlock.py                                                          #
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
from os import execv
from socket import gethostbyname
from labscript_utils.ls_zprocess import get_config

"""Script to run a zlock server configured according to LabConfig. Run with:

    python -m labscript_utils.zlock
"""


def main():
    config = get_config()

    if gethostbyname(config['zlock_host']) != gethostbyname('localhost'):
        msg = (
            "Zlock not configured to run on this host according to labconfig: "
            + "zlock_host=%s" % config['zlock_host']
        )
        raise ValueError(msg)

    cmd = [
        sys.executable,
        '-m',
        'zprocess.zlock',
        '--port',
        config['zlock_port'],
    ]
    if config['shared_secret_file'] is not None:
        cmd += ['--shared-secret-file', config['shared_secret_file']]
    if config['allow_insecure']:
        cmd += ['--allow-insecure']

    # Replace the current process with the call to zlock:
    execv(sys.executable, cmd)


if __name__ == '__main__':
    main()
