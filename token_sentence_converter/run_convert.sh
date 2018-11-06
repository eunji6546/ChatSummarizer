#!/bin/bash

for ((i=2;i<21;i++))
do
	python Tok-sen.py < ../sample_data/chat$i.txt > ../sample_data/converted/chat$i.txt 
done
 
