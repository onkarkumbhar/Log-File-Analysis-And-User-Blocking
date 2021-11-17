#!/bin/bash
rm blacklist_tokens_login.txt
rm blacklist_tokens_server.txt
touch blacklist_tokens_login.txt
touch blacklist_tokens_server.txt

python3 mapreduce_login.py log/login.data>>blacklist_tokens_login.txt
python3 mapreduce_server.py log/server.data>>blacklist_tokens_server.txt

rm log/login.data
rm log/server.data
touch log/login.data
touch log/server.data