#!/bin/bash


count=0


read -p "initial count :" count
while true;
do
	echo -en "hello ${count}\r"
	sleep 1
	
	((count++))
done
