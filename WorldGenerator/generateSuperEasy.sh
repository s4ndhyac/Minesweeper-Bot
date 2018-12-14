#!/bin/bash

cd Problems
rm -rf Easy
mkdir Easy
cd ..
python3 WorldGenerator.py 1000 Easy_world_ 5 5 1

echo Finished generating worlds!
