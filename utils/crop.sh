#!/bin/bash
ffmpeg -i "$1" -filter:v "crop=1920:1080" -y $(dirname "$1")/$2.png
