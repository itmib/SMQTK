#!/usr/bin/env python
"""
Create an ingest of files in a specified directory.
"""

import glob
import logging
import os.path as osp

import smqtk_config

from SMQTK.utils import DataIngest


def main():
    import optparse

    usage = """%prog [options] GLOB [ GLOB [ ... ] ]"""

    parser = optparse.OptionParser(usage)
    parser.add_option('-t', '--type',
                      help="Ingest data type. Currently supports 'image' or "
                           "'video'.")
    parser.add_option('-d',
                      help="Custom directory to base the ingest in. Otherwise "
                           "we use the system default based on the ingest "
                           "type.")
    parser.add_option('-v', '--verbose', action='store_true', default=False,
                      help='Add debug messaged to output logging.')
    opts, args = parser.parse_args()

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    if opts.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if opts.type not in ('image', 'video'):
        raise RuntimeError("Invalid ingest type! Given: %s" % opts.type)
    t = opts.type
    t = t[0].upper() + t[1:]

    if opts.d:
        target_dir = opts.d
    else:
        target_dir = osp.join(smqtk_config.DATA_DIR,
                              smqtk_config.SYSTEM_CONFIG['Ingest'][t])
    work_dir = osp.join(smqtk_config.WORK_DIR,
                        smqtk_config.SYSTEM_CONFIG['Ingest'][t])

    ingest = DataIngest(target_dir, work_dir)
    print "Script arguments:\n%s" % args
    for g in args:
        if osp.isfile(g):
            ingest.add_data_file(g)
        else:
            for fp in glob.glob(g):
                ingest.add_data_file(fp)


if __name__ == '__main__':
    main()
