# This is a sample Python script.
from turtle import title

import value as value
from pyspark.shell import sc
from pyspark.sql.functions import when, split


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('This is just a beginning :)')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# Pyspark Introduction

# import pyspark
# from pyspark.sql import SparkSession
# from pyspark.sql.types import StructType, StructField, StringType, IntegerType
# from pyspark.sql.types import ArrayType, DoubleType, BooleanType
# from pyspark.sql.functions import col, array_contains
#
# spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
#
# df = spark.read.option("header", True).csv("./zipcodes.csv")
#
# df.printSchema()
#
import pyspark
from pyspark.sql import SparkSession

# spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

#
# fileRDD = sc.wholeTextFiles("./Files")
#
# rdd = fileRDD.collect()
#
# columns = ["Platform","Page","View Rank"]
# df = spark.createDataFrame(data=rdd, schema = columns)
# df.show()
# # rdd.show()
# # print Data
# for row in rdd: {
#
#     print(row)
# }


# spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
# data = [("James","Smith","USA","CA"),
#     ("Michael","Rose","USA","NY"),
#     ("Robert","Williams","USA","CA"),
#     ("Maria","Jones","USA","FL")
#   ]
# columns = ["firstname","lastname","country","state"]
# df = spark.createDataFrame(data = data, schema = columns)
# # df.show(truncate=False)
#
# df.select("firstname",when(df.firstname == 'Michael', 1).otherwise(0)).show(10)
#
# dataframe = df.withColumn('new_column', pyspark.F.lit('This is a new column'))
# dataframe.show(2)


spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
# spark is from the previous example


# A text dataset is pointed to by path.
# The path can be either a single text file or a directory of text files
path = "./pageviews.txt"

df = spark.read.text(path)
# df.show(3)
# df.selectExpr("split(value, ' ') as\
# (deneme,Text_Data_In_Rows_Using_Text)").show(4,False)

split_col = pyspark.sql.functions.split(df['value'], ' ')
df3 = df.select(split_col.getItem(0).alias('platform'), split_col.getItem(1).alias('page_title'),
                split_col.getItem(2).alias('views'))
# df3.show(truncate=False)
rowList = df3.collect()

columns = ["page_title", "views"]

vals = [('Sirene', 3)]

search_df = spark.createDataFrame(vals, columns)

def findviews(search, df3,search_df):
    df4 = df3.filter(df3["page_title"] == search)
    df4.show(50)

    row_list = df4.collect()
    # print(type(row_list[1].__getitem__('views')))
    print(len(row_list))



    # Summing number of views
    view = 0

    for x in range(0, len(row_list)):
        view += int(row_list[x].__getitem__('views'))

    print("Total view of '", search, "'\n")
    print(view)

    # Saving search results to dataframe

    newRow = spark.createDataFrame([(search, view)], columns)
    search_df = search_df.union(newRow)
    search_df.show()
    return search_df


    # Other Part search algorithms

    # df3.select("page_title", when(df3.page_title == 'Barack_Obama', 1).otherwise(0))
    #
    # df3.select("page_title", df3.page_title.like("Barack_Obama"))

    # dataframe_txt.select(when(dataframe_txt == 'By Lewis Carol')).show(10)


# name = 'Siren'
# findviews(name,df3,search_df)
# df6 = search_df.filter(search_df["page_title"] == name)
# df6.show(6)
# print(len(df6.collect()))
# if len(df6.collect())>0:
#     print("found it")


for x in range(0, len(rowList)):
    name = str(rowList[x].__getitem__('page_title'))
    print(name)

    df6 = search_df.filter(search_df["page_title"] == name)

    if len(df6.collect()) == 0:
        print("Searching views for:")
        print(name, "\n")
        search_df = findviews(name, df3, search_df)
    # df6 = search_df.filter(df3["page_title"] == 'Sirene')
    # print(name)
    # len(df6)
    # if name != '':
    #     print("Searching")
    #     print(name)
    #     findviews(name,df3,search_df)
    # name = ''








