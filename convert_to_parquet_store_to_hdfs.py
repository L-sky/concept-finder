from pyspark.sql import SparkSession
import os
 
spark = SparkSession.builder.\
    master('local[2]').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext

dirpath = os.getcwd()
gzfile = f'file:///{dirpath}/data/*.gz'
sc_file = sc.textFile(gzfile)

df = spark.read.option('compression', 'gzip').json(gzfile)
df = df.select('id', 'title', 'year', 'entities', 'paperAbstract')
df.write.save('hdfs:/scholar_data/base.parquet', format='parquet')

spark.stop()
