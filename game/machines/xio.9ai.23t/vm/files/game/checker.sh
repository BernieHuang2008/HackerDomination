#!/bin/bash

target_hash="04b273e6a0ffbd9533198c6a0958beef4367b8ce46515f2b62a9dd707bac1220"
now_hash=$(sudo sha256sum -b /home/webserver/www/mission/secret.sec | awk '{print $1}')

if [ "$target_hash" == "$now_hash" ]; then
    echo "passed"
else    echo "failed"
    exit 1
fi
