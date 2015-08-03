from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.types import StructType, StructField, StringType, LongType, \
    BooleanType

if __name__ == '__main__':
    schema = StructType([
        StructField('_corrupt_record', StringType(), True),
        StructField('id', LongType(), True),
        StructField('ns', LongType(), True),
        StructField('redirect', BooleanType(), True),
        StructField('restrictions', StringType(), True),
        StructField('revision', StructType([
            StructField('comment', StringType(), True),
            StructField('contributor', StructType([
                StructField('id', LongType(), True),
                StructField('ip', StringType(), True),
                StructField('username', StringType(), True)
            ]), True),
            StructField('format', StringType(), True),
            StructField('id', LongType(), True),
            StructField('minor', BooleanType(), True),
            StructField('model', StringType(), True),
            StructField('parentid', LongType(), True),
            StructField('sha1', StringType(), True),
            StructField('text', StringType(), True),
            StructField('timestamp', LongType(), True)
        ]), True),
        StructField('title', StringType(), True)
    ])

    sc = SparkContext()
    sqlCtx = SQLContext(sc)

    wikiData = sqlCtx.jsonFile("hdfs://hadoop0:8020/enwiki.json",
                               schema=schema)
    wikiData.registerAsTable("wikiData")
    query = sqlCtx.sql("SELECT revision.contributor.username as user, "
                       "       COUNT(*) AS contribs "
                       "FROM wikiData "
                       "WHERE revision.contributor.username <> '' "
                       "GROUP BY revision.contributor.username "
                       "ORDER BY contribs DESC LIMIT 10")
    users = query.collect()

    for user in users:
        print("%s: %d" % user)

    sc.stop()
