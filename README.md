# CS2 Matches and Players/Teams Scraper  

I was having a hard time finding good datasets of Counter-Strike 2 matches on the internet. Every dataset I found on Kaggle was either extremely outdated, way too simple, or both.  

After some googling, I figured why not make my own dataset with the data I actually want to analyze? So here we are.  

And while I'm at it, why not make it more interesting and maybe create a database in MySQL and a Power BI dashboard?  

---

![Getting the data](https://github.com/thaalescosta/cs2-match-and-player-scraper/blob/main/ExtractMatchData/_resources/diagram.png)  

## What Do These Scripts Do?  

You'll find two Jupyter Notebook scripts in this repository:  

- **`ExtractPlayerData.ipynb`** – Scrapes player information from HLTV.  
- **`ExtractMatchData.ipynb`** – Scrapes match data and processes demos.  

### ExtractPlayerData.ipynb  

- Scrapes the **Top N** teams on the HLTV ranking for their **players' names, photos, and countries**.  
- Stores the data in a Pandas DataFrame, including columns with the paths to the player and flag PNGs.  

![Players and flags pictures](https://github.com/thaalescosta/cs2-match-and-player-scraper/blob/main/ExtractPlayerData/_resources/example_pngs.png)  

This was done so I can create **dimension tables** containing information on all players and their respective teams.  

### ExtractMatchData.ipynb  

This script is more complex and can be divided into three parts:  

1. **Download match demos**  
   - Scrape the list of all matches within the chosen tournaments.  
   - Make GET requests to fetch direct download links.  
   - Download the demos.  

2. **Analyze each demo using a modified CSDA.exe**  
   - Extract data from the demos using [cs-demo-analyzer](https://github.com/akiver/cs-demo-analyzer).  
   - Store the extracted data in Pandas DataFrames.  

3. **Insert the DataFrames into a MySQL database (`dbCS2`)**  


After that, it's a matter of **cleaning and transforming** all these tables into an actual usable structure, defining what my **fact and dimension tables** will look like. **`Work in progress...`**  

The last step of this project is to **reproduce HLTV visuals for matches and players in Power BI**, with the help of **Figma** to create a clean and well-designed dashboard. **`Work in progress...`**  

---

## Tools  

- [x] **Browser automation using `Selenium`**  
- [x] **Scraping of HTML pages using `BeautifulSoup`**  
- [x] **`Pandas` to clean and structure data**  
- [x] **Modification of `CSDA.exe` to extract only the relevant data**  
- [x] **`MySQL` database to store all data**  
- [ ] **`SQL` querying to create fact and dimension tables**
- [ ] **Create the dashboard design in `Figma`**  
- [ ] **`Power BI` as a visualization tool**  

---

## Usage  

This project was designed for people like me—who aren't developers but know enough to put everything together and make it work.  

All downloads and script outputs are saved into the cloned folder. You shouldn't need to install anything beyond what's in the `requirements.txt` file.  

## Usage
Everything here was done thinking about people like me, who aren't actual developers/programmers but know enough to put this all together and actually make it work.

I made it so every download and output from these scripts are saved into the cloned folder and you shouldn't need to install anything else other than what's in the _requirements.txt_ file.

To clone this repository and run the scripts:
```
git clone https://github.com/thaalescosta/cs2-match-and-player-scraper.git
```
Install the _requirements.txt_ file:
```
pip install -r requirements.txt
```
Run **`ExtractMatchData.ipynb`** or **`ExtractPlayerData.ipynb`** to scrape the data you want.

&nbsp;

## Acknowledgements

This project uses the project [cs-demo-analyzer](https://github.com/akiver/cs-demo-analyzer) made by [@akiver](https://github.com/markus-wa) using [demoinfocs-golang](https://github.com/markus-wa/demoinfocs-golang) created by [@markus-wa] and maintained by him and [@akiver](https://github.com/akiver).


The modification was made to reduce the number of .csv files generated for each demo, generating only the ones I felt relevant to my project

&nbsp;

### License
[MIT](https://github.com/thaalescosta/cs2-match-and-player-scraper/blob/main/LICENSE)



