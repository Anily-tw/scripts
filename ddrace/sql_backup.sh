#!/bin/bash
mysqldump --defaults-extra-file=~/.my.cnf teeworlds --result-file=$ANILY_DDRACE_ROOT/backups/backup-$(date +\%F).sql
