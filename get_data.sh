#!/bin/sh

# create data folder
mkdir data

# move in
cd data

# manifest
URL_MANIFEST=https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/manifest.txt

# content
URL_CONTENT=https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/

# get manifest file
wget $URL_MANIFEST

# get content
wget -B $URL_CONTENT -i manifest.txt

# remove sample file
rm sample-S2-records.gz

# return back
cd -