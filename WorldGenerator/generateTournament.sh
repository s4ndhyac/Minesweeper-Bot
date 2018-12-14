#!/bin/bash

cd Problems

rm -rf Beginner
rm -rf Intermediate
rm -rf Expert

mkdir Beginner
mkdir Intermediate
mkdir Expert
cd ..
 
python3 WorldGenerator.py 1000 Beginner_world_ 8 8 10

python3 WorldGenerator.py 1000 Intermediate_world_ 16 16 40

python3 WorldGenerator.py 1000 Expert_world_ 16 30 99

echo Finished generating worlds!
