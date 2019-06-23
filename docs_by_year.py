from pyspark.sql import SparkSession
from pyspark import SQLContext
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import collect_list

from pyspark.ml.feature import CountVectorizer

spark = SparkSession.builder.\
    master('local[2]').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)


def keep_only_alpha_numeric(key_teerms):
    return [word for word in key_teerms if word.replace(' ', '').replace('-', '').isalnum()]


unpack_udf = udf(lambda l: [item for sublist in l for item in sublist], ArrayType((StringType()), containsNull=True))

spark_keep_alnum = udf(lambda entities: keep_only_alpha_numeric(entities), ArrayType((StringType()), containsNull=True))

cv = CountVectorizer(inputCol="alnum", outputCol="vectors")


res = sqlContext.read.format('orc').\
    load('./data/orc').\
    select('year', spark_keep_alnum('entities').alias('alnum')).\
    groupby('year').\
    agg(collect_list("alnum").alias("alnum")).\
    withColumn("alnum", unpack_udf("alnum"))


model = cv.fit(res)
model.transform(res).show()
