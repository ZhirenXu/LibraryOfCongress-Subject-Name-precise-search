#Author: Ruth Kitchin Tillman
#Original script: https://github.com/ruthtillman/subjectreconscripts/blob/master/retrieve-lc-uris-from-csv.py
#Modifiied by: Zhiren Xu
import requests, os, time, urllib, progressbar
from functions import SimpleCSV

##Process the initial name to fit url format
# @param    word
#           keyword for LOC name search
# @return   a processed word which can put in url without error
def URI_escape(word):
  return word.replace(' -- ', '--').replace(' ', '%20').replace(',', '%2C').replace("'","%27").replace('(', '%28').replace(')', '%29')

##Precisely search the name (direct append into url to test if it exist)
# @param    *names
#           *arg, contain a list of name keywords
# @return   combinedNameData
#           a list contain lists which have name, url and perferred label
def preciseNameSearch(*names):
    nameData = []
    errName = []
    # a list contain names that fail to find in preciseSearch
    combinedNameData = []
    counter = 1
    k = 0
    totalRecordNum = len(names[0])
    
    for k in progressbar.progressbar(range(len(names[0])), redirect_stdout=True):
      name = names[0][k]
      processedName = URI_escape(name)
      print("Processing ", counter, " / ", totalRecordNum, " of records...", end = "")
      nameURL = 'https://id.loc.gov/authorities/names/label/' + processedName
      try:
        nameResponse = requests.head(nameURL)
      except:
        print("Fail to request: ", name)
        errName.append([name])
      if nameResponse.status_code == 302:
          try:
              nameData.append(name)
              nameData.append(name)
              nameData.append(nameResponse.headers['X-Uri'])
              nameData.append(nameResponse.headers['X-Preflabel'])
          except:
              print("Fail to get part of the header. The record may be broken.")
              print("\nFail to request: ", name)
              errName.append([name])
      else:
        if nameResponse.status_code == 301:
            print("\nHTTP 301- Request link has been moved permanently....", end = "")
            print("Fail to request: ", name)
            errName.append([name])
        elif nameResponse.status_code == 404:
            print("\nHTTP 404- Request link page doesn't exist....", end = "")
            print("Fail to request: ", name)
            errName.append([name])
        else:
            print("\n HTTP", subjectResponse.status_code, "- Not a valid response for scraping....", end = "")
            print("Fail to request: ", name)
            errName.append([name])
        #TODO: name not appended, no err file out
        nameData.append(name)
        nameData.append("null")
        nameData.append("null")
        nameData.append("null")
      combinedNameData.append(nameData)
      print("Done!")
      counter = counter + 1
      k = k + 1
      nameData = []
    if(len(errName) > 0):
        errorOut = open("Failed Name.csv", 'w', encoding = 'utf-8', newline = '')
        SimpleCSV.writeCSV(["Failed Names"], errorOut)
        for name in errName:
          SimpleCSV.writeCSV(name, errorOut)
        print("\nName that cause error is put into Failed Name.csv")
        errorOut.close()
    #add header for output file
    combinedNameData.insert(0, ["Internal ID link", "Raw Name", "Correct Name", "LC_URI", "LC_Label"])
    return combinedNameData

##Precisely search the subject (direct append into url to test if it exist)
# @param    *subjects
#           *arg, contain a list of subject keywords
# @return   combinedSubjectData
#           a list contain lists which have subject, url and perferred label    
def preciseSubjectSearch(*subjects):
    #print(subjects)
    subjectData = []
    combinedSubjectData = []
    errSubject = []
    counter = 1
    k = 0
    totalRecordNum = len(subjects[0])
    
    #for loop can be parallelized. Nope, add progress bar for pretty output
    for k in progressbar.progressbar(range(len(subjects[0])), redirect_stdout=True):
      subject = subjects[0][k]
      print("Processing ", counter, " / ", totalRecordNum, " of records...", end = "")
      processedSubject = URI_escape(subject)
      subjectURL = 'https://id.loc.gov/authorities/subjects/label/' + processedSubject
      try:
        subjectResponse = requests.head(subjectURL)
      except:
        print("Fail to request: ", subject)
        #print(subjectResponse.headers)
        errSubject.append([subject])
      if subjectResponse.status_code == 302:
          try:
              subjectData.append(subject)
              subjectData.append(subject)
              subjectData.append(subjectResponse.headers['X-Uri'])
              subjectData.append(subjectResponse.headers['X-Preflabel'])
          except:
              print("Fail to get part of the header. The record may be broken.")
              print("\nFail to request: ", subject)
              errSubject.append([subject])
      else:
          if subjectResponse.status_code == 301:
            print("\nHTTP 301- Request link has been moved permanently....", end = "")
          elif subjectResponse.status_code == 404:
            print("\nHTTP 404- Request link page doesn't exist....", end = "")
          else:
            print("\n HTTP", subjectResponse.status_code, "- Not a valid response for scraping....", end = "")
          subjectData.append(subject)
          subjectData.append("null")
          subjectData.append("null")
          subjectData.append("null")
          print("Fail to request: ", subject)
          errSubject.append([subject])
      combinedSubjectData.append(subjectData)
      print("Done!")
      subjectData=[]
      counter = counter + 1
      k = k + 1
    #add header for output file
    if(len(errSubject) > 0):
        errSubject.insert(0, ["Failed Subjects"])
        errorOut = open("Failed Subject.csv", 'w', encoding = 'utf-8', newline = '')
        for subject in errSubject:
          SimpleCSV.writeCSV(subject, errorOut)
        errorOut.close()
        print("\nSubject that cause error is put into Failed Subject.csv")
    combinedSubjectData.insert(0, ["Internal ID Link", "Raw subject", "Correct Subject", "LC_URI", "LC_Label"])
    return combinedSubjectData

