import csv

class Company:
    ratingByMonthYear = dict()

# TODO: rename ratings to score. Refactoring tool not working rn
class Month:
    ratingsAllSum = 0
    ratingsAllCount = 0
    ratingsAll = 0.0

    ratingsCurrentOnlySum = 0
    ratingsCurrentOnlyCount = 0
    ratingsCurrentOnly = 0.0

    ratingsFormerOnlySum = 0
    ratingsFormerOnlyCount = 0
    ratingsFormerOnly = 0.0

class Rating:
    company = str()
    date = str()
    rating = int()
    employeeStatus = str()

def extractDate(dateRaw):
    return dateRaw[:4] + dateRaw[-2:]

def extractEmployeeStatus(employeeStatusRaw):
    return employeeStatusRaw.split()[0]

def formatAndPrintScoreSummary():
    printHeader()
    for company in companies:
        for date in companies[company].ratingByMonthYear:
            calculateAverages(companies[company].ratingByMonthYear[date])
            printMonthScore(company, date)

def calculateAverages(month):
        month.ratingsAll = calculateAverage(month.ratingsAllSum, month.ratingsAllCount)
        month.ratingsCurrentOnly = calculateAverage(month.ratingsCurrentOnlySum, 
                                                    month.ratingsCurrentOnlyCount)
        month.ratingsFormalOnly = calculateAverage(month.ratingsFormerOnlySum, 
                                                    month.ratingsFormerOnlyCount)

def calculateAverage(totalSum, count):
    return float(totalSum) / count if count != 0 else 0

def printHeader():
    print("In the works")

def printMonthScore(company, date):
    month = companies[company].ratingByMonthYear[date]
    print("{}\t{}\t{:.2f}\t{:.2f}\t{:.2f}".format(company, date, month.ratingsAll, 
                                        month.ratingsCurrentOnly, month.ratingsFormalOnly))

# Constants
COMPANY_NAME = 1
REVIEW_DATE = 3
OVERALL_SCORE = 9

# Load csv
fl = open('employee_reviews.csv', 'r')
data = csv.reader(fl, delimiter=',')

companies = dict()

next(data)
for row in data:
    rating = Rating()
    rating.company = str(row[COMPANY_NAME])

    dateRaw = str(row[REVIEW_DATE])
    
    if dateRaw == 'None':
        continue
    
    rating.date = extractDate(dateRaw)

    rating.score = int(float(row[OVERALL_SCORE]))

    employeeStatusRaw = str(row[4])
    rating.employeeStatus = extractEmployeeStatus(employeeStatusRaw)

    if rating.company not in companies:
        companies[rating.company] = Company()

    if rating.date not in companies[rating.company].ratingByMonthYear:
        companies[rating.company].ratingByMonthYear[rating.date] = Month()
    
    companies[rating.company].ratingByMonthYear[rating.date].ratingsAllSum += rating.score
    companies[rating.company].ratingByMonthYear[rating.date].ratingsAllCount += 1

    if rating.employeeStatus == 'Current':
        companies[rating.company].ratingByMonthYear[rating.date].ratingsCurrentOnlySum += rating.score
        companies[rating.company].ratingByMonthYear[rating.date].ratingsCurrentOnlyCount += 1

    elif rating.employeeStatus == 'Former':
        companies[rating.company].ratingByMonthYear[rating.date].ratingsFormerOnlySum += rating.score
        companies[rating.company].ratingByMonthYear[rating.date].ratingsFormerOnlyCount += 1

formatAndPrintScoreSummary()


