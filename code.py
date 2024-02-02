# initial setup importing libraries and data source
import pandas as pd # working with data set
import matplotlib.pyplot as plt # graphs

# reading data and storing it in a DataFrame object
df = pd.read_csv('survey_results_public.csv')
# Retrieving first 5 rows in dataframe
df.head(5)

df = df.drop_duplicates()

df = df.drop([
    'ResponseId',  # Unique identifier, not relevant for analysis
    'Q120',        # Internal metadata, likely not relevant
    'SOAccount',   # Whether they have a Stack Overflow account or not is not directly relevant
    'SOComm',      # Community belonging is less relevant to technology and workflow
    'TBranch',    # Participation in Professional Developer Series
    'ICorPM',     # Individual Contributor or People Manager status
    'TimeSearching', 'TimeAnswering', # Time spent searching/answering questions
    'SurveyLength', 'SurveyEase', # Feedback on survey length and ease
    'OfficeStackAsyncHaveWorkedWith', 'OfficeStackAsyncWantToWorkWith', 'OfficeStackSyncHaveWorkedWith' # office tools
], axis=1)

print(df.columns.values.tolist())

# Aggregate the data
country_counts = df['Country'].value_counts()

# Sort and select the top 5
top_5_countries = country_counts.head(5)

# Bar Chart Visualisation
plt.figure(figsize=(10, 6))
top_5_countries.plot(kind='bar')
plt.title('Top 5 Countries with Most Survey Participants')
plt.xlabel('Country')
plt.ylabel('Number of Participants')
plt.xticks(rotation=45)
plt.show()

# Identify the top 5 countries
top_5_countries = df['Country'].value_counts().head(5).index

# Filter the dataset to include only the top 5 countries
filtered_data = df[df['Country'].isin(top_5_countries)]

# Process the data to count the number of technologies used per respondent
def count_tech_per_respondent(row):
    return len(str(row).split(';'))

# Columns to analyze
tech_columns = ['LanguageHaveWorkedWith', 'DatabaseHaveWorkedWith', 'PlatformHaveWorkedWith', 'WebframeHaveWorkedWith']

# Creating a DataFrame to hold the counts
tech_counts = pd.DataFrame()

for col in tech_columns:
    col_count = filtered_data[col].apply(count_tech_per_respondent)
    tech_counts[col] = col_count

# Adding country for grouping
tech_counts['Country'] = filtered_data['Country']

# Plotting
plt.figure(figsize=(12, 8))

# Box plot for each technology category
for i, col in enumerate(tech_columns, 1):
    plt.subplot(2, 2, i)
    boxplot_data = tech_counts.groupby('Country')[col].apply(list)
    plt.boxplot(boxplot_data, labels=boxplot_data.index)
    plt.title(f'Distribution of {col}')
    plt.xticks(rotation=45)
    plt.ylabel('Count of Technologies Used')

plt.subplots_adjust(hspace=2)
plt.show()


# Filter the DataFrame for the United Kingdom and the specified age range
uk_young_devs = df[(df['Country'] == 'United Kingdom of Great Britain and Northern Ireland') & 
(df['Age'].isin(['18-24 years old', 'Under 18 years old']))]

# Function to count the frequency of each language
def count_languages(series):
    # Split the string by semicolon and return the exploded list to count each language separately
    return series.str.cat(sep=';').split(';')

# Count the languages for 'LanguageHaveWorkedWith' and 'LanguageWantToWorkWith'
languages_have_worked = count_languages(uk_young_devs['LanguageHaveWorkedWith'])
languages_want_to_work = count_languages(uk_young_devs['LanguageWantToWorkWith'])

# Count the frequency of each language
languages_have_worked_freq = pd.Series(languages_have_worked).value_counts()
languages_want_to_work_freq = pd.Series(languages_want_to_work).value_counts()

# Combine the frequencies into a single DataFrame
combined_freq = pd.DataFrame({
    'HaveWorkedWith': languages_have_worked_freq,
    'WantToWorkWith': languages_want_to_work_freq
})

# Sort by 'HaveWorkedWith' frequency for the line graph
combined_freq = combined_freq.sort_values(by='HaveWorkedWith', ascending=False)

# Plot the line graph
plt.figure(figsize=(15, 5))
plt.plot(combined_freq['HaveWorkedWith'], marker='o', label='Have Worked With')
plt.plot(combined_freq['WantToWorkWith'], marker='x', label='Want To Work With')
plt.title('Most Popular Languages Have Worked With & Want To Work With (UK, Age 18-24 or under 18)')
plt.xlabel('Programming Languages')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.show()

# Function to split the semi-colon separated list and count each unique category
def count_semi_colon_separated_values(df, column):
    return df[column].str.cat(sep=';').split(';')

# Create lists of all the learning methods from the semi-colon separated fields
learn_code_all = count_semi_colon_separated_values(df, 'LearnCode')
learn_code_online_all = count_semi_colon_separated_values(df, 'LearnCodeOnline')
learn_code_courses_cert_all = count_semi_colon_separated_values(df, 'LearnCodeCoursesCert')

# Count the occurrences of each learning method
learn_code_freq = pd.Series(learn_code_all).value_counts()
learn_code_online_freq = pd.Series(learn_code_online_all).value_counts()
learn_code_courses_cert_freq = pd.Series(learn_code_courses_cert_all).value_counts()

# Plotting histograms for learning methods
plt.figure(figsize=(14, 6))

plt.subplot(1, 3, 1)
learn_code_freq.plot(kind='bar')
plt.title('LearnCode Methods')
plt.xlabel('Method')
plt.ylabel('Frequency')
plt.xticks(rotation=90)

plt.subplot(1, 3, 2)
learn_code_online_freq.plot(kind='bar')
plt.title('LearnCodeOnline Resources')
plt.xlabel('Resource')
plt.xticks(rotation=90)

plt.subplot(1, 3, 3)
learn_code_courses_cert_freq.plot(kind='bar')
plt.title('LearnCodeCoursesCert Platforms')
plt.xlabel('Platform')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()
