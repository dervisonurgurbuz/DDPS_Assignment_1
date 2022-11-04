import pyspark
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, split
from pyspark.sql import SparkSession

st = time.time()
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

# path = "./Files"

# Path for das5
path = "../../../../home/ddps2202/DDPS_Assignment_1/Files"

df = spark.read.text(path)

print("Total data row number")
print(len(df.collect()))

split_col = pyspark.sql.functions.split(df['value'], ' ')
df2 = df.select(split_col.getItem(0).alias('platform'), split_col.getItem(1).alias('page_title'),
                split_col.getItem(2).alias('views'))

rdd = df2.rdd
print("RDD partition count:" + str(rdd.getNumPartitions()))

# st = time.time()
# rdd4 = rdd.filter(lambda x: 'Sjabloon:Str_endswith' in x[1])
#
# et = time.time()
# data2 =rdd4.collect()
# view = 0
#
# for f in data2:
#     print(f[1]+ "  "+ f[2])
#     view += int(f[2])
#
# print("Total view is: ", view)

# Search dataframe

columns = ["page_title", "views"]

vals = [('Abruzze', 3)]

search_df = spark.createDataFrame(vals, columns)


# Scanning all pages for calculating total view per page
def findtotalviews(search, rdd, search_df):
    rdd4 = rdd.filter(lambda x: search in x[1])

    data2 = rdd4.collect()
    view = 0
    for f in data2:
        # print(f[1] + "  " + f[2])
        view += int(f[2])

    print("Total view of '", search, "= ", view, "'\n")

    # Saving search results to dataframe

    newRow = spark.createDataFrame([(search, view)], columns)
    search_df = search_df.union(newRow)

    return search_df


data = rdd.collect()

st2 = time.time()
# Main iteration function
for f in data:
    # print("Key:"+ str(f[1]) + "Value"+ str(f[2]) )
    name = str(f[1])
    df3 = search_df.filter(search_df["page_title"] == name)

    if len(df3.collect()) == 0:
        print("Searching views for:")
        print(name, "\n")
        search_df = findtotalviews(name, rdd, search_df)

search_df.show()
et = time.time()

compile_time = et - st
pageview_time = et - st2
print("Total compile time:", compile_time)
print("Pageview implementation time", pageview_time)
