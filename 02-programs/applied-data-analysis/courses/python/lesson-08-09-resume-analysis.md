---
title: "Lessons 8 and 9: resume data analysis project"
type: lecture
program: applied-data-analysis
course: Python
status: draft
created: 2026-11-08
updated: 2026-11-08
---
# Lessons 8 and 9: resume data analysis project

[Python](python.md) · [Lesson 6](lesson-06-pandas.md)

## Context and evidence

The owner supplied the notebook `Лекция_8_9.ipynb` on 2026-11-08. Its title gives Lesson 8.
The author, lecture date, and original notebook URL are unknown.
Lesson 7 was not supplied. The vault has no note for it.
Notebook metadata reports Python 3.9.7. Metadata does not verify the active runtime.
The notebook has a full solved project. It does not identify the author of the solution.

The project uses resumes from hh.ru: 44,744 rows and 12 columns. It also uses a table of exchange rates.
The stored outputs contain records about real people.
The vault does not retain these records, the notebook, the data links, original text, or images.
Examples below use agent-made values.

The agent did not download the resume data. Numbers below are stored source outputs.
The agent checked the logic with small agent-made tables, pandas 2.3.3, and local Python 3.9.6 on 2026-11-08.

## Project steps

1. Examine the structure: `head`, `shape`, `info`, `describe`, and the range of dates.
2. Change the data: make numeric and category features from text.
3. Do exploratory data analysis with charts.
4. Clean the data: duplicates, missing values, and outliers.

## Change text to features

The source uses `apply` with a function for each column. Check the result with `unique()`, `value_counts()`, or `isnull().sum()`.

| New feature | Method in the source | Trap |
| --- | --- | --- |
| Education (4 categories) | Substring check | Capital letters: `Высшее` does not match in `Неоконченное высшее` |
| Sex and age | `split` and a search for the words `год`, `года`, `лет` | The result must be `int`, or a histogram treats the values as text |
| Experience in months | Years × 12 + months, in the first 6 words | Some rows have only years or only months. `Не указано` is a hidden missing value |
| City (4 categories) | First part before the comma, then a list of large cities | The other parts can contain cities too |
| Ready to move | `False` for the two negative forms, else `True` | `'готов к переезду'` is also a substring of the negative form |
| Ready for business trips | The same, and `False` if the text is missing | Long city lists cut off the end of some rows |
| Employment and schedule | A `bool` column for each category | See the corrections |
| Salary in rubles | Amount × rate ÷ proportion, after a left merge with rates | See the corrections |

The proportion is the number of currency units for one rate. A rate of 17.197 for 100 KZT gives 0.17197 rubles for 1 KZT.

## Charts

| Purpose | Chart | Code |
| --- | --- | --- |
| Distribution of one feature | Histogram and box plot | `px.histogram(df, x=col, marginal="box")` |
| Median by category | Bar chart | `groupby` and `px.bar` |
| Distribution by category | Box plot | `px.box(df, x=cat, y=col)` |
| Two categories | Grouped bar chart | `px.bar(..., barmode="group")` |
| Two features and a value | Pivot table and heatmap | `pivot_table` and `px.imshow` |
| Two numeric features | Scatter plot | `sns.scatterplot`, `sns.regplot` |

Stored medians of desired salary, for salaries below 1,000,000 rubles:

| Education | Median |
| --- | --- |
| Higher | 60,000 |
| Incomplete higher | 50,000 |
| Secondary | 40,000 |
| Secondary vocational | 40,000 |

| Business trips | Move | Median |
| --- | --- | --- |
| No | No | 40,000 |
| No | Yes | 50,000 |
| Yes | No | 60,000 |
| Yes | Yes | 70,000 |

These results come before the corrections below. Foreign-currency salaries in them can be incorrect.

## Clean the data

| Step | Code | Stored result |
| --- | --- | --- |
| Full duplicates | `data.drop_duplicates()` | 153 rows removed |
| Missing workplace or position | `dropna(subset=[...])` | Rows removed |
| Missing experience | `fillna(median)` | Mean is 114 months |
| Salary above 1,000,000 or below 1,000 rubles | `data.drop(outliers.index)` | 435 rows removed |
| Experience not less than age | The same | 7 rows removed |

