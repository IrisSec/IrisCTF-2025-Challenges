#!/bin/bash

echo "Copying data..."
cp -r /home/user/data /tmp/data

echo "Starting MySql..."
mysqld_safe --mysqlx=0 --socket=mysql.sock --datadir=/tmp/data &

while [[ $(grep "ready for connections" /var/log/mysql/error.log | wc -l) -ne 1 ]]
do
    echo "Waiting for MySql to start..."
    sleep 1
done

echo "MySql started."

echo "Running web app..."
cd /home/user && /home/user/app