from pyspark.sql import SparkSession
from pyspark import SQLContext

import pyspark.sql.functions as F 
import pyspark.sql.types as T
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.ml.feature import BucketedRandomProjectionLSH

import numpy as np

def make_normed_vector(x):
    x_np = np.array(x, dtype=np.float64)
    x_np = x_np / np.linalg.norm(x_np)
    return Vectors.dense(x_np)

    
spark = SparkSession.builder.\
    master('local[2]').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)


df = sqlContext.read.format('parquet').load('hdfs:/scholar_data/token_embeddings.parquet').select('entities', 'embeddings')

to_vector = F.udf(lambda x: Vectors.dense(x), VectorUDT())
to_normed_vector = F.udf(make_normed_vector, VectorUDT())

df = df.withColumn('normed_embeddings', to_normed_vector('embeddings'))
df = df.withColumn('embeddings', to_vector('embeddings'))

brpLSH = BucketedRandomProjectionLSH(inputCol="normed_embeddings", outputCol="hashes", seed=42, bucketLength=12.0, numHashTables=20)
brpLSHmodel = brpLSH.fit(df)

brpLSHmodel.save('hdfs:/scholar_model/brpLSH_model')
df.write.save('hdfs:/scholar_data/token_normed_vector_embeddings.parquet', format='parquet', mode='overwrite')

spark.stop()
