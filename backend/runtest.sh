#! /usr/bin/sh
dropdb -h 172.23.240.1 -U root trivia_test
createdb -h 172.23.240.1 -U root trivia_test
psql -h 172.23.240.1 -U root trivia_test < trivia.psql
python3 test_flaskr.py