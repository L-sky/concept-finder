from rake_nltk import Rake

from pyspark.sql import SparkSession
from pyspark import SQLContext
from pyspark.sql.types import ArrayType, StructType, StructField, FloatType, StringType
from pyspark.sql.functions import udf


spark = SparkSession.builder.\
    master('local[2]').\
    appName('scholar').\
    getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)


data = sqlContext.read.format('orc').load('./data/orc')

rake_schema = ArrayType(StructType([
    StructField('score', FloatType()),
    StructField('concept', StringType())
]), containsNull=True)

"""
class RakeWrapper:
    def __init__(self):
        self.r = Rake()

    def apply_rake(self, text):
        self.r.extract_keywords_from_text(text)
        return self.r.get_ranked_phrases_with_scores()


rake = RakeWrapper()
spark_rake = udf(lambda text: rake.apply_rake(text), rake_schema)
"""


def apply_rake(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases_with_scores()


spark_rake = udf(lambda text: apply_rake(text), rake_schema)

res = data.filter('paperAbstract!=\'\'').select('id', 'title', 'year', 'entities', spark_rake('paperAbstract').alias('candidateConcepts'))
print(res.count())

res.write.save('./data/candidates', format='orc', mode='append')


spark.stop()
