---
title: "Lesson 6: pandas"
type: lecture
program: applied-data-analysis
course: Python
status: draft
created: 2026-11-08
updated: 2026-11-08
---
# Lesson 6: pandas

[Python](python.md) · [Lesson 5](lesson-05-numpy.md)

## Context and evidence

The owner supplied the Lesson 6 notebook on 2026-11-08.
The author, lecture date, and original notebook URL are unknown.
Notebook metadata reports Python 3.9.7. Metadata does not verify the active runtime.
The notebook has no practice tasks or recall questions.
The agent checked the additions below with pandas 2.3.3 on local Python 3.9.6 on 2026-11-08.
The checks used the Titanic CSV file from the URL in the notebook, with 891 rows and 12 columns.
The vault does not retain the notebook, the data file, original text, or images.

Main reference: [pandas documentation](https://pandas.pydata.org/docs/).

## Data analysis steps

The source gives this usual sequence:

1. Load the data and examine it.
2. Change or extend the data if necessary.
3. Do exploratory data analysis (EDA): calculations and charts.
4. Clean the data.
5. Make statistical or other models.

A dataset is a table of data. The target is the column with the variable to predict. Features are the other columns.

## Series and DataFrame

| Property | `Series` | `DataFrame` |
| --- | --- | --- |
| Dimensions | 1 | 2 |
| Labels | One index | Row index and column names |
| NumPy equivalent | Vector | Matrix |
| Example | One column | Full table |

```python
data = pd.read_csv("train.csv")
ages = data["Age"]                     # Series
part = data[["Sex", "Age", "Fare"]]    # DataFrame
one = data[["Age"]]                    # DataFrame with one column
```

Agent addition: `ages[5]` finds the label 5, not the position 5. After a sort, these are different rows.

## Inspect a table

| Name | Kind | Result |
| --- | --- | --- |
| `head(n)`, `tail(n)`, `sample(n)` | Method | First, last, or random rows |
| `info()` | Method | Column types and counts of values that are not missing |
| `describe()` | Method | Statistics for numeric columns |
| `describe(include=["object"])` | Method | Statistics for text columns |
| `shape`, `columns`, `values` | Attribute | Size, column names, NumPy array |
| `sum`, `min`, `max`, `mean`, `median`, `count` | Method | Aggregation |
| `unique()`, `nunique()` | Method | Unique values, number of unique values |
| `value_counts(normalize=True)` | Method | Part of the total for each value |
| `sort_values(cols, ascending=...)` | Method | Sorted table |

An attribute has no parentheses. A method has parentheses.

## Missing values

`NaN` marks a missing value. An arithmetic operation with `NaN` gives `NaN`. A comparison with `NaN` gives `False`.

| Method | Result |
| --- | --- |
| `isna()`, `isnull()` | `True` where a value is missing |
| `dropna()` | Removes rows with a missing value |
| `fillna(value)` | Replaces missing values |
| `mean()`, `median()` | Ignore `NaN` by default. `skipna=False` gives `NaN` |
| `count()`, `nunique()` | Do not count `NaN` |
| `unique()` | Includes `NaN` |

In this data, `Age` has 177 missing values, `Cabin` has 687, and `Embarked` has 2.

## Select rows and columns

| Tool | Selects by | End of a slice |
| --- | --- | --- |
| `data["col"]` | Column name | |
| `.loc[rows, cols]` | Labels | Included |
| `.iloc[rows, cols]` | Positions | Excluded |

Agent check: `data.loc[:4]` gives 5 rows. `data.iloc[:4]` gives 4 rows.

### Filter

```python
data[(data["Pclass"] == 3) & (data["Sex"] == "male")]   # 347 rows
```

Use `&`, the vertical bar operator, and `~` for "and", "or", and "not".
The source recommends parentheses around each condition. Agent check: they are necessary, because `&` has a higher priority than `==`.
Without them, this example causes `TypeError`. The word `and` causes `ValueError`.

## Change a table

| Purpose | Code |
| --- | --- |
| Rename columns | `data.rename(columns={"Age": "Years"})` |
| Remove columns | `data.drop(["a", "b"], axis=1)` |
| Add a column | `data["sum"] = data["a"] + data["b"]` |
| Apply a function | `data["Age"].apply(f)`, or `data.apply(f, axis=1)` for rows |
| Remove duplicates | `data.drop_duplicates()`, or with a list of columns |
| Group | `data.groupby("Sex")["Age"].mean()` |
| Index to a column | `result.reset_index()` |
| Save | `data.to_csv("f.csv", index=False)`, `data.to_excel("f.xlsx", index=False)` |

Most of these methods return a new object. Assign the result, or use `inplace=True` where the method permits it.

Agent additions:

- Use an operation on full columns when you can. `data.apply` on rows was about 70 times slower than `+` in one measurement here.
- `to_excel` needs the `openpyxl` package. Without it, the call causes `ModuleNotFoundError`.

## Source corrections

| Source example | Correction or limit |
| --- | --- |
| `data_sorted.loc[0]` is called the first row | It is the row with label 0, Braund. The first row of the sorted table is `iloc[0]`, Thomas |
| Text says that `iloc` makes the slice in `data.loc[:4, ...]` | The code uses `loc`, and its end is included |
| `isna()` is described as a mask of values that are not empty | It is the opposite: `True` marks missing values |
| `ages.fillna(-1) > 60` | `fillna` is not necessary. `ages > 60` gives the same 22 rows |
| `ages.median()` has the comment "mean age" | The median is not the mean |
| `tmp = data[[...]]`, then `tmp["Age"] = ...` | This causes `SettingWithCopyWarning`. Use `data[[...]].copy()` |
| "Method 2" for elderly survivors | Method 1 gives a count, 5. Method 2 gives a part of the total, 0.227 |
| Class survival rates are printed as "mean ticket price" | The values 0.63, 0.47, and 0.24 are survival rates |
| `data["col"].fillna(value, inplace=True)` | This causes `FutureWarning`. It will not operate in pandas 3.0. Use `data["col"] = data["col"].fillna(value)` |
| `data[????]` and `np.nan` before `import numpy` | These cells do not run in a fresh execution |

### Duplicates that are not duplicates

The source removes `PassengerId`, `Ticket`, and `Name`, and then removes 107 "duplicates".
Agent check: the original table has 0 duplicate rows. These 107 rows are different passengers with the same remaining values.
The removal changes the results:

| Value | Original data | After removal |
| --- | --- | --- |
| Survival rate | 0.384 | 0.412 |
| Mean age of women | 27.916 | 27.946 |
| Mean age of men | 30.727 | 31.036 |

Thus the `groupby` result in the source (27.98 and 30.64) is not equal to the earlier filter result (27.92 and 30.73).
The source calls these the same calculation. The data changed between them, also because of the median fill.
Do a duplicate check before you remove identifier columns.

### Fill with the mode

The source fills `Cabin` with its most frequent value. In the original data, 77% of `Cabin` is missing, and that value occurs 4 times.
After the fill, one cabin has 78% of all passengers. This is not a correct description of the data.
A separate "unknown" value or a column that marks missing values keeps this information.

## Owner attempts

On 2026-11-08 the owner reported one solved LeetCode problem.
The time is owner-reported. The LeetCode test results were not shown to the agent.

- [Big Countries](https://leetcode.com/problems/big-countries/): solved in 11:06.01.
  The solution filters rows with two conditions in parentheses and the vertical bar operator. It then selects three columns.

Agent check, 2026-11-08: the agent ran the solution on a small table made by the agent, with values at both limits. The results were correct.
Agent comment: `world.area` operates here, but this form fails when a column name is the same as a `DataFrame` attribute. For a column named `size`, `d.size` gives the table size and `d["size"]` gives the column.
A local variable with the name of its function operates here, but a different name is clearer.

The owner then wrote a second version in 03:01.60 (owner-reported), with named conditions and square brackets.
Agent check: this version has an error. It uses `>` but the task says "at least", which is `>=`. A country with an area of exactly 3,000,000 or a population of exactly 25,000,000 is not in the result.

## Recall questions

1. What is the difference between `data["Age"]` and `data[["Age"]]`?
2. What is the difference between an attribute and a method?
3. What does `isna()` give for a missing value?
4. What does `mean()` do with `NaN`?
5. What is the difference between `loc` and `iloc`?
6. How many rows does `data.loc[:4]` give?
7. Why are parentheses necessary in a filter with `&`?
8. Why can you not use `and` in a filter?
9. What is `axis=1` in `drop`?
10. Why can a duplicate check give an incorrect result after you remove identifier columns?
11. Why is the mode a bad fill value for a column with 77% missing values?

Open questions: official course title, lecture date, and required runtime.
