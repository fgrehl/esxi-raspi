# esxi-raspi
Demo Scripts for the Native GPIO Driver for ESXi-Arm on Raspberry Pi.

Driver: https://github.com/thebel1/thpimon/tree/main/build/vib

Driver installation: https://www.virten.net/2020/11/get-raspberry-pi-cpu-temperature-on-esxi-arm/

See also: https://www.virten.net/2020/11/raspberry-pi-running-esxi-arm-send-cpu-temperature-to-graphite/


## pimon_temp.py
Print the current temperature.

```
# python ./pimon_temp.py
Polling CPU temperature every 10 seconds...
CPU Temperature: 48.0 C

# python ./pimon_temp.py 2
Polling CPU temperature every 2 seconds...
CPU Temperature: 47.0 C
CPU Temperature: 48.0 C

```


## pimon_tempGraphite.py
Send the temperature to Graphite. Configure CARBONSERVER, CARBONPORT and INTERVAL.

```
# python ./pimon_tempGraphite.py
servers.esx9-virten-lab.cputemp 48.0 1604949554
servers.esx9-virten-lab.cputemp 49.0 1604949564
servers.esx9-virten-lab.cputemp 47.0 1604949574
```



## hostd-operation.cgi
Python Script to pull data from external hosts using the hostdCgiServer. Make the script executable and link it to `/usr/lib/vmware/hostd/cgi-bin/`

```
# chmod +x /vmfs/volumes/[datastore]/pyUtil/hostd-operation.cgi
# ln -s '/vmfs/volumes/[datastore]/pyUtil/hostd-operation.cgi' /usr/lib/vmware/hostd/cgi-bin/hostd-operation.cgi
# ln -s '/vmfs/volumes/[datastore]/pyUtil/pimonLib/' /usr/lib/vmware/hostd/cgi-bin/pimonLib
```

To make the configuration persistent across reboots, add this to your `/etc/rc.local.d/local.sh` before `exit 0`

```
# ln -s '/vmfs/volumes/[datastore]/pyUtil/hostd-operation.cgi' /usr/lib/vmware/hostd/cgi-bin/hostd-operation.cgi
# ln -s '/vmfs/volumes/[datastore]/pyUtil/pimonLib/' /usr/lib/vmware/hostd/cgi-bin/pimonLib
```

You can then pull data using curl or a browser: https://[ESXi-URL]/cgi-bin/hostd-operation.cgi?getTemp
