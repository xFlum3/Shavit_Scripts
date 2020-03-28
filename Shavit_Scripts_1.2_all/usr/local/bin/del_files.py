#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
   delFiles - Delete log files(support several deletion method)

   Version: 1.0 (2020-03-28)
   Dev: Shavit Ilan (ilan.shavit@gmail.com)
"""

import logging
import glob
from datetime import date
import os
import json


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
                    log_msg = log_message + " - Deleted!"
                    logging.info(log_msg)
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
                        log_msg = log_message + " - Deleted!"
                        logging.info(log_msg)
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
        read del_file.ini and call func to delete the files
        - SIMULATION_MODE: Y (Simulation mode) \ N (Delete the files)
        - RECURSIVE MODE: Y (Scan directory RECURSIVELY) \ N (Dont scan RECURSIVELY)
        - METHOD: T (depends on timestamp signature in the file name) \ C (depends on file creation time)
        - BASE_DIR = C:\PATH\TO\FILES (Windows) \ /PATH/TO/FILES (Linux)
        - FILES_TEMPLATE = file_*.zip (look for files starting with 'file', ending with 'zip')
        - KEEP = 5 How many files to keep (Last 5 FILES or 5 DAYS)
    """
    if os.name == 'posix':
        ini_file = "/etc/del_files.ini"
    elif os.name == 'nt':
        home_dir = os.environ['HOME']
        ini_file = home_dir + "/del_files.ini"
    else:
        print "Error: Unsupported platform"
        exit()
    try:
        with open(ini_file, "r") as ini_file:
            json_content = json.load(ini_file)
    except:
        print "Missing or illegal config file in /etc/del_files.ini"
        exit()

    for each_config in json_content:
        log_file = each_config["LOG_FILE"]
        logging.basicConfig(filename=log_file, level=logging.INFO,\
            format='%(asctime)s - %(levelname)s - %(message)s')
        simulation_mode = each_config['SIMULATION_MODE']
        base_dir = each_config['BASE_DIR']
        recursive_mode = each_config['RECURSIVE_MODE']
        method = each_config['METHOD']
        keep = int(each_config['KEEP'])
        files_template = each_config['FILES_TEMPLATE']

        if method == "T":
            del_file_timestamp(base_dir, files_template, keep, simulation_mode, recursive_mode)
        elif method == "C":
            del_file_creation(base_dir, files_template, keep, simulation_mode, recursive_mode)


if __name__ == "__main__":
    main()
