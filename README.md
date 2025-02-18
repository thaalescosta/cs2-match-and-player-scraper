# CS2 Matches and Players/Teams Scraper

I was having a hard time finding datasets of Counter Strike 2 on the internet. After doing some googling I figured why not make my own.

And while I'm at it, why not make it more complex and maybe create a database in MySQL and a Power BI dashboard.

![test](https://github.com/thaalescosta/cs2-match-and-player-scraper/blob/main/ExtractMatchData/_resources/diagram.png)

## Tools
- [x] **Browser automation using Selenium**
- [x] **Scraping of HTML pages using BeautifulSoup**
- [x] **Pandas to clean and structure data**
- [x] **Modification of CSDA.exe to prevent useless data for this project**
- [ ] **MySQL database created to store all data**
- [ ] **SQL querying to create fact and dimensions table**
- [ ] **Power BI as a visualization tool**

## Usage
Everything was done thinking in those who are like me, who don't know much about programming but still is someone able to do something like this if they put their time into it.

Every download and output from the script will be saved into the cloned folder and you shouldn't need to install anything else other than what's in the _requirements.txt_ file.


Clone this repository:
```
git clone https://github.com/yourusername/cs2-match-and-player-scraper.git
```
Install the _requirements.txt_ file:
```
pip install -r requirements.txt
```
Use the **ExtractMatchData.ipynb** or **ExtractPlayerData.ipynb** to scrape the data you want.

&nbsp;

## About the scripts

#### **ExtractMatchData.ipynb**
I divided everything I wanted and needed to do into function to keep the notebook clean and easy to read.

You can snoop around the functions and see what's going on.
Comment out the _--headless_ line in **\\_resources\chromelib.py** to see what Selenium is doing.

In summary this is what I had the script do:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**1. Scrape through the results page of each tournament gathering the URLs for each matchup (Bo1, Bo3 or Bo5)**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**2. Use an ID found in the matchup page to get an URL, to make a GET request and retrieve the direct download link to the demos**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**3. Then download all demos and put them through **CSDA.exe** to process the .dem files and extract all sorts of data.**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**4. Once the demos are analyzed, all the data that I've been collecting throughout the process is stored in .csv files.**


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**5. Iinsert data into a **MySQL database** after I figure out how I want the tables to be structured and what information I need**

&nbsp;

#### **ExtractPlayerData.ipynb**
It's a simpler script that scrapes data about players from the top N HLTV teams (names, nicknames, PNG photos, country and more).
This data will be used to create a teams dataset to be later used in a Power BI dashboard.

So as with ExtractMatchData.ipynb, I divided everything into functions and these were the basic steps:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**1. Scrape the Top HLTV Teams gathering the URLs for each team page**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**2. Scrape the team pages to get the players data like full name, country, PNG photos, country flag and some more data.**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**3. Stored the data nice and clean in a dataframe or .csv file and later.**
  
## Acknowledgements
This project uses a modified demo parser [demoinfocs-golang](https://github.com/markus-wa/demoinfocs-golang) created by [@markus-wa](https://github.com/markus-wa) and maintained by him and [@akiver](https://github.com/akiver).

The modification was made to reduce the number of .csv files generated for each demo, generating only the ones I felt relevant to my project

&nbsp;

### License
[MIT](https://github.com/thaalescosta/cs2-match-and-player-scraper/blob/main/LICENSE)



