# This is a sample Python script.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('This is just a beginning :)')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import time
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, split

# rdd = fileRDD.collect()
#
# columns = ["Platform","Page","View Rank"]
# df = spark.createDataFrame(data=rdd, schema = columns)
# df.show()
# rdd.show()
# print Data
# for row in rdd: {
#
#     print(row)
# }

st = time.time()

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
# spark is from the previous example

# A text dataset is pointed to by path.
# The path can be either a single text file or a directory of text files
path = "../../../../ddps2202/DDPS_Assignment_1/Files/pageviews2"
# df = sparkContext.wholeTextFiles(path)


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


# Part 1 Calculating total views
def findtotalviews(search, df3, search_df):
    df4 = df3.filter(df3["page_title"] == search)

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

    return search_df


# This function search pages that exactly matching given word
def exactmatch(search, df3):
    df7 = df3.select("page_title", when(df3.page_title == search, 1).otherwise(0))
    df7.show()
    # df4 = df3.filter(df3["page_title"] == search)
    # Other Part search algorithms

    # df3.select("page_title", when(df3.page_title == 'Barack_Obama', 1).otherwise(0))
    #
    # df3.select("page_title", df3.page_title.like("Barack_Obama"))

    # dataframe_txt.select(when(dataframe_txt == 'By Lewis Carol')).show(10)


def partiallymatch(search, df3):
    search = "%"+search+"%"
    df8 = df3.select("page_title", df3.page_title.like(search))
    df8.show()


# Part 1 Main Iterative Implementation
st2 = time.time()
for x in range(0, len(rowList)):
    name = str(rowList[x].__getitem__('page_title'))
    print(name)

    df6 = search_df.filter(search_df["page_title"] == name)

    if len(df6.collect()) == 0:
        print("Searching views for:")
        print(name, "\n")
        search_df = findtotalviews(name, df3, search_df)

search_df.show()

et1 = time.time()
# Part 2 Execution
print("Exactly Match")
exactmatch("Sirene", df3)
et2 = time.time()

# Part 3 Execution
print("Partially Match")
partiallymatch("Sjabloon", df3)
et3 = time.time()


total_compile_time = et3 - st
dataframe_compile_time = st-st2
part3_compile_time = et3-et2
part2_compile_time =  et2-et1
part1_compile_time = et1 - st2

print('Total Execution time:', total_compile_time, 'seconds')
print('Reading Dataframe Execution time:', total_compile_time, 'seconds')
print('Part1 Execution time', part1_compile_time, 'seconds')
print('Part2 Execution time', part2_compile_time, 'seconds')
print('Part3 Execution time', part3_compile_time, 'seconds')