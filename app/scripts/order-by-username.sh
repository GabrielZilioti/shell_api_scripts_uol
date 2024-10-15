#!/bin/bash

if [ "$2" == "-desc" ]; then
  awk '{print $1, $2, $3, $4, $5}' "$1" | sort -k1,1r
else
  awk '{print $1, $2, $3, $4, $5}' "$1" | sort -k1,1
fi
