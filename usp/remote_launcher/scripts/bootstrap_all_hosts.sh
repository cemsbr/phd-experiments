#!/bin/bash
for i in $(seq 0 $1); do
    VM="hadoop$i" make bootstrap-vm &
done
