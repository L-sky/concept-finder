from pyspark.sql import SparkSession
from pyspark import SQLContext

import pyspark.sql.functions as F 


spark = SparkSession.builder.\
    master('yarn').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)

df = sqlContext.read.format('parquet').load('hdfs:/scholar_data/base.parquet').\
    select('year', 'entities').\
    filter("year < 2019").\
    withColumn('entities', F.explode('entities'))

df = df.withColumn('entities', F.lower(F.col('entities')))
df = df.withColumn('entities', F.regexp_replace(F.col('entities'), '(\d)[, ](\d{3})', '$1$2'))
df = df.withColumn('entities', F.explode(F.split('entities', '[,]')))
df = df.withColumn('entities', F.trim(F.col('entities')))
df = df.withColumn('entities', F.regexp_replace(F.col('entities'), '_', ' '))
df = df.withColumn('entities', F.regexp_replace(F.col('entities'), '\s+', ' '))

df = df.filter(~(F.col('entities').rlike('[^\w\s]'))).\
    groupby('entities').\
    pivot('year').\
    count().\
    sort('entities')

df.write.save('hdfs:/scholar_data/tokens_count_by_year.parquet', format='parquet', mode='overwrite')

spark.stop()
