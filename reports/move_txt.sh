#!/bin/bash

source_d="/home/andsec/Documents/program/andsec_program/console_logs/"

destination_d1="/home/andsec/Documents/program/andsec_program/reports/"

inotifywait -m -q -e close_write "$source_d" |

while read -r path action file; do
  if [ -d "$path$file" ]; then
    cp -r -- "$path$file" "$destination_d1$file"
  else
    cp -- "$path$file" "$destination_d1$file"
  fi
  rm -r -- "$path$file"  # Remove the source file or directory
done