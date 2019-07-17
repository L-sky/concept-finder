from pyspark.sql import SparkSession
from pyspark import SQLContext

import pyspark.sql.functions as F 

import numpy as np
import pandas as pd

import fasttext
import os

from pyspark.ml.feature import BucketedRandomProjectionLSHModel
from pyspark.ml.linalg import Vectors

neighbors_num = 20
dist_cutoff = 1

def format_np_array(x):
    return Vectors.dense(x/np.linalg.norm(x))

dirpath = os.getcwd()
model_bin_path = f'{dirpath}/fasttext/crawl-300d-2M-subword.bin'

spark = SparkSession.builder.\
    master('yarn').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)

print("Loading tokens space...")
df = sqlContext.read.format('parquet').load('hdfs:/scholar_data/token_normed_vector_embeddings.parquet').select('entities', 'normed_embeddings')

print("Loading TF space...")
TF = sqlContext.read.format('parquet').load('hdfs:/scholar_data/tokens_freq_by_year.parquet').select('entities', F.col('2018').alias('score'))

print("Loading fasttext model...")
ftmodel = fasttext.load_model(model_bin_path)

print("Loading LHS model...")
brpLSHmodel = BucketedRandomProjectionLSHModel.load('hdfs:/scholar_model/brpLSH_model')
print("Completed! You can start!")

token = ''
while token != 'stop':
    token = input()
    token = token.lower()
    if token == 'stop':
        break
    token_vector = format_np_array(ftmodel[token])

    search_result = brpLSHmodel.approxNearestNeighbors(df, token_vector, neighbors_num).select('entities', 'distCol').filter(f'distCol < {dist_cutoff}')
    search_result = search_result.join(TF, 'entities', how='left')
    search_result = search_result.select('entities', *[F.round(F.col(c), 3).alias(c) for c in ['distCol', 'score']])
    #search_result.orderBy('score', ascending=False).show()
    search_result_pd = search_result.orderBy('score', ascending=False).toPandas()

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(search_result_pd)

spark.stop()
