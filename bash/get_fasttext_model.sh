#!/bin/sh

# create model folder
mkdir fasttext

# move in
cd fasttext

# model archive
URL_MODEL=https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip

# get model archive
wget $URL_MODEL

# extract only model file
unzip crawl-300d-2M-subword.zip crawl-300d-2M-subword.bin

# clean up 
rm crawl-300d-2M-subword.zip

# return back
cd -
