import csv
from enum import Enum

class Company:
    def __init__(self):
        self.ratingByMonthYear = dict()

class Month:
    def __init__(self):
        self.scoreAllSum = 0
        self.scoreAllCount = 0
        self.scoreAll = 0.0

        self.scoreCurrentOnlySum = 0
        self.scoreCurrentOnlyCount = 0
        self.scoreCurrentOnly = 0.0

        self.scoreFormerOnlySum = 0
        self.scoreFormerOnlyCount = 0
        self.scoreFormerOnly = 0.0

class Rating:
    def __init__(self):
        self.company = ''
        self.date = ''
        self.rating = 0
        self.employeeStatus = ''

class MonthFromStr(Enum):
    Jan = 1
    Feb = 2
    Mar = 3
    Apr = 4
    May = 5
    Jun = 6
    Jul = 7
    Aug = 8
    Sep = 9
    Oct = 10
    Nov = 11
    Dec = 12

def ifInvalidDate(dateRaw):
    return dateRaw[-4:] == '0000'

def extractDate(dateRaw):
    month = dateRaw[1:4]
    year = dateRaw[-2:]
    return str(MonthFromStr[month].value) + "-" + year

def extractEmployeeStatus(employeeStatusRaw):
    return employeeStatusRaw.split()[0]

def formatAndPrintScoreSummary():
    printHeader()
    for company in companies:
        for date in companies[company].ratingByMonthYear:
            calculateAverages(companies[company].ratingByMonthYear[date])
            printMonthScore(company, date)

def calculateAverages(month):
        month.scoreAll = calculateAverage(month.scoreAllSum, month.scoreAllCount)
        month.scoreCurrentOnly = calculateAverage(month.scoreCurrentOnlySum, 
                                                    month.scoreCurrentOnlyCount)
        month.ratingsFormalOnly = calculateAverage(month.scoreFormerOnlySum, 
                                                    month.scoreFormerOnlyCount)

def calculateAverage(totalSum, count):
    return float(totalSum) / count if count != 0 else 0

def printHeader():
    print("Company".ljust(10)+"\tDate\tAll\tCurrent\tFormer")

def printMonthScore(company, date):
    month = companies[company].ratingByMonthYear[date]
    print("{}\t{}\t{:.2f}\t{:.2f}\t{:.2f}".format(company.ljust(10), date.rjust(5), month.scoreAll, 
                                        month.scoreCurrentOnly, month.ratingsFormalOnly))

def writeResultsCSV():
    flOut = open('summary_employee_reviews.csv', 'w')
    dataOut = csv.writer(flOut, delimiter=',')
    dataOut.writerow(['Company','Date','Total','Current Emp.','Former Emp.'])
    for company in companies:
        for date in companies[company].ratingByMonthYear:
            month = companies[company].ratingByMonthYear[date]
            dataOut.writerow([company, date, '{:.2f}'.format(month.scoreAll), 
                '{:.2f}'.format(month.scoreCurrentOnly), '{:.2f}'.format(month.ratingsFormalOnly)])

# Constants
COMPANY_NAME = 1
REVIEW_DATE = 3
OVERALL_SCORE = 9

# Load csv
flIn = open('employee_reviews.csv', 'r')
dataIn = csv.reader(flIn, delimiter=',')

companies = dict()

next(dataIn)
for row in dataIn:
    rating = Rating()
    rating.company = str(row[COMPANY_NAME])

    dateRaw = str(row[REVIEW_DATE])
    
    if dateRaw == 'None' or ifInvalidDate(dateRaw):
        continue
    
    rating.date = extractDate(dateRaw)

    rating.score = int(float(row[OVERALL_SCORE]))
    
    employeeStatusRaw = str(row[4])
    rating.employeeStatus = extractEmployeeStatus(employeeStatusRaw)

    if rating.company not in companies:
        companies[rating.company] = Company()

    if rating.date not in companies[rating.company].ratingByMonthYear:
        companies[rating.company].ratingByMonthYear[rating.date] = Month()
    
    companies[rating.company].ratingByMonthYear[rating.date].scoreAllSum += rating.score
    companies[rating.company].ratingByMonthYear[rating.date].scoreAllCount += 1

    if rating.employeeStatus == 'Current':
        companies[rating.company].ratingByMonthYear[rating.date].scoreCurrentOnlySum += rating.score
        companies[rating.company].ratingByMonthYear[rating.date].scoreCurrentOnlyCount += 1

    elif rating.employeeStatus == 'Former':
        companies[rating.company].ratingByMonthYear[rating.date].scoreFormerOnlySum += rating.score
        companies[rating.company].ratingByMonthYear[rating.date].scoreFormerOnlyCount += 1

formatAndPrintScoreSummary()
writeResultsCSV()