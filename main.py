import pandas as pd
import numpy as np
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Load airbnb_price.csv, prices
prices = pd.read_csv("airbnb_price.csv")

# Load airbnb_room_type.xlsx, xls
xls = pd.ExcelFile('airbnb_room_type.xlsx', engine='openpyxl')

# Parse the first sheet from xls, room_types
room_types = xls.parse(0)

# Load airbnb_last_review.tsv, reviews
reviews = pd.read_csv('airbnb_last_review.tsv', sep='\t')

# Print the first five rows of each DataFrame
print(prices.head(), "\n", room_types.head(), "\n", reviews.head())



# removing whitespace and getting rid of "dollars"
prices['price']= prices['price'].str.replace("dollars", "")

# Converting price column to numerical datatype
prices['price'] = pd.to_numeric(prices['price'])

# Printing descriptive statistics for the price column
print(prices['price'].describe())

free_listings = prices['price'] == 0

prices = prices.loc[~free_listings]

avg_price = round(prices['price'].mean(), 2)

print("The average price per night for an Airbnb listing in NYC is ${}.".format(avg_price))

prices_per_month = prices['price'] * 365/12

average_price_per_month = round(prices_per_month.mean(), 2)

print("airbnb monthly costs are ${}, while in the private market you would pay {}.".format(average_price_per_month, "$3,100.00"))
# set the room_type equal to y


# Convert the y column into lowercase
room_types["room_type"] = room_types["room_type"].str.lower()

# Update the y column to category data type
room_types["room_type"] = room_types["room_type"].astype("category")

# Create the variable room_frequencies
room_frequencies = room_types["room_type"].value_counts()

# Print the room_frequencies
print(room_frequencies)

# Set r equal to reviews["last_review"]


# Update r column to datetime data type
reviews["last_review"] = pd.to_datetime(reviews["last_review"])

# Create first_reviewed variable, the earliest review date
first_reviewed = reviews["last_review"].dt.date.min()

# Create last_reviewed variable, the latest review date
last_reviewed = reviews["last_review"].dt.date.max()

# Print first_reviewed and last_reviewed
print("The earliest Airbnb review is {}, the latest review is {}".format(first_reviewed, last_reviewed))

# Merge prices and room_types to create rooms_and_prices
rooms_and_prices = prices.merge(room_types, how="outer", on="listing_id")

# Merge rooms_and_prices with the reviews DataFrame to create airbnb_merged
airbnb_merged = rooms_and_prices.merge(reviews, how="outer", on="listing_id")

# Drop missing values from airbnb_merged
airbnb_merged.dropna(inplace=True)

num_dup = airbnb_merged.duplicated().sum()

# Check if there are any duplicate values
print("There are {} duplicates in the DataFrame.".format(num_dup))

# Extract information from the nbhood_full column and store as a new column, borough
airbnb_merged["borough"] = airbnb_merged["nbhood_full"].str.partition(",")[0]

# Group by borough and calculate summary statistics
boroughs = airbnb_merged.groupby("borough")["price"].agg(["sum", "mean", "median", "count"])

# Round boroughs to 2 decimal places, and sort by mean in descending order
boroughs = boroughs.round(2).sort_values("mean", ascending=False)

# Print boroughs
print(boroughs)

label_name = ["Budget", "Average", "Expansive", "Extravagant"]

Range = [0, 69, 175, 350, np.inf]

airbnb_merged["price_range"] = pd.cut(airbnb_merged["price"], bins=Range, labels=label_name)

prices_by_borough = airbnb_merged.groupby(["borough", "price_range"])["price_range"].count()

print(prices_by_borough)





