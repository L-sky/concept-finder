from pyspark.sql import SparkSession
from pyspark import SQLContext


spark = SparkSession.builder.\
    master('local[2]').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)


def split_into_chars(entities):
    return [char for entity in entities for word in entity for char in word]


characters = sqlContext.read.format('orc').load('./data/orc').select('entities').rdd.flatMap(split_into_chars).distinct().collect()
print(characters)

