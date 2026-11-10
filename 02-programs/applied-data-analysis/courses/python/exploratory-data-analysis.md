---
title: Exploratory data analysis for homework
type: concept
program: applied-data-analysis
course: Python
status: draft
created: 2026-11-10
updated: 2026-11-10
---
# Exploratory data analysis for homework

[Python](python.md) · [Lesson 6](lesson-06-pandas.md) · [Lessons 8 and 9](lesson-08-09-resume-analysis.md)

## Meaning

Exploratory data analysis (EDA) is the first examination of a dataset with calculations and charts.
The homework uses EDA as a small study. Each task has code, its output, and a conclusion in words.
The course grades the conclusion equal to the code. Thus code without a conclusion is half of a task.

This note gives a general method. It does not contain homework answers.
Examples use an agent-made table with 12 rows.

## One cycle for each task

1. Read the question. Find the column and the result that the question asks for.
2. Write the code that gives this result.
3. Read the output. Find the number that answers the question.
4. Write the conclusion: fact, meaning, limit.

A conclusion pattern:

| Part | Content | Example |
| --- | --- | --- |
| Fact | A number from the output | "Members of the club have a mean of 67.5 points. Other students have 33.0." |
| Meaning | What the number tells about the question | "The difference is large: 34.5 points." |
| Limit | Why the result can be incorrect or incomplete | "Each group has only 5 or 6 students. This is an association, not a proved cause." |

A conclusion without a number is too general. A number without a meaning does not answer the question.

## Task types and tools

| Question | Code | What to read in the output |
| --- | --- | --- |
| How large is the table? | `df.shape` | Rows, columns |
| Which types and missing values? | `df.info()` | Type of each column, values that are not missing |
| Which range? | `df.describe()` | `min` and `max` outside the permitted scale are errors |
| Are rows repeated? | `df.duplicated().sum()` | 0 means no full duplicates |
| Is a column redundant? | `(df["a"] / df["b"]).unique()`, `df["a"].corr(df["b"])` | One ratio, or correlation 1 or −1 |
| Make categories from numbers | A function with `if`, then `apply` | `value_counts()` of the new column |
| Distribution of one column | `sns.histplot(df[col])`, `describe()` | Peaks, gaps, a long tail. Compare the mean and the median |
| Outliers | `df[col].sort_values(ascending=False).head()` | Compare the values with a real limit |
| Frequencies of categories | `value_counts()`, `sns.barplot` | The largest and the smallest categories |
| Binary feature and target | `sns.boxplot(data=df, x=bin, y=target)`, `groupby(bin)[target].agg(["count", "mean", "median"])` | Difference of medians, size of each group |
| Ordinal feature and target | `groupby(feature)[target].agg(["count", "mean"])`, `sns.barplot` | Direction of the means, groups with few rows |
| Clean | `df.loc[mask, col] = np.nan`, `df = df[~mask]` | `shape`, `min`, and `max` after each step |
| Save | `df.to_csv("name.csv", index=False)` | The file reads again with the same `shape` |

Feature kinds:

- A binary feature has two values, for example `yes` and `no`.
- A categorical feature has named values with no order, for example a job.
- An ordinal feature has numbers with an order but not equal steps, for example a scale from 1 to 4.

## Read a chart

- Histogram: the height of a bar is the number of values in its range. A separate bar at 0 can show a different event, for example no exam.
- Box plot: the line is the median. The box has the middle 50% of values. Points outside the whiskers are possible outliers.
- If the mean is much smaller or larger than the median, a tail or outliers move the mean.
- One extreme value compresses all other bars of a histogram into one narrow bar.

## Agent check

The agent ran these examples with pandas 2.3.3 and seaborn 0.13.2 on local Python 3.9.6 on 2026-11-10.

| Check | Result |
| --- | --- |
| A column equal to a second column × 10 | Ratio `[10.]`, correlation 1.0 |
| `groupby("club")` on points | `no`: 5 rows, mean 33.0. `yes`: 6 rows, mean 67.5 |
| `groupby("level")` on points | Means 21.7, 47.5, 75.0, 90.0. Level 4 has only 1 row |
| `df[df["points"] > 0]` on 12 rows with one 0 and one `NaN` | 10 rows: the filter also removes `NaN` |

## Common errors

| Error | Result | Correction |
| --- | --- | --- |
| `pd.cut` with bins `[-inf, 40, 70, inf]` for "40 to 70 inclusive" | The default puts 40 in the low group. `right=False` puts 70 in the high group | Use a function with `<` and `<=`, then test the limit values |
| A function for `apply` with no `NaN` check | A missing value goes into the last group | Return `np.nan` first if `pd.isna(value)` |
| A filter such as `> 0` | It also removes rows with `NaN` | Write this in the conclusion, or remove `NaN` in a separate step |
| A mean of a group with 1 to 3 rows | The value can be random | Show `count` near the mean |
| A different mean is called a cause | Other features can have an effect on both | Write "associated with" |
| No check after a cleaning step | An incorrect mask can remove too many rows | Show `shape` before and after |
| The data file is not in `/content` in Colab | `FileNotFoundError` | Upload the file in the Files panel before Restart and run all |

## Recall questions

1. Which three parts must a conclusion have?
2. How do you show that one column is redundant?
3. Why do you show `count` near a group mean?
4. What does the box of a box plot show?
5. Why can one extreme value make a histogram hard to read?
6. What happens to `NaN` in the filter `df[df["x"] > 0]`?
7. Why is a function safer than `pd.cut` for a range with an inclusive end?

## Sources

- [pandas documentation](https://pandas.pydata.org/docs/)
- [seaborn tutorial](https://seaborn.pydata.org/tutorial.html)
