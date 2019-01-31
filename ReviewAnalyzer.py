import csv

class Company:
    ratingByMonthYear = dict()

class Month:
    scoreAllSum = 0
    scoreAllCount = 0
    scoreAll = 0.0

    scoreCurrentOnlySum = 0
    scoreCurrentOnlyCount = 0
    scoreCurrentOnly = 0.0

    scoreFormerOnlySum = 0
    scoreFormerOnlyCount = 0
    scoreFormerOnly = 0.0

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
        month.scoreAll = calculateAverage(month.scoreAllSum, month.scoreAllCount)
        month.scoreCurrentOnly = calculateAverage(month.scoreCurrentOnlySum, 
                                                    month.scoreCurrentOnlyCount)
        month.ratingsFormalOnly = calculateAverage(month.scoreFormerOnlySum, 
                                                    month.scoreFormerOnlyCount)

def calculateAverage(totalSum, count):
    return float(totalSum) / count if count != 0 else 0

def printHeader():
    print("In the works")

def printMonthScore(company, date):
    month = companies[company].ratingByMonthYear[date]
    print("{}\t{}\t{:.2f}\t{:.2f}\t{:.2f}".format(company, date, month.scoreAll, 
                                        month.scoreCurrentOnly, month.ratingsFormalOnly))

def writeResultsCSV():
    flOut = open('summary_employee_reviews.csv', 'w')
    dataOut = csv.writer(flOut, delimiter=',')
    dataOut.writerow(['Company','Date','Total Score','Current Employees Score','Former EmployeesScore'])
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


