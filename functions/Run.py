import urllib.request
import concurrent.futures
from bs4 import BeautifulSoup
from functions import PreciseSearch
from functions import SimpleCSV
import sys

def loadUrl(url):
    html = urllib.request.urlopen(url)
    return html

##main process of search in two mode
# @param    *argv
#           parameters, first is suppoose to be a list conatin search keyword
#           second is suppose to be a boolean value of search mode
#           True for name search, False for subject search
# @return   resultList
#           a list of correct name
def processSerial(*argv):
    newPreciseResult = []
    preciseResult = []
    fuzzyResult = []
    resultList = []
    failedResult = []
    printOption = True
    isFailed = False
    #name search mode
    if argv[1] == True:
        print("\nSearch name terms in precise mode...")
        #preciseResult is a list contain list!
        try:
            preciseResult = PreciseSearch.preciseNameSearch(argv[0][1])
        except:
            print("\n Failure happen when try to search one of the keyword.")
            print("Please check your network. If this keep hapeening please send author a message.")
            print("Hit enter to exit.", end = "")
            input()
            sys.exit()
        failedResult = checkFailure(preciseResult, argv[0][1], printOption)
        #when some of them fail(most of the user case)
        if len(failedResult) > 0:
            resultList = preciseResult
            print("\nFailed name precise result find! Generate failed result report.")
            openedFail = open("failed names.csv", 'w', encoding = 'utf-8',newline='')
            for failed in failedResult:
                SimpleCSV.writeCSV([failed], openedFail)
            openedFail.close()
            for element in preciseResult:
                for failedTerm in failedResult:
                    if failedTerm == element[0]:
                        isFailed = True
                        break
                if not isFailed:
                    newPreciseResult.append(element)
                isFailed = False
            resultList = newPreciseResult
        #when all keyword fails(rare)
        elif len(failedResult) == len(argv[0][1]):
            resultList = []
            print("\nFailed name precise result find! Generate failed result report.")
            openedFail = open("failed names.csv", 'w', encoding = 'utf-8',newline='')
            for failed in failedResult:
                SimpleCSV.writeCSV([failed], openedFail)
            openedFail.close()
        #when all keywords success(extreme rare)
        elif len(failedResult) == 0:
            resultList = preciseResult
    #subject search mode
    elif argv[1] == False:
        print("\nSearch subject terms in precise mode...")
        try:
            preciseResult = PreciseSearch.preciseSubjectSearch(argv[0][1])
        except:
            print("\n Failure happen when try to search one of the keyword.")
            print("Please check your network. If this keep hapeening please send author a message.")
            print("Hit enter to exit.", end = "")
            input()
            sys.exit()
        failedResult = checkFailure(preciseResult, argv[0][1])
        #when some of them fail(most of the user case)
        if len(failedResult) > 0:
            resultList = preciseResult
            print("\nFailed subject precise result find! Generate failed result report.")
            openedFail = open("failed subjects.csv", 'w', encoding = 'utf-8',newline='')
            for failed in failedResult:
                SimpleCSV.writeCSV([failed], openedFail)
            openedFail.close()
            for element in preciseResult:
                for failedTerm in failedResult:
                    if failedTerm == element[0]:
                        isFailed = True
                        break
                if not isFailed:
                    newPreciseResult.append(element)
                isFailed = False
            resultList = newPreciseResult
        #when all keyword fails(rare)
        elif len(failedResult) == len(argv[0][1]):
            resultList = []
            print("\nNo subject precise result find! Generate failed result report.")
            openedFail = open("failed subjects.csv", 'w', encoding = 'utf-8',newline='')
            for failed in failedResult:
                SimpleCSV.writeCSV([failed], openedFail)
            openedFail.close()
        #when all keywords success(extreme rare)
        elif len(failedResult) == 0:
            resultList = preciseResult
    print("\nkeyword search complete!")
    return resultList

## Check if any precise search result is null.
## If true,delete it from search result and add to another list for fuzzySearch
## If isPrint is true, print user-friendly message
# @param    result
#           a list come from precise search, which have name/subject, url and perferred label
# @param    *terms
#           parameters, first is suppoose to be a list conatin search keyword
#           second is suppose to be a boolean value of search mode
#           True for name search, False for subject search
# @return   failed
#           a list contains all failed terms
def checkFailure(result, *terms):
    failed = []
    newPreciseResult = []

    print("\nCheck null results...", end = "")
    print("\nKeyword with no result: ")
    for element in result:
        if "null" in element:
            failed.append(element[0])
            print(element[0])
    print("Done!")
    return failed

## merge results from two search mode together
# @param    precise
#           a list contain lists which have name/subject, url and perferred label
# @param    fuzzy
#           a list contain lists which have name/subject, url and perferred label
# @return   combinedResult
#           a list contain list which none of them are null
def mergeResult(precise, fuzzy):
    combinedResult = []
    length = len(fuzzy)
    isMatched = False
    
    #need re-design this 6/8
    for element in precise:
        isMatched = False
        term = element[0]
        if "null" in element:
            for item in fuzzy:
                if item[0] == term:
                    combinedResult.append(item)
                    isMatched = True
                    break
            if isMatched == False:
                combinedResult.append(element)
        else:
            combinedResult.append(element)
    return combinedResult

## ask user what search mode they perfer to run
# @return   searchMode
#           A boolean value, true for name search, falsefor subject search
def askSearchMode():
    print("Which search mode you perfer?")
    print("1. Name search (LCNAF)        2. Subject search (LCSH)")
    print("Enter the number before each term: ", end = "")
    #empty input protection
    rawInput = input()
    #invalid input protection
    while len(rawInput) == 0 or int(rawInput) < 1 or int(rawInput) > 2:
        print("The number you selected is invalid. Please type in number displayed.")
        print("If you want to exit the program press ctrl+c.")
        print("Enter the number before each term: ", end = "")
        rawInput = input()
    if int(rawInput) == 1:
        return True
    else:
        return False

