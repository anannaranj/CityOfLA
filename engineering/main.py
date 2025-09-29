import os
import re
from dateutil.parser import parse
from word2number import w2n
import numpy as np
import pandas as pd


def parseTitle(c):
    return re.findall(r"^(?:\s*)(?=\S).*?(?=  |$|\t)",
                      c, flags=re.M)[0].strip(),


def parseClassNo(c):
    return int(
        (
            re.findall(r"(?<=code:)\s*[0-9]+",
                       c,
                       flags=re.I)
            or
            [2009]
        )[0]
    )


def parseDate(c):
    return parse(
        re.findall(r"(?<=date:)\s*[A-Za-z0-9-, ]+",
                   c,
                   flags=re.M | re.I)[0]
    )


def parseDriverLicense(c):
    return len(
        re.findall(r"driver.*(?=license)",
                   c,
                   flags=re.M | re.I)
    ) > 0


def strtoint(s): return int("".join(re.findall(r'\d+', s, re.M)))


def parseSalary(c):

    ranges = [[
        strtoint(x) for x in salaryrange.split(" to ")
    ] for salaryrange in
        re.findall(r"\$\d+(?:,)\d*\*? to \$\d+(?:,)\d*",
                   c, re.M)]

    avgOfRanges = [sum(r)/2 for r in ranges]

    fixedvalues = [strtoint(val) for val in re.findall(
        r"(?<!to )\$\d+(?:,\d+)?(?!.+to)", c, re.M)]

    if (len(avgOfRanges) + len(fixedvalues)) == 0:
        return np.nan

    avg = (sum(avgOfRanges) + sum(fixedvalues)) / \
          (len(avgOfRanges) + len(fixedvalues))

    return round(avg)


def parseEdu(c):
    return " ".join([
        "university" if len(re.findall(
            r"university", c, flags=re.I | re.M)) > 0 else "",
        "college" if len(re.findall(
            r"college", c, flags=re.I | re.M)) > 0 else "",
        "apprenticeship" if len(re.findall(
            r"apprenticeship", c, flags=re.I | re.M)) > 0 else "",
        "highschool" if len(re.findall(
            r"high-? ?school", c, flags=re.I | re.M)) > 0 else "",
    ]).strip()


def parseEduYears(c):
    return (
        np.nan if type(parseEdu(c)) != str else
        4 if parseEdu(c).split(
            " ")[0] in ["university", "college"] else
        3 if parseEdu(c).split(
            " ")[0] == "apprenticeship" else np.nan
    )


def parsew2n(x):
    try:
        return float(w2n.word_to_num(x))
    except:
        return 0.0


def parseExp(c):
    xp = re.findall(
        r"(?m)^\s*.*?\b([A-Za-z]+|\d+)\s+(years?|months?)\b(?=.*\bexperience\b).*$",
        c,
        flags=re.M | re.I)
    if len(xp) > 0:
        if xp[0][1].lower() == "months":
            return parsew2n(xp[0][0]) / 12 or np.nan
        else:
            return parsew2n(xp[0][0]) or np.nan
    return np.nan


def parsePartTime(c):
    return ("part" if re.findall(
        r"(part|half|full)(?=.*time)",
        c,
        re.I
    )[0].lower() in ["part", "half"] else "full") if len(
        re.findall(r"(part|half|full)(?=.*time)", c, re.I)
    ) > 0 else np.nan


def parseDuties(c):
    return (
        re.findall(r"(?:DUTIES AND RESPONSIBILITIES|DUTIES)\s*([\S ]+)",
                   c, flags=re.M)
        or
        [re.findall(r"^.+$", c, flags=re.M)[0]]
    )[0].strip()


files = os.listdir("data/")

dfs = []
for filename in files:
    file = open(f"data/{filename}", "r", encoding="latin-1")
    content = file.read()

    obj = {
        "FILE_NAME": [filename],
        "JOB_CLASS_TITLE": parseTitle(content),
        "JOB_CLASS_NO": parseClassNo(content),
        "OPEN_DATE": parseDate(content),
        "DRIVERS_LICENSE_REQ": parseDriverLicense(content),
        "ENTRY_SALARY": parseSalary(content),
        "SCHOOL_TYPE": parseEdu(content),
        "EDUCATION_YEARS": parseEduYears(content),
        "EXPERIENCE_LENGTH": parseExp(content),
        "FULL_TIME_PART_TIME": parsePartTime(content),
        "NON-RACIST": len(re.findall(r"(EQUAL EMPLOYMENT|OPEN COMPETITIVE|INTERDEPARTMENTAL)", content, re.I)) > 0,
        "JOB_DUTIES": parseDuties(content),
    }

    dfs.append(pd.DataFrame(obj))

final = pd.concat(dfs)
final.to_csv("data.csv")
# print(final.describe())
# print(final.head())
# print(final.info())
