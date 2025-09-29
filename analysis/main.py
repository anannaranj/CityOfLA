# NOTE: The data.csv was NOT done by me, my try at extracting the data can be found at ../engineering
# This csv was done by executing code written by Antonello Buccoliero
# Link to his submission: https://www.kaggle.com/code/antonellobuccoliero/structured-csv-for-jobbullettin-lacity-with-tool

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data.csv", index_col=0)
cmap = plt.get_cmap("BrBG", 14)



#####################################
# Question 1:
#   A non-experienced job seeker wants to know what is the best job for him?

nonxpjobs = df[
        (
            (df["EXPERIENCE_LENGTH"] == 0) |
            (df["EXPERIENCE_LENGTH"].isna())
        ) &
        (
            (df["EDUCATION_YEARS"] == 0) |
            (df["EDUCATION_YEARS"].isna())
        )
    ]["JOB_CLASS_TITLE"]

# # print the jobs those dont require any experience or education at all
# for x in nonxpjobs: print(x)



#####################################
# Question 2:
#   A concerned parents contacts you to tell them if there is a spicific school type that would guaranteed for their child a good future if you can tell, and which is it ?

schooltypes = []
for x in df["SCHOOL_TYPE"].unique():
    if str(x) == "nan":
        continue
    schooltypes.append([x,len(df[df["SCHOOL_TYPE"] == x])])
schooltypes.sort(key=lambda s: -s[-1])

# # display a pie chart that shows the percentages
# plt.pie(
#     [z[1] / 683 for z in schooltypes],
#     labels = [z[0] for z in schooltypes],
#     colors = [cmap(11-i) for i in range(12)],
#     autopct = '%1.1f%%')
# plt.show()



#####################################
# Question 3:
#   What the best time in the year to be ready for a job applying in any experience level?

jobsbymonth = [0]*12
monthnames = "January,February,March,April,May,June,July,August,September,October,November,December".split(",")
for x in df["OPEN_DATE"].str.split("-"):
    jobsbymonth[int(x[1])-1] += 1

# # display a bar chart that shows how much jobs were opened in each month
# plt.bar(monthnames, jobsbymonth, color=cmap(10))
# plt.show()



#####################################
# Question 4:
#   Is experience more important than educational level?

subdf = df[["EXPERIENCE_LENGTH", "EDUCATION_YEARS", "ENTRY_SALARY"]].astype(float)

# # display a correlation matrix that shows which variable has bigger effect on the salary
# plt.figure(figsize=(10, 10))
# sns.heatmap(pd.DataFrame(subdf.corr(method="spearman")["ENTRY_SALARY"]), annot=True, cmap="BrBG", vmin=-1, vmax=1)
# plt.show()
# 
# # As seen, experience has bigger effect on the salary than the education.



#####################################
# Question 5:
#   Which fresh grade job that will guarantee many job offers in the future for him?

freshgraduate = df[df["EXPERIENCE_LENGTH"].isna() & (df["EDUCATION_YEARS"] > 0)]["JOB_CLASS_TITLE"]
# # print the jobs those don't require any experience but need education
# for title in freshgraduate: print(title)



#####################################
# Question 6:
# Based on the jobs requirments you structred above do you think that LA governate may bais a little for men over women or the applicant marital status for example may effect his chance to gain the job?

# # only 1 file doesn't have a keyword that indicated how LA has no bias whatsoever, but it also didn't mention that it had a bias to 1 race against the others
# print(df[df["NON-RACIST"] == False])



#####################################
# Question 7:
#   The city need an advice based on your analysis, build a new schools for more fresh non-experienced workers or encorge the work environment to help the workers to get promotions?

## Based on Q4, the experience has bigger effect than education. so the latter option has theoretically better results
 
 
 
#####################################
# Question 8:
#   What is the average salary for worker with a driver licence?

tsalaries = df[df["DRIVERS_LICENSE_REQ"] == True][["ENTRY_SALARY"]]
tsalaries.replace(-1, pd.NA, inplace=True)
tsalaries.dropna(inplace=True)
# print(tsalaries["ENTRY_SALARY"].mean().round().astype(int))

fsalaries = df[df["DRIVERS_LICENSE_REQ"] == False][["ENTRY_SALARY"]]
fsalaries.replace(-1, pd.NA, inplace=True)
fsalaries.dropna(inplace=True)
# print(fsalaries["ENTRY_SALARY"].mean().round().astype(int))

## RESULTS:
## Jobs with a required license:    97,670$
## Jobs without a required license: 95,926$
 
 
 
#####################################
# Question 9:
#   list the most feature that effect the salary of the worker.

dfcp = df.copy()
le = LabelEncoder()
strcols = dfcp.select_dtypes(include=['object']).columns
for col in strcols:
    dfcp[col] = le.fit_transform(dfcp[col])
del dfcp["NON-RACIST"]

# display a correlation matrix that shows which variable has bigger effect on the salary
plt.figure(figsize=(10, 10))
corr = dfcp.corr()
corr = corr.iloc[corr["ENTRY_SALARY"].argsort()[::-1]]
# corr = corr.iloc[corr["ENTRY_SALARY"].abs().argsort()[::-1]]

# sns.heatmap(pd.DataFrame(corr["ENTRY_SALARY"]), annot=True, cmap="BrBG", vmin=-1, vmax=1)
# plt.show()

## RESULTS:
## The 4 columns with the highest correlation with the salary are:
## JOB_CLASS_NO = 0.39
## EXPERIENCE_LENGTH = 0.16
## FULL_TIME_PART_TIME = -0.12
## EDUCATION_YEARS = 0.11

## Overall, the most important factor is the experience length