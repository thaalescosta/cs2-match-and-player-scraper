# CS2 Matches and Players/Teams Scraper

I was having a hard time finding good datasets of Counter Strike 2 matches on the internet. Every dataset I found on Kaggle was either extremely outdated, way too simple or both.

After some googling I figured why not make my own dataset with the data I actually what to analyze. So here we are.

And while I'm at it, why not make it more interest and maybe create a database in MySQL and a Power BI dashboard.

![Getting the data](https://github.com/thaalescosta/cs2-match-and-player-scraper/blob/main/ExtractMatchData/_resources/diagram.png)


## So what do these scripts do?

Good question. You'll find two scripts in the Jupyter Notebooks here called ExtractPlayerData.ipynb and ExtractMatchData.ipynb

I won't go into too much detail about what exactly they're doing, but in summary:

**ExtractPlayerData.ipynb** scrapes the Top N teams on the HLTV ranking for their player's names, photos and countries. The data is stored in a Pandas dataframe, including columns with the paths to the players and flags PNGs

![Players and flags pictures](https://github.com/thaalescosta/cs2-match-and-player-scraper/blob/main/ExtractPlayerData/_resources/example_pngs.png)

This was done so I'm able to create dimension tables containing information on all Players and their respective teams.

**ExtractMatchData.ipynb** is a bit more complex and can be divided into three parts:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. First part aims to download the demos of all matches played within the chosen tournaments. For this to happen the script had to first scrape the list of all matches, then make GET requests in order to fetch the direct links so it can finally download the demos.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Second part is to analyze every single demo using a modified CSDA.exe (you can learn more about it on their [repository](https://github.com/akiver/cs-demo-analyzer)). All data extracted from the demos are stored in dataframes as well.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Third part is inserting the dataframes into a MySQL database I called dbCS2.

After that, it's a matter of cleaning and transforming all of these tables into an actual usable structure, defining what my fact and dimension tables will look like. **WORK IN PROGRESS...**

Last thing of this project is to sort of reproduce the HLTV visuals for matches and players in Power BI, with the help of Figma to create a clean and nice looking dashboard. **WORK IN PROGRESS...**


## Tools
- [x] **Browser automation using Selenium**
- [x] **Scraping of HTML pages using BeautifulSoup**
- [x] **Pandas to clean and structure data**
- [x] **Modification of CSDA.exe to extract only the relevant data for this project**
- [x] **MySQL database created to store all data**
- [ ] **SQL querying to create fact and dimensions table**
- [ ] **Power BI as a visualization tool**

## Usage
Everything here was done thinking about people like me, who aren't actual developers/programmers but know enough to put this all together and actually make it work.

I made it so every download and output from these scripts are saved into the cloned folder and you shouldn't need to install anything else other than what's in the _requirements.txt_ file.


To clone this repository and run the scripts:
```
git clone https://github.com/yourusername/cs2-match-and-player-scraper.git
```
Install the _requirements.txt_ file:
```
pip install -r requirements.txt
```
Use the **ExtractMatchData.ipynb** or **ExtractPlayerData.ipynb** to scrape the data you want.

&nbsp;

## Acknowledgements

This project uses the project [cs-demo-analyzer](https://github.com/akiver/cs-demo-analyzer) made by [@akiver](https://github.com/markus-wa) using [demoinfocs-golang](https://github.com/markus-wa/demoinfocs-golang) created by [@markus-wa] and maintained by him and [@akiver](https://github.com/akiver).


The modification was made to reduce the number of .csv files generated for each demo, generating only the ones I felt relevant to my project

&nbsp;

### License
[MIT](https://github.com/thaalescosta/cs2-match-and-player-scraper/blob/main/LICENSE)



