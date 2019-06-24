#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import atexit
import argparse
import sys
import time
import ssl
from pyVmomi import vim, vmodl
from pyVim.task import WaitForTask
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi
import argparse
import getpass
reload(sys)
sys.setdefaultencoding('utf8')
__author__='Gitrajit-singh.takhelmayum@amadeus.com'
__version__=1.0

import logging
logFormatter = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s' ,datefmt='%a %d %b %Y %H:%M:%S', )
log = logging.getLogger()
log.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)

def get_args():
    parser = argparse.ArgumentParser(description='A utility to Generate / Remove snapshot which are older than <any> hours. ')
    parser._action_groups.pop()  # Edited this line
    required = parser.add_argument_group('Required Arguments')
    optional = parser.add_argument_group('Optional Arguments')
    required.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='Vcenter Name [**Note:- Multiple Vcenter accepted separated by COMMA(,)]')
    required.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='User name to connect to Vcenter.')

    optional.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to connect to Vcenter.')

    required.add_argument('-o', '--operation',
                        required=True,
                        action='store',
                        choices=['remove', 'list_all'],
                        help='Operation to perform remove/list_all .')
    required.add_argument('-t', '--hours',
                        type=int,
                        required=True,
                        action='store',
                        default=0,
                        help='Number of hours.')

    args = parser.parse_args()
    input1 = dict()
    if args.password is None:
        prom_txt = 'Enter password for User %s : ' % (args.user)
        passwrd = getpass.getpass(prompt=prom_txt)
        input1['vcenter_password'] = passwrd
    else:
        input1['vcenter_password'] = args.password


    vcenterhost=args.host.split(",")
    input1['vcenter_ip'] = vcenterhost
    input1['vcenter_user'] = args.user
    input1['operation'] = args.operation
    input1['hour'] = args.hours
    input1['ignore_ssl'] = 'True'

    return input1


def list_snapshots_recursively(snapshots):
    from datetime import timedelta, datetime
    snapshot_data = []
    snap_text = ""
    for snapshot in snapshots:
        #print snapshot

        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        date1 = datetime.now()
        date2 = snapshot.createTime.strftime('%Y-%m-%d %H:%M:%S.%f')
        #print snapshot
        diff = datetime.strptime(str(date1), datetimeFormat) \
               - datetime.strptime(str(date2), datetimeFormat)

        if diff.total_seconds()/3600 > inputs.get('hour', 0):

            snap_text = "%s; %s; %s; %s " % (snapshot.name, snapshot.createTime,int(diff.total_seconds()/3600), snapshot.description)
            snapshot_data.append(snap_text)
        snapshot_data = snapshot_data + list_snapshots_recursively(snapshot.childSnapshotList)
            #print snapshot

    #print snapshot_data
    return snapshot_data

def get_snapshot(snapshots):
    from datetime import timedelta, datetime
    snapshot_data = []
    snap_text = ""
    for snapshot in snapshots:
        #print snapshot

        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        date1 = datetime.now()
        date2 = snapshot.createTime.strftime('%Y-%m-%d %H:%M:%S.%f')
        diff = datetime.strptime(str(date1), datetimeFormat) \
               - datetime.strptime(str(date2), datetimeFormat)

        if diff.total_seconds()/3600 > inputs.get('hour', 0):
            #snap_text = "Name: %s; CreateTime: %s; Description: %s " % (snapshot.name, snapshot.createTime, snapshot.description)
            snapshot_data.append(snapshot.snapshot)
            #print snapshot.snapshot
        snapshot_data = snapshot_data + get_snapshot(snapshot.childSnapshotList)

    #print snapshot_data
    return snapshot_data

def create_html(data,hrd):
    try:
        import os
        from jinja2 import Environment, FileSystemLoader
        from datetime import datetime
        now = datetime.now()
        now1 = now.strftime('%Y-%m-%d')
        root = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(root, 'templates')
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template('s.html')
        filename = os.path.join(root, 'Snapshot_report' + now1 +'.html')
        with open(filename, 'w') as fh:
            fh.write(template.render(data=data,hrd=hrd))

        return True
    except Exception as e:
        return e

def main():

    si = None
    global inputs
    inputs = get_args()
    log.info("Trying to connect to VCENTER SERVER . . .")
    context = None
    operation = inputs['operation']
    log.info("Operation selected : " + operation)
    if operation == 'list_all':
        global final_obj
        final_obj = list()
        try:
            for vc in inputs['vcenter_ip']:

                if inputs['ignore_ssl'] and hasattr(ssl, "_create_unverified_context"):
                    context = ssl._create_unverified_context()
                si = connect.Connect(vc, 443, inputs['vcenter_user'], inputs['vcenter_password'], sslContext=context)
                atexit.register(Disconnect, si)
                log.info("Connected to VCENTER SERVER : " + vc)
                log.info("Searching for snapshot . . .")
                content = si.RetrieveContent()
                container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
                for c in container.view:

                    if c.snapshot != None:
                        obj = list_snapshots_recursively(c.snapshot.rootSnapshotList)

                        for i in obj:
                            final_obj.append(vc + ";" + c.name + ";" + i)

                log.info("Snapshot data collected")
            print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("| %-40s| %-25s| %-50s| %-40s| %-10s| %-40s" % ('Vcenter Name', 'VM Name', 'SnapshotName', 'Created Time', 'Hours', 'Description'))
            print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            for line in final_obj:
                val1 = line.split(';')[0].strip()
                val2 = line.split(';')[1].strip()
                val3 = line.split(';')[2].strip()
                val4 = line.split(';')[3].strip()
                val5 = line.split(';')[4].strip()
                val6 = line.split(';')[5].strip()

                print("| %-40s| %-25s| %-50s| %-40s| %-10s | %-40s" % (val1, val2, val3, val4, val5, val6))
            print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            hrd = inputs['hour']

            out = create_html(final_obj, hrd)
            if out == True:
                log.info("Html file created!!!")
            else:
                log.info("Error while Creating html :" + str(out))
        except Exception as e:
            log.error(e)


    elif operation == 'remove':

        try:

            for vc in inputs['vcenter_ip']:
                if inputs['ignore_ssl'] and hasattr(ssl, "_create_unverified_context"):
                    context = ssl._create_unverified_context()
                si = connect.Connect(vc, 443, inputs['vcenter_user'], inputs['vcenter_password'], sslContext=context)
                atexit.register(Disconnect, si)
                log.info("Connected to VCENTER SERVER : " + vc)
                log.info("Searching for snapshot . . .")
                content = si.RetrieveContent()
                container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
                for c in container.view:
                    if c.snapshot != None:
                        ob = get_snapshot(c.snapshot.rootSnapshotList)
                        for i in ob:
                            WaitForTask(i.RemoveSnapshot_Task(False))
                            log.info("Deleted snapshot for Vcenter: %s , VM name: %s" % (vc, c.name))
        except Exception as e:
            log.error(e)
    else:

        log.error("Specify operation in "
                  "remove/list_all")


# Start program
if __name__ == "__main__":
    main()