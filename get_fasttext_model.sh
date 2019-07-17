#!/bin/sh

# create model folder
mkdir fasttext

# move in
cd fasttext

# model archive
URL_MODEL=https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip

# get model archive
wget $URL_MANIFEST

# unzip
unzip crawl-300d-2M-subword.zip

# remove embeddings (.vec) and archive (.zip), keep only model (.bin) 
rm crawl-300d-2M-subword.vec
rm crawl-300d-2M-subword.zip

# return back
cd -
