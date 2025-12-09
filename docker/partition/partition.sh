#!/bin/bash

set -e

GROUP1=($1)
GROUP2=($2)

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 \"group1_nodes\" \"group2_nodes\""
  echo "Example: $0 \"node1 node2 node3\" \"node4 node5\""
  exit 1
fi


get_ip() {
  docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$1"
}

echo "=== Partitioning network ==="
echo "Group 1: ${GROUP1[*]}"
echo "Group 2: ${GROUP2[*]}"

# Block traffic between groups
for n1 in "${GROUP1[@]}"; do
  iptables_exists=$(docker exec "$n1" which iptables 2>/dev/null || true)
  if [ -z "$iptables_exists" ]; then
    echo "Installing iptables in $n1 ..."
    docker exec "$n1" sh -c "apk add --no-cache iptables || apt-get update && apt-get install -y iptables"
  fi
  for n2 in "${GROUP2[@]}"; do
    IP2=$(get_ip "$n2")
    echo "Blocking $n1 -> $n2 ($IP2)"
    docker exec "$n1" iptables -A OUTPUT -d "$IP2" -j DROP || true
  done
done

for n2 in "${GROUP2[@]}"; do
  iptables_exists=$(docker exec "$n2" which iptables 2>/dev/null || true)
  if [ -z "$iptables_exists" ]; then
    echo "Installing iptables in $n2 ..."
    docker exec "$n2" sh -c "apk add --no-cache iptables || apt-get update && apt-get install -y iptables"
  fi
  for n1 in "${GROUP1[@]}"; do
    IP1=$(get_ip "$n1")
    echo "Blocking $n2 -> $n1 ($IP1)"
    docker exec "$n2" iptables -A OUTPUT -d "$IP1" -j DROP || true
  done
done

echo "The network partition has been created."
