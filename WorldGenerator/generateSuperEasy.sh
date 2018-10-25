#!/bin/bash

rm -rf Problems
mkdir Problems

python3 WorldGenerator.py 1000 Easy_world_ 5 5 1

echo Finished generating worlds!
