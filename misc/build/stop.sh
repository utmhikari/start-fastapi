#!/usr/bin/env bash

# grep your tag~
ps aux | grep -i start-fastapi | awk '{print $2}' | xargs sudo kill -9
