#!/bin/bash

origin_hash=$(sudo cat /game/origin_hash.dat)
now_hash=$(sudo grep root /etc/shadow)

if [ "$origin_hash" != "$now_hash" ]; then
    echo "passed"
else
    echo "failed"
    exit 1
fi