## Source corrections

### Two errors in the salary calculation

Agent check: these two errors change the main result of the project.
The agent did not calculate their size, because it did not download the data.

**Error 1: the merge finds almost no rates.**
Step 1 of the source algorithm says to take the date only. The code for this is commented out.
Thus `Обновление резюме` keeps its time, for example `13:21`, and the rate table has `00:00`. The merge keys do not agree.
Then `fillna(1)` gives a rate of 1 to all rows with no match, not only to rubles.

With an agent-made table, 550 USD at 13:21 became 550 rubles. The same row at 00:00 became 36,025 rubles.
Such a salary is then below 1,000 and is removed as an outlier. Thus the outlier count of 435 can also be incorrect.

```python
data["date"] = data["Обновление резюме"].dt.normalize()
merged = data.merge(rates, left_on=["cur", "date"], right_on=["currency", "date"], how="left")
```

After this change, set the rate to 1 only where the currency is `RUB`. Then a row with a missing rate stays visible.

**Error 2: months and days change places in the rate table.**
The file has the format `dd/mm/yy`, but `pd.to_datetime(rates["date"])` has no format.
The stored warning says that pandas parsed each value separately.

| Text | Without a format | With `format="%d/%m/%y"` |
| --- | --- | --- |
| `29/12/17` | 2017-12-29 | 2017-12-29 |
| `01/02/18` | 2018-01-02 | 2018-02-01 |
| `12/11/19` | 2019-12-11 | 2019-11-12 |

The source text says that the rates end on 05.12.2019, but the stored maximum is 2019-12-11. This agrees with the error.
Treat a warning from a date parser as an error. Always specify the format.

### Other corrections

| Source example | Correction or limit |
| --- | --- |
| Employment and schedule columns are called One Hot Encoding | One row can have several `True` values. One-hot encoding has exactly one. This is multi-label encoding |
| `apply(lambda x: x.split(",")).sum()` | `sum` on lists joins them, and this is slow for many rows. Use `str.split(", ").explode().unique()` |
| A `zip` loop over employment and schedule lists | It operates only because both lists have 5 items. Use two loops, or `str.get_dummies(sep=", ")` |
| `arg is np.nan` | `float("nan") is np.nan` gives `False`. Use `pd.isna(arg)` |
| `get_salary_сurrency` | The `с` in this name is a Cyrillic letter. A call with a Latin `c` causes `NameError` |
| `fill_value=0` in the pivot table | An empty group looks like a salary of 0 on the heatmap. Keep `NaN` |
| The conclusion says that ages 16 and 17 have high values for higher education | The stored table has 1,900 and 10,000. The high value, 60,000, is at age 14 |
| The conclusion gives experience "from 57 to 154 years", and calls it age | The unit is months |
| "Most" applicants are in the box of the box plot | The box has the middle 50% of the values |
| Questions about salary and experience refer to anomalies in age | Copy error |
| Different medians "clearly influence" salary, or readiness "strongly increases" it | These results show an association, not a cause. Position and city can have an effect on both |
| The age anomalies, 14 and 100 years | The notebook finds them, but no cleaning step removes them |
| The text lists 3 columns with missing values | The stored output lists 4 |
| Cell with only `pandas, matplotlib, seaborn, plotly` | It causes `NameError` in a fresh execution |

Also, `min` and `max` on dates as text give an incorrect range: `31.10.2018` is more than `01.02.2019`.
The source shows this error and then corrects it with `pd.to_datetime`.

## Recall questions

1. Why does `max` on text dates give an incorrect result?
2. What is a hidden missing value? Give an example from this project.
3. Why must a merge key have the same form in both tables?
4. Why is `fillna(1)` on all rate rows dangerous?
5. Why specify `format` in `pd.to_datetime`?
6. What is the difference between one-hot and multi-label encoding?
7. Why is `fill_value=0` a bad choice for a heatmap of medians?
8. What does the box of a box plot show?
9. Why do different medians not prove a cause?
10. Why can a conversion error make an outlier count incorrect?

Open questions: official course title, lecture dates, the content of Lesson 7, and the size of the two salary errors.
