# CS2 Matches and Players/Teams Data Scraper

This scraper basically does two things:
1. **ExtractMatchData.ipynb** is the notebook that handles item 1.

1. Download and analyze demos from every single match within N chosen events
2. Gather data about players from top N HLTV teams (names, nicknames, PNG photos, country and more)



**ExtractPlayerData.ipynb** is the notebook that handles item 2.

## Project Overview

This repository contains two main Jupyter notebooks that handle different aspects of the data pipeline:

### ExtractMatchData.ipynb
Skills & Technologies Demonstrated:
- Web scraping using Selenium and BeautifulSoup4
- Automated file downloads and handling
- Cookie/session management
- ETL pipeline development
- Error handling and retry mechanisms

Data Pipeline:
1. Scrapes match metadata from HLTV.org
2. Downloads match demo files
3. Processes demos using CS2 Demo Analyzer
4. Transforms raw data into structured tables
5. Outputs match-level statistics

Output Tables:
- **Matches**: Basic match information
  ```
  | checksum | date | map | tournament |
  |----------|------|-----|------------|
  ```
- **Teams**: Team compositions and sides
  ```
  | name | team | match_checksum | tournament |
  |------|------|----------------|------------|
  ```
- **Players Economy**: Round-by-round economic data
  ```
  | steamid | name | player_side | equipment_value | type | match_checksum | tournament |
  |---------|------|-------------|-----------------|------|----------------|------------|
  ```

## **ExtractPlayerData.ipynb**
Skills & Technologies Demonstrated:
- Data transformation and cleaning
- Statistical analysis
- Performance metric calculations
- Advanced pandas operations

Data Pipeline:
1. Processes player-level events from demo files
2. Calculates performance metrics
3. Analyzes clutch situations and trade patterns
4. Generates comprehensive player statistics

Output Tables:
- **Players**: Comprehensive player statistics
  ```
  | name | steamid | team_name | kills | assists | deaths | headshots | hs_% | k/d | kast | ... |
  |------|---------|-----------|-------|---------|--------|-----------|------|-----|------|-----|
  ```
- **Clutches**: Analysis of 1vX situations
  ```
  | won | steamid | name | survived | kill_count | match_checksum | tournament |
  |-----|---------|------|----------|------------|----------------|------------|
  ```
- **Kills**: Detailed kill event data
  ```
  | killer_name | killer_steamid | victim_name | weapon_name | headshot | is_trade_kill | ... |
  |-------------|----------------|-------------|-------------|----------|----------------|-----|
  ```


