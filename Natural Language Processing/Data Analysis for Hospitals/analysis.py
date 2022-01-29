import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 8)  # Output config

# Reading files
general = pd.read_csv('general.csv')
prenatal = pd.read_csv('prenatal.csv')
sports = pd.read_csv('sports.csv')

# Change columns names
columns = general.columns
prenatal.columns = columns
sports.columns = columns

# Concatenate tables
common_table = pd.concat([general, prenatal, sports], ignore_index=True)

# Delete unnamed column
common_table.drop(columns='Unnamed: 0', inplace=True)

# Delete empty rows
common_table.dropna(axis=0, how='all', inplace=True)

# Change gender column
common_table.replace({'gender': {'female': 'f', 'woman': 'f', 'man': 'm', 'male': 'm'}}, inplace=True)

# Change prenatal gender
common_table['gender'].fillna('f', inplace=True)

# Fill all NaN values with 0
common_table.fillna(0, inplace=True)

# Stage 4

# First question
# print(f'The answer to the 1st question is {common_table.hospital.value_counts().idxmax()}')
#
# # Second question
# stomach_in_general_count = common_table.loc[(common_table['hospital'] == 'general') &
#                                             (common_table['diagnosis'] == 'stomach')].shape[0]
# patients_in_general_count = common_table.loc[common_table['hospital'] == 'general'].shape[0]
# print(f'The answer to the 2nd question is {round(stomach_in_general_count / patients_in_general_count, 3)}')
#
# # Third question
# dislocation_in_sports_count = common_table.loc[(common_table['hospital'] == 'sports') &
#                                                (common_table['diagnosis'] == 'dislocation')].shape[0]
# patients_in_sports_count = common_table.loc[common_table['hospital'] == 'sports'].shape[0]
# print(f'The answer to the 3rd question is {round(dislocation_in_sports_count / patients_in_sports_count, 3)}')
#
# # Fourth question
# age_difference = common_table.loc[common_table['hospital'] == 'general']['age'].mean() - \
#     common_table.loc[common_table['hospital'] == 'sports']['age'].mean()
# print(f'The answer to the 4th question is {int(age_difference)}')
#
# # Fifth
# max_blood_test_hospital = common_table.groupby(['hospital'])['blood_test'].value_counts().idxmax()[0]
# max_value = common_table.groupby(['hospital'])['blood_test'].value_counts()[max_blood_test_hospital]['t']
# print(f'The answer to the 5th question is {max_blood_test_hospital}, {max_value} blood tests')

# Stage 5

# Sixth question
common_table.plot(y=['age'], kind='hist', bins=[1, 15, 35, 55, 70, 80])
print('The answer to the 1st question: 15-35')
plt.show()

# Seventh question
common_table['diagnosis'].value_counts().plot(kind='pie')
plt.show()
print('The answer to the 2nd question: pregnancy')

# Eighth question
sns.violinplot(y="height", x='hospital', data=common_table)
plt.show()
print('The answer to the 3rd question: It\'s because athletes are usually bigger.')
