# German Bank Budget manager
A script for processing german bank export files.

## Why

To monitor how much money we spend in different areas of life. 


## What 

While living in Germany it is important to get a budget overview at the end of the month. 
This script can read custom CSVs and map them to a (custom) unified format. 
With minimal effort it can generate uniform CSV files to get a nice overview of the monthly budget. 


# How 

String matching using the [fuzzy wuzzy](https://github.com/seatgeek/fuzzywuzzy) library allows for rules application. 

The configuration files are yaml files and there is one example included. 
Should be expanded with the user's special needs (restaurant or supermarket names).
