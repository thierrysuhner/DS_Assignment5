#!/bin/bash

set -e

NODES=(node1 node2 node3 node4 node5)

echo "=== Reconnecting all nodes ==="
for node in "${NODES[@]}"; do
  echo "Flushing iptables in $node..."
  docker exec "$node" iptables -F || true
done

echo "Network fully reconnected."
