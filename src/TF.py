from pyspark.sql import SparkSession
from pyspark import SQLContext

import pyspark.sql.functions as F 


spark = SparkSession.builder.\
    master('yarn').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)

# enables cartesian join
spark.conf.set("spark.sql.crossJoin.enabled", "true")

df = sqlContext.read.format('parquet').load('hdfs:/scholar_data/tokens_count_by_year.parquet')

# keep only tokens starting from 3 characters in length
df = df.filter('LENGTH(entities) > 2')

# gather column names linked to years
col_years = [col_name for col_name in df.columns]
col_years.remove('entities')

# Find peak usage of token across the years
# https://stackoverflow.com/questions/40874657/pyspark-compute-row-maximum-of-the-subset-of-columns-and-add-to-an-exisiting-da
minf = F.lit(float("-inf"))
df = df.withColumn("year_max", F.greatest(*[F.coalesce(F.col(year), minf) for year in col_years]))

# forget about tokens that have never been really used
df = df.filter("year_max > 10").drop('year_max')

# find total number of "valid" tokens used on each year
df = df.join(df.groupby().sum(*col_years))

# retrieve token frequency (times common coefficient) for each year
# coefficient is to make sure we do not limitations of float precision too hard
for year in col_years:
    df = df.withColumn(year, 100000.0*F.col(year) / F.col(f'sum({year})')).drop(f'sum({year})')

# store results 
df.write.save('hdfs:/scholar_data/tokens_freq_by_year.parquet', format='parquet', mode='overwrite')

spark.stop()
