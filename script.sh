#!/bin/bash


count=0
while true;
do
	stdbuf -oL echo "hello ${count}"
	sleep 1
	((count++))

	if [[ count -eq 11  ]];then
		break
	fi
done

exit 0
