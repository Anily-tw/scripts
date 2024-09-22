#!/bin/bash
for fifo in $ANILY_DDRACE_ROOT/servers/*.fifo; do
  echo $1 > "$fifo"
done