#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
   delFiles - Delete log files(support several deletion method)

   Version: 2.3 (2017-03-4)
   Dev: Shavit Ilan (ilan.shavit@gmail.com)
"""

import logging
import glob
from ConfigParser import SafeConfigParser
from datetime import date
import os


def del_file_timestamp(base_dir, files_template, keep_files, \
                       simulation_mode, recursive_mode):
    """
        delete files on FILE_FIMESTAMP method
    """
    all_dir = [base_dir]
    if recursive_mode == "Y":
        all_dir.append([name for name in os.listdir(base_dir) \
            if os.path.isdir(os.path.join(base_dir, name))])
    else:
        all_dir.append([])
    all_dir[1].append('.')

    for each_dir in all_dir[1]:
        os.chdir(base_dir)
        os.chdir(each_dir)
        files_list = glob.glob(files_template)
        files_list = sorted(files_list)
        num_files = len(files_list)

        if (num_files - keep_files) <= 0:
            log_message = "%s/%s: No files to delete..." % (base_dir, each_dir)
            if simulation_mode == 'Y':
                print log_message
            else:
                logging.info(log_message)


        for temp_i in range(num_files - int(keep_files)):
            log_message = "%s/%s/%s" % (base_dir, each_dir, files_list[temp_i])
            if simulation_mode == 'Y':
                print log_message + " - Going to delete..."
            else:
                try:
                    os.remove(files_list[temp_i])
                    logging.info(log_message + " - Deleted!")
                except OSError:
                    log_message = "%s/%s/%s - OSError exception raised !!!" %\
                            (base_dir, each_dir, files_list[temp_i])
                    logging.error(log_message)


def del_file_creation(base_dir, files_template, keep_days, simulation_mode, \
                      recursive_mode):
    """
        delete files on FILE_CREATION method
    """
    all_dir = [base_dir]
    if recursive_mode == "Y":
        all_dir.append([name for name in os.listdir(base_dir) \
            if os.path.isdir(os.path.join(base_dir, name))])
    else:
        all_dir.append([])
    all_dir[1].append('.')

    current_date = date.today()
    for each_dir in all_dir[1]:
        os.chdir(base_dir)
        os.chdir(each_dir)
        files = glob.glob(files_template)
        need_delete = False
        for each_file in files:
            try:
                the_file = os.path.getmtime(each_file)
                the_file_ts = date.fromtimestamp(the_file)
                days_diff = (current_date - the_file_ts).days
                if days_diff > keep_days:
                    need_delete = True
                    log_message = "%s/%s/%s" % (base_dir, each_dir, each_file)
                    if simulation_mode == 'Y':
                        print log_message + " - Going to delete..."
                    else:
                        os.remove(each_file)
                        logging.info(log_message + " - Deleted!")
            except OSError:
                log_message = "%s/%s/%s -  OSError Excepion Raised !!!" %\
                        (base_dir, each_dir, each_file)
                logging.error(log_message)
            except TypeError:
                log_message = "%s/%s/%s -  TypeError Exception Raised !!!" %\
                        (base_dir, each_dir, each_file)
                logging.error(log_message)
            except Exception, the_err:
                log_message = "%s/%s/%s - %s !!!" %\
                        (base_dir, each_dir, each_file, str(the_err))
                logging.error(log_message)

        if not need_delete:
            log_message = "%s/%s -  No files to delete..." %\
                        (base_dir, each_dir)
            if simulation_mode == 'Y':
                print log_message
            else:
                logging.info(log_message)


def main():
    """
        Explain the function of the main program
    """
    ini_file = "del_files.ini"
    log_file = "del_files.log"

    logging.basicConfig(filename=log_file, level=logging.INFO,\
        format='%(asctime)s - %(levelname)s - %(message)s')
    parser = SafeConfigParser()
    parser.read(ini_file)
    simulation_mode = parser.get('CONFIG', 'SIMULATION_MODE')
    base_dir = parser.get('CONFIG', 'BASE_DIR')
    recursive_mode = parser.get('CONFIG', 'RECURSIVE_MODE')
    method = parser.get('CONFIG', 'METHOD')
    keep = int(parser.get('CONFIG', 'KEEP'))
    files_template = parser.get('CONFIG', 'FILES_TEMPLATE')

    if method == "T":
        del_file_timestamp(base_dir, files_template, keep, simulation_mode, recursive_mode)
    elif method == "C":
        del_file_creation(base_dir, files_template, keep, simulation_mode, recursive_mode)


if __name__ == "__main__":
    main()

