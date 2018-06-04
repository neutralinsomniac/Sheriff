#! /bin/sh

username=$1
ssh-keygen -b 2048 -t rsa -f "./"$username"_id_rsa" -q -N ''
