```python
import pandas as pd
```

|             | Description                                                                                          | Command                                                             |
| ----------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Count       | **Count missing values**                                                                             | sf_permits.isnull().sum().sum()                                     |
| Count       | **Count all data points**                                                                            | np.product(sf_permits.shape)                                        |
| Drop        | **Drop all missing rows**<br>⚠ If only one cell has missing value, the entire ***row*** is dropped   | df.dropna(axis=0)                                                   |
| Drop        | Drop all missing columns<br>⚠ If only one cell has missing value, the entire ***column*** is dropped | df.dropna(axis=1)                                                   |
| Update      | Fill in the missing values using the next valid value                                                | `df.bfill()`                                                        |
| Show        | Show data type                                                                                       | `df['collumn'].dtype`                                               |
| Date parse  | Convert data type                                                                                    | `df['date_parsed'] = pd.to_datetime(df['date'], format="%m/%d/%y")` |
| Date parse  | Extract day of a date                                                                                | `day_of_month_landslides = landslides['date_parsed'].dt.day`        |
| Aggregation | Group and count diferent values of a series or dataframe                                             | `df.value_counts()`                                                 |
| Filtering   | Filter by condition and return df index                                                              | `indices = np.where([date_lengths == 24])[1]`                       |
| Update      | Set a value do a specific cell                                                                       | `df.loc[3378, "Date"] = "02/23/1975"`                               |
| Show        | Random sample of rows                                                                                | df.sample(5)                                                        |
| Aggregation | All the unique values, sorted alphabetically                                                         | `df['column'].unique().sort()`                                      |
| Transform   | Convert categorical variable into dummy/indicator variables.                                         | `df.get_dummies(df, drop_first=True)`                               |
| Show        | Print summary statistics                                                                             | `df["a_column"].describe()`                                         |
## Normalizing

| Description            | Command                                                                                                           |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Encode string to UTF-8 | str.encode("utf-8", errors="replace")                                                                             |
| Filtering              | matches = fuzzywuzzy.process.extract(string_to_match, strings, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio) |
|                        |                                                                                                                   |
