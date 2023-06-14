import pandas as pd
import json
import os
import datetime
import argparse

# Create argument parser
parser = argparse.ArgumentParser(description='Process some json data.')
parser.add_argument('file', type=str, help='The json file to process')

# Parse arguments
args = parser.parse_args()

# Get today's date
today = datetime.date.today()

# Create a base file name with today's date
base_filename = f"{today}_test_results.xlsx"

# Create a mapping from 'type_of_test' to its actual name
test_name_mapping = {
    1: 'Prestanda (GL)',
    4: 'SEO (GL)',
    5: 'Praxis (GL)',
    6: 'HTML',
    7: 'CSS',
    8: 'Webbapp (GL)',
    9: 'Standardfiler',
    10: 'Axe',
    15: 'Sitespeed',
    17: 'Frontend (YLT)',
    18: 'Pa11y',
    20: 'Webbkoll',
    21: 'HTTP & Tekniktest',
    22: 'Energi',
    23: 'Spårning och Integritet',
    24: 'E-post',
    25: 'Mjukvara'
}

# Load the JSON data into a pandas DataFrame
with open(args.file, 'r', encoding='utf-8') as file:
    test_results_dict = json.load(file)

test_results_df = pd.json_normalize(test_results_dict['tests'])

# Extract 'test_results' into a separate DataFrame
test_results_list = test_results_df['test_results'].apply(pd.Series).stack().reset_index(level=-1, drop=True)
test_results_expanded = pd.json_normalize(test_results_list)
test_results_expanded['site_id'] = test_results_list.index

# Map 'type_of_test' to its actual name
test_results_expanded['test_name'] = test_results_expanded['type_of_test'].map(test_name_mapping)

# Tests to include
tests_to_include = test_name_mapping.values()

# Loop through each of the new dataframes and clean the test report field
for test in tests_to_include:
    # Split the string into lines
    lines = test_results_expanded[f'report'].str.split('\r\n')
    # Filter out lines where the rating is 5.00
    cleaned_lines = lines.apply(lambda x: [line for line in x if '( 5.00 rating )' not in line])
    # Join the lines back together and assign back to the dataframe
    test_results_expanded['report'] = cleaned_lines.str.join('\r\n')

# Pivot the DataFrame to have a separate column for each test
rating_df = test_results_expanded.pivot(index='site_id', columns='test_name', values='rating')
report_df = test_results_expanded.pivot(index='site_id', columns='test_name', values='report')

# Merge the pivot table with the main dataframe to associate each site with its URL
merged_rating_df = pd.merge(test_results_df[['url']], rating_df, left_index=True, right_index=True)
merged_report_df = pd.merge(test_results_df[['url']], report_df, left_index=True, right_index=True)

# Merge ratings and reports DataFrames together
final_df = pd.DataFrame()

for column in merged_rating_df.columns:
    if column != 'url':
        final_df[column + '_rating'] = merged_rating_df[column]
        final_df[column + '_report'] = merged_report_df[column]
    else:
        final_df[column] = merged_rating_df[column]

# Check if the file already exists
version = 1
filename = base_filename
while os.path.exists(filename):
    # If the file exists, add a version number to the end of the file name
    version += 1
    filename = f"{today}_test_results_v{version}.xlsx"

# Save the results to the Excel file
final_df.to_excel(filename, index=False)
