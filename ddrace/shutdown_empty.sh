#!/bin/bash
for fifo in $ANILY_DDRACE_ROOT/servers/*.fifo; do
  echo "sv_shutdown_when_empty 1" > "$fifo"
done