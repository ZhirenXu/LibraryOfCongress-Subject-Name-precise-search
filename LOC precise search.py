from functions import Greeting
from functions import SimpleCSV
from functions import Run

def main():
    inputCSV = ""
    outputCSV = ""
    isSearchName = True
    keyword = []
    result = []
    
    #greeting
    Greeting.showInfo()
    isSearchName = Run.askSearchMode()
    #read from input, return rows in list, update search mode
    inputCSV = SimpleCSV.getCSVInput()
    outputCSV = SimpleCSV.getCSVOutput()
    keywords = SimpleCSV.readCSV(inputCSV, isSearchName)
    #run process (precise->fuzzy->output), return a list contain lists of each row
    result = Run.processSerial(keywords, isSearchName)
    #TODO: ask Ariel give input file and test it
    SimpleCSV.zipList(result)
    if len(result) != 0:
        #write into output csv
        openedOut = open(outputCSV, 'w', encoding = 'utf-8',newline='')
        for row in result:
            SimpleCSV.writeCSV(row, openedOut)
        #exit
        openedOut.close()
    Greeting.sysExit(outputCSV)
    
if __name__ == "__main__":
    main()
