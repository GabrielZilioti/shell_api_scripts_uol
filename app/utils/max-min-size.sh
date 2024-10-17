#!/bin/bash

if [ "$2" == "min" ]; then
  awk '{print $1, $2, $3, $4, $5}' "$1" | sort -k5,5n | head -n 1
else
  awk '{print $1, $2, $3, $4, $5}' "$1" | sort -k5,5nr | head -n 1
fi
