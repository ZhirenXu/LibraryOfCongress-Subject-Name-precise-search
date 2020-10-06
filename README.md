# LibraryOfCongress-Subject-Name-Scrapper  

A script that can scrapes terms from LOC for library use.

Base on  https://github.com/ruthtillman/subjectreconscripts

User can choose search mode and generate a csv file as output.
Currently support LCNAF and LCSH searching.
If there are terms that cannot return precise search result, an csv of failed names/subjects will generate.
If all input terms failed, there will only be failure report, no normal output csv.

## Prerequisites:  

   Run in Windows10 environment. 
   
   Python ver. 3.8 or higher, other version has not been tested. 
   
   Required Package: 
      
      BeautifulSoup 
	  
	  ProgressBar2  
      
   If not installed, please open CMD, go to the path of id scraper folder, then type following command:
   
	  pip install -r dependencies.txt  

   If dependencies.txt doesn't exist or command above has failure, try manually install dependencies by tying following command:
      
      pip install bs4  
	  
	  pip install progressbar2  
	
## Instruction
1. put csv file which contain name terms or subject terms in the same folder as the LOC Scrapper. CSV file SHOULD NOT conatin header.
2. run 'LOC exact search.py'  
3. follow instructions on display  