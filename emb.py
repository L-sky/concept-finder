from pyspark.sql import SparkSession
from pyspark import SQLContext

import pyspark.sql.functions as F 
import pyspark.sql.types as T

import os
import fasttext
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

dirpath = os.getcwd()
model_bin_path = f'{dirpath}/fasttext/crawl-300d-2M-subword.bin'
emb_length = 300

spark = SparkSession.builder.\
    master('local[2]').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)

df = sqlContext.read.format('parquet').load('hdfs:/scholar_data/tokens_freq_by_year.parquet')
pd_df = df.select('entities').toPandas()
spark.stop()


model = fasttext.load_model(model_bin_path)
pd_df['embeddings'] = pd_df['entities'].apply(model.__getitem__)
del model

emb_components = pd.DataFrame(pd_df['embeddings'].tolist(), columns=[f'v{i}' for i in range(emb_length)])
pd_df = pd.concat([pd_df['entities'], emb_components[:]], axis=1) 

pa_df = pa.Table.from_pandas(pd_df)

fs = pa.hdfs.connect()
#fs = pa.hdfs.connect(host='localhost', port=9000)

with fs.open('hdfs:/scholar_data/token_embeddings.parquet', 'wb') as target:
    pq.write_table(pa_df, target)

"""
schema = T.StructType([T.StructField(f'v{i}', T.FloatType(), False) for i in range(emb_length)])
emb_udf = F.udf(lambda x: model[x], schema)
df = df.select('entities', emb_udf('entities').alias('embedding')).select('entities', 'embedding.*')
df.write.save('hdfs:/scholar_data/token_embeddings.parquet', format='parquet', mode='overwrite')
"""



