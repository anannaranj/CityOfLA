import os
import re
from dateutil.parser import parse
from word2number import w2n
import numpy as np
import pandas as pd

files = os.listdir("data/")

dfs = []
for filename in files:
    file = open(f"data/{filename}", "r", encoding="latin-1")
    content = file.read()

    def strtoint(s): return int("".join(re.findall(r'\d+', s, re.M)))

    def parseSalary(c):

        ranges = [[
            strtoint(x) for x in salaryrange.split(" to ")
        ] for salaryrange in
            re.findall(r"\$\d+(?:,)\d*\*? to \$\d+(?:,)\d*",
                       c, re.M)]

        avgOfRanges = [sum(r)/2 for r in ranges]

        fixedvalues = [strtoint(val) for val in re.findall(
            r"(?<!to )\$\d+(?:,\d+)?(?!.+to)", content, re.M)]

        if (len(avgOfRanges) + len(fixedvalues)) == 0:
            return np.nan

        avg = (sum(avgOfRanges) + sum(fixedvalues)) / \
              (len(avgOfRanges) + len(fixedvalues))

        return round(avg)
    
    def parseEdu(c):
        return " ".join([
                "university" if len(re.findall(r"university", c, flags=re.I|re.M))>0 else "",
                "college" if len(re.findall(r"college", c, flags=re.I|re.M))>0 else "",
                "apprenticeship" if len(re.findall(r"apprenticeship", c, flags=re.I|re.M))>0 else "",
                "highschool" if len(re.findall(r"high-? ?school", c, flags=re.I|re.M))>0 else "",
            ]).strip()
    
    def parsew2n(x):
        try:
            return float(w2n.word_to_num(x))
        except:
            return 0.0

    def parseExp(c):
        xp = re.findall(r"(?m)^\s*.*?\b([A-Za-z]+|\d+)\s+(years?|months?)\b(?=.*\bexperience\b).*$", content, flags=re.M|re.I)
        if len(xp)>0:
            if xp[0][1].lower() == "months":
                return parsew2n(xp[0][0]) / 12 or np.nan
            else:
                return parsew2n(xp[0][0]) or np.nan
        return np.nan


    obj = {
        "FILE_NAME": [filename],
        "JOB_CLASS_TITLE":
            re.findall(r"^(?:\s*)(?=\S).*?(?=  |$|\t)",
                       content, flags=re.M)[0].strip(),
        "JOB_CLASS_NO": int(
            (
                re.findall(r"(?<=code:)\s*[0-9]+",
                           content,
                           flags=re.I)
                or
                [2009]
            )[0]
        ),
        "OPEN_DATE": parse(
            re.findall(r"(?<=date:)\s*[A-Za-z0-9-, ]+",
                       content,
                       flags=re.M | re.I)[0]
        ),
        "DRIVERS_LICENSE_REQ": len(
            re.findall(r"driver.*(?=license)",
                       content,
                       flags=re.M | re.I)
        ) > 0,
        "ENTRY_SALARY": parseSalary(content),
        "SCHOOL_TYPE": parseEdu(content),
        "EDUCATION_YEARS": np.nan if type(parseEdu(content)) != str else 4 if parseEdu(content).split(" ")[0] in ["university", "college"] else 3 if parseEdu(content).split(" ")[0] == "apprenticeship" else np.nan,
        "EXPERIENCE_LENGTH": parseExp(content),
        "FULL_TIME_PART_TIME": ("part" if re.findall(
                r"(part|half|full)(?=.*time)",
                content,
                re.I
            )[0].lower() in ["part", "half"] else "full") if 
                len(re.findall(r"(part|half|full)(?=.*time)", content, re.I)) > 0
            else np.nan,
        "NON-RACIST": len(re.findall(r"(EQUAL EMPLOYMENT|OPEN COMPETITIVE|INTERDEPARTMENTAL)", content, re.I)) > 0,
        "JOB_DUTIES": (
            re.findall(r"(?:DUTIES AND RESPONSIBILITIES|DUTIES)\s*([\S ]+)",
                       content, flags=re.M)
            or
            [re.findall(r"^.+$", content, flags=re.M)[0]]
        )[0].strip(),
    }

    dfs.append(pd.DataFrame(obj))

final = pd.concat(dfs)
final.to_csv("data.csv")
# print(final.describe())
# print(final.head())
# print(final.info())
