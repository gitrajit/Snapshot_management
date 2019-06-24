# Snapshot_management
To display and delete all the snapshot which are older than &lt;any> hours at vcenter level

# Description:
A utility to Generate / Remove snapshot which are older than ANY hours at Vcenter level.
This is created by using Python SDK of Vmware (PyVmomi).

## Steps to execute.

* git clone
* cd snapshot
* Virtualenv Venv
* source Venv/bin/activate
* pip install -r requirements
* python snapshot_Management.py -s vcenter1,vcenter2,.. -u username -o <list_all/remove> -t 72 [-p <password> optional]

```
(Venv)[pgtakhel@gitrajit snapshot]$ python snapshot_Management.py --help
usage: snapshot_Management.py [-h] -s HOST -u USER [-p PASSWORD] -o
                              {remove,list_all} -t HOURS

A utility to Generate / Remove snapshot which are older than <any> hours.

Required Arguments:
  -s HOST, --host HOST  Vcenter Name [**Note:- Multiple Vcenter accepted
                        separated by COMMA(,)]
  -u USER, --user USER  User name to connect to Vcenter.
  -o {remove,list_all}, --operation {remove,list_all}
                        Operation to perform remove/list_all .
  -t HOURS, --hours HOURS
                        Number of hours.

Optional Arguments:
  -p PASSWORD, --password PASSWORD
                        Password to connect to Vcenter.




(Venv)[pgtakhel@gitrajit snapshot]$ python snapshot_Management.py -s Vcenter1.net,Vcenter2.net -u abcdef@vsphere.local -o list_all -t 1000
Enter password for User abcdef@vsphere.local : 
Thu 20 Jun 2019 11:44:08 root INFO     Trying to connect to VCENTER SERVER . . .
Thu 20 Jun 2019 11:44:08 root INFO     Operation selected : list_all
Thu 20 Jun 2019 11:44:08 root INFO     Connected to VCENTER SERVER : Vcenter1.vclassic.net
Thu 20 Jun 2019 11:44:08 root INFO     Searching for snapshot . . .
Thu 20 Jun 2019 11:44:08 root INFO     Snapshot data collected
Thu 20 Jun 2019 11:44:08 root INFO     Connected to VCENTER SERVER : Vcenter2.vclassic.net
Thu 20 Jun 2019 11:44:08 root INFO     Searching for snapshot . . .
Thu 20 Jun 2019 11:44:09 root INFO     Snapshot data collected

Thu 20 Jun 2019 11:44:09 root INFO     html file created
(Venv)[pgtakhel@gitrajit snapshot]$


```
