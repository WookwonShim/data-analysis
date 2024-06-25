from google.colab import drive
import pandas as pd
import numpy as np

## DATA PREPROCESSING
# DATA LOADING
    # 2018-central-park-squirrel-census-squirrel-data.csv
    # 2018-central-park-squirrel-census-hectare-data.csv (not yet complete)
# DATA TYPE REVIEW AND CONVERSION
# ORDERING AND RENAMING COLUMNS

## DATA PREPROCESSING ----------------------------------------------------------------------------------------------------------------

# DATA LOADING
# Mount Google Drive
drive.mount('/content/drive')
# Load Data from Google Drive
squirrel = pd.read_csv('/content/drive/My Drive/Colab Notebooks/data/2018-central-park-squirrel-census-squirrel-data.csv')

# Check .info() 
print(squirrel.info())
'''
Initial Notes
- the shape is (3023, 31).
- update the field names.
'''

#
print(squirrel.sample(n=5, random_state=28).T)
'''
Initial Notes (continued)
- the date type is %m%d%Y (e.g., 10142018).
- the observations are made over a period. How many observers?
- possibility of a squirrel counted more than once? 
- the unique id is a combination of other field values.
- change data types from object to category.
- 
'''

# DATA TYPE REVIEW AND CONVERSION ----------------------------------------------------------------------------------------------------

squirrel['Date'] = pd.to_datetime(squirrel['Date'], format='%m%d%Y') # Convert the date from %m%d%Y to pd.datetime.

squirrel['Hectare'].nunique() #339/3023 unique values
squirrel['Hectare'] = squirrel['Hectare'].astype('category') # Convert object to category.

squirrel['Shift'].unique() # AM or PM
squirrel['Shift'] = squirrel['Shift'].astype('category') # Convert object to category.

squirrel['Hectare Squirrel Number'].max() # max value 23
squirrel['Hectare Squirrel Number'].min() # min value 1
squirrel['Hectare Squirrel Number'] = squirrel['Hectare Squirrel Number'].astype('int8') # Convert int64 to int8.

squirrel['Age']unique() # [nan, 'Adult', 'Juvenile', '?']
squirrel['Age'] = squirrel['Age'].astype('category') # Convert object to category.
squirrel['Age'] = squirrel['Age'].replace('?', np.nan) # treat ? as a missing value, NaN

squirrel['Primary Fur Color'].unique() # [nan, 'Gray', 'Cinnamon', 'Black']
squirrel['Primary Fur Color'] = squirrel['Primary Fur Color'].astype('category') # Convert object to category.

squirrel['Highlight Fur Color'].unique() # has multiple categories. e.g., 'Gray', 'Cinnamon, White', 'Gray, White'
# Split the multiple categories into a list of categories
squirrel['Highlight Fur Color'] = squirrel['Highlight Fur Color'].str.split(', ')
# Handle NaN values by filling them with an empty list
squirrel['Highlight Fur Color'] = squirrel['Highlight Fur Color'].apply(lambda x: x if isinstance(x, list) else [])
# Explode the list to get each category in its own row
exploded = squirrel.explode('Highlight Fur Color')
# Create dummy variables for each unique category
dummies = pd.get_dummies(exploded['Highlight Fur Color'], prefix='highlight_color')
# Group by the original index and sum to collapse back into the original rows
dummies = dummies.groupby(exploded.index).sum()
# Combine the original DataFrame with the dummies DataFrame
squirrel = pd.concat([squirrel, dummies], axis=1)

squirrel['Location'].unique() # [nan, 'Above Ground', 'Ground Plane']
squirrel['Location'] = squirrel['Location'].astype('category') # Convert object to category.

#
print(squirrel.info())


# ORDERING AND RENAMING COLUMNS -----------------------------------------------------------------------------------------------------
# Renaming columns in the DataFrame
renamed_columns = {
    'Unique Squirrel ID': 'unique_squirrel_id',
    'Hectare': 'hectare',
    'Hectare Squirrel Number': 'hectare_squirrel_number',
    'X': 'x',
    'Y': 'y',
    'Lat/Long': 'lat_long',
    'Date': 'date',
    'Shift': 'shift',
    'Age': 'age',
    'Primary Fur Color': 'primary_fur_color',
    'Highlight Fur Color': 'highlight_fur_color',
    'Combination of Primary and Highlight Color': 'combination_fur_color',
    'Color notes': 'color_notes',
    'Running': 'running',
    'Chasing': 'chasing',
    'Climbing': 'climbing',
    'Eating': 'eating',
    'Foraging': 'foraging',
    'Other Activities': 'other_activities',
    'Kuks': 'kuks',
    'Quaas': 'quaas',
    'Moans': 'moans',
    'Tail flags': 'tail_flags',
    'Tail twitches': 'tail_twitches',
    'Approaches': 'approaches',
    'Indifferent': 'indifferent',
    'Runs from': 'runs_from',
    'Other Interactions': 'other_interactions',
    'Location': 'location',
    'Above Ground Sighter Measurement': 'above_ground_sighter_measurement',
    'Specific Location': 'specific_location'
}

# Identification Columns
id_cols = [
    'unique_squirrel_id', 'hectare', 'hectare_squirrel_number'
]

# Location Columns
loc_cols = [
    'x', 'y', 'lat_long'
]

# Time Columns
time_cols = [
    'date', 'shift'
]

# Physical Characteristics
physical_char_cols = [
    'age', 'primary_fur_color', 'highlight_fur_color',
    'combination_fur_color', 'color_notes'
]

# Behavior Columns
behavior_cols = [
    'running', 'chasing', 'climbing', 'eating',
    'foraging', 'other_activities', 'kuks', 'quaas',
    'moans', 'tail_flags', 'tail_twitches', 'approaches',
    'indifferent', 'runs_from', 'other_interactions'
]

# Additional Location Details
other_loc_cols = [
    'location', 'above_ground_sighter_measurement', 'specific_location'
]

# Combined Ordered Columns
ordered_columns = (
    id_cols
    + loc_cols
    + time_cols
    + physical_char_cols
    + behavior_cols
    + other_loc_cols
)

# Applying the renaming and ordering to the DataFrame
squirrel = squirrel.rename(columns=renamed_columns)[ordered_columns]
