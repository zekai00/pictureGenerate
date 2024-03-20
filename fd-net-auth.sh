#!/bin/bash

URL="https://10.250.3.66/include/auth_action.php"
read -p "enter your username[20110240007]:" username
read -p "enter your password:" password

if [ -z "$username" ]; then
	username=20110240007
fi
ip=10.177.58.143
echo "\n"
curl $URL --insecure --data "action=login&username=$username&password=$password&ac_id=1&user_ip=$ip&nas_ip=&user_mac=&save_me=1&ajax=1" #> /dev/null 2>&1
echo "\n"
