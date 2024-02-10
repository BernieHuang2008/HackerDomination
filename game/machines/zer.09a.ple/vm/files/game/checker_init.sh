origin_hash=$(sudo grep root /etc/shadow)
echo "$origin_hash" > /game/origin_hash.dat
