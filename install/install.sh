#!/bin/bash

rm -r /tmp/borg
mkdir /tmp/borg
cp -r /opt/borg/* /tmp/borg/

rm -r /tmp/borg/.git
rm -r /tmp/borg/.server
rm -r /tmp/borg/.client
rm -r /tmp/borg/data
rm -r /tmp/borg/database

mkdir /tmp/borg/.server
mkdir /tmp/borg/.client
mkdir /tmp/borg/data
mkdir /tmp/borg/database

# máquina de testes
scp -rp /tmp/borg/* debian@54.37.137.117:/opt/borg/


