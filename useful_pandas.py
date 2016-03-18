
'''
CONTENTS
Some of the code presented here is from bsweger/useful_pandas_snippets.py
I've augmented it to include useful snippets to read large csv files with iterators, 
working with timestamps, and working with web sessions.
'''

import pandas as pd


#load large csv file
reader = pd.read_csv(original_filename , iterator = True, chunksize = 10000)

# Filter records according to values in columns
# Set Captured time as index
list_of_dfs = [chunk[(chunk[col1]>a) & (chunk[col2]<b)] for chunk in reader]
df = pd.concat(list_of_dfs)

# drop a list of rows (say, [1,3])
df.drop(df.index[[1,3]])

#List unique values in a DataFrame column
pd.unique(df.column_name.ravel())

#Convert Series datatype to numeric, getting rid of any non-numeric values
df['col'] = df['col'].astype(str).convert_objects(convert_numeric=True)

#Grab DataFrame rows where column has certain values
valuelist = ['value1', 'value2', 'value3']
df = df[df.column.isin(value_list)]

#Grab DataFrame rows where column doesn't have certain values
valuelist = ['value1', 'value2', 'value3']
df = df[~df.column.isin(value_list)]

#Delete column from DataFrame
del df['column']

#Select from DataFrame using criteria from multiple columns
newdf = df[(df['column_one']>val1) & (df['column_two']==val2)]

#Rename several DataFrame columns
df = df.rename(columns = {
    'col1 old name':'col1 new name',
    'col2 old name':'col2 new name',
    'col3 old name':'col3 new name',
})

#lower-case all DataFrame column names
df.columns = map(str.lower, df.columns)

#even more fancy DataFrame column re-naming
#lower-case all DataFrame column names (for example)
df.rename(columns=lambda x: x.split('.')[-1], inplace=True)

#Loop through rows in a DataFrame
#(if you must)
for index, row in df.iterrows():
    print index, row['some column']  

#Lower-case everything in a DataFrame column
df.column_name = df.column_name.str.lower()

#Sort dataframe by multiple columns
df = df.sort(['col1','col2','col3'],ascending=[1,1,0])

#get top n for each group of columns in a sorted dataframe
#(make sure dataframe is sorted first)
top5 = df.groupby(['groupingcol1', 'groupingcol2']).head(5)

#Grab DataFrame rows where specific column is null/notnull
newdf = df[df['column'].isnull()]

#select from DataFrame using multiple keys of a hierarchical index
df.xs(('index level 1 value','index level 2 value'), level=('level 1','level 2'))

#Change all NaNs to None (useful before
#loading to a db)
df = df.where((pd.notnull(df)), None)

#Get quick count of rows in a DataFrame
len(df.index)

# Set a col of df as the index
df.set_index('id',inplace=True)

#Pivot data (with flexibility about what what
#becomes a column and what stays a row).
#Syntax works on Pandas >= .14
pd.pivot_table(
  df,values='cell_value',
  index=['col1', 'col2', 'col3'], #these stay as columns
  columns=['col4']) #data values in this column become their own column

#change data type of DataFrame column
df.column_name = df.column_name.astype(np.int64)

# Get rid of non-numeric values throughout a DataFrame:
for col in refunds.columns.values:
  refunds[col] = refunds[col].replace('[^0-9]+.-', '', regex=True)

#Set DataFrame column values based on other column values
df['column_to_change'][(df['column1'] == some_value) & (df['column2'] == some_other_value)] = new_value

# Remove row if one of the values is zero
df = df[(df != 0).all(1)]

#Clean up missing values in multiple DataFrame columns
df = df.fillna({
    'col1': 'missing',
    'col2': '99.999',
    'col3': '999',
    'col4': 'missing',
    'col5': 'missing',
    'col6': '99'
})

#Concatenate two DataFrame columns into a new, single column
#(useful when dealing with composite keys, for example)
df['newcol'] = df['col1'].map(str) + df['col2'].map(str)

#Doing calculations with DataFrame columns that have missing values
#In example below, swap in 0 for df['col1'] cells that contain null
df['new_col'] = np.where(pd.isnull(df['col1']),0,df['col1']) + df['col2']

# Split delimited values in a DataFrame column into two new columns
df['new_col1'], df['new_col2'] = zip(*df['original_col'].apply(lambda x: x.split(': ', 1)))


# Collapse hierarchical column indexes
df.columns = df.columns.get_level_values(0)

# one hot encode categorical variables
dfnew = pd.get_dummies(df, columns=[u'col1', u'col2', u'col3'])

#merge 2 dataframes
df_merged = pd.merge(
	left=df1, right=df2, 
	left_on='col1', right_on='col2')


'''
dates and timestamps
'''
# separate dates of form YYYY-MM-DD into 3 columns, YYYY, MM, DD
ux = [(int(u.date_account_created[i][0:4]),
       int(u.date_account_created[i][5:7]),
       int(u.date_account_created[i][8:10]))for i in range(len(u))]

u['year_account_created'] = [ux[i][0] for i in range(len(ux))]


# convert timestamps of form 20090319043255 into '2009-03-19 04:32:55'
x = u.timestamp
y = [str(i) for i in x.values]
ux = [y[i][0:4]+'-'+y[i][4:6]+'-'+y[i][6:8]+' '+y[i][8:10]+':'+y[i][10:12]+':'+y[i][12:14] for i in range(len(y))]

'''
web sessions

'''
# user_id	action	action_type	action_detail	device_type	secs_elapsed
# 0	d1mm9tcy42	lookup	NaN	NaN	Windows Desktop	319
# 1	d1mm9tcy42	search_results	click	view_search_results	Windows Desktop	67753
# 2	d1mm9tcy42	lookup	NaN	NaN	Windows Desktop	301
# 3	d1mm9tcy42	search_results	click	view_search_results	Windows Desktop	22141
# 4	d1mm9tcy42	lookup	NaN	NaN	Windows Desktop	435


def flatten_df(df,delimeter="_",suffix=""):
    df.columns = [suffix+delimeter.join(col).strip() for col in df.columns.values]
    return df


# Total secs spent by each user. Can expand by
# aggregate({'sec_sum':np.sum, 'sec_mean':np.mean}), etx
secs = df.groupby(['user_id'])['secs_elapsed'].aggregate({'sec_sum':np.sum},fill_value=0).reset_index()


# Create df with one row per user, and each column will be 
# sum_x, where x is an action type, and the value in the cell will be
# the sum of seconds for action type x for the user
action_detail_gp = flatten_df(pd.pivot_table(
	sessions1, 
	index = ['user_id'],
	columns = ['action_type'],
	values = 'secs_elapsed',
	aggfunc=[np.sum],
	fill_value=0).reset_index())


