#!/bin/bash

origin_hash="root:\$6\$Z4.wjAeraoZ2KfVJ\$yVkNLGRjUVSFD1qQoEYqrSbj4mWjWueZfjqaqcunLzSh2R4pq1Z2yA9rHHwZnotNlH2kYGRt7XUQGic3SZbVD1:19755:0:99999:7:::"
now_hash=$(sudo grep root /etc/shadow)

if [ "$origin_hash" != "$now_hash" ]; then
    echo "passed"
else
    echo "failed"
    exit 1
fi
