#!/bin/bash

nohup /usr/lib/trino/bin/run-trino &

sleep 10

chmod +x /tmp/post-init.sh

trino < /tmp/post-init.sql

tail -f /dev/null