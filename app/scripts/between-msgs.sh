#!/bin/bash

awk -v min="$2" -v max="$3" '{if ($3+0 >= min && $3+0 <= max) print $1, $2, $3, $4, $5}' "$1"
