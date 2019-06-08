from pyspark.sql import SparkSession

spark = SparkSession.builder.\
    master('local[2]').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext

gzfile = './data/*.gz'
sc_file = sc.textFile(gzfile)

data = spark.read\
    .option('compression', 'gzip')\
    .json(gzfile)\
    .select('id', 'title', 'year', 'entities', 'paperAbstract')\
    .write.save('./data/orc', format='orc', mode='append')

spark.stop()
