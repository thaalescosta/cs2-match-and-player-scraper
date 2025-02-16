<<<<<<< HEAD
// ... existing code ...
# CS2 Professional Match Data Analysis Pipeline

A comprehensive data pipeline for extracting, transforming, and analyzing professional Counter-Strike 2 match data from HLTV.org. This project automates the collection of match statistics, player performance metrics, and game events to enable detailed esports analytics.

## Project Overview

This pipeline processes professional CS2 matches by:
1. Scraping match data from HLTV.org
2. Downloading and extracting demo files
3. Processing demos using CS2 Demo Analyzer (CSDA)
4. Transforming raw data into structured datasets
5. Generating comprehensive match statistics

## Key Features

- **Automated Data Collection**
  - Match identification and metadata extraction
  - Automated demo file downloads with retry mechanisms
  - Cookie handling and session management
  - Progress tracking for long-running operations

- **Data Processing**
  - Demo file extraction and analysis
  - Player performance statistics
  - Kill events and trade analysis
  - Economy and equipment tracking
  - Round-by-round statistics

## Sample Data Output

### Clutches Table
| won | steamid | name | survived | kill_count | match_checksum | tournament |
|---|---|---|---|---|---|---|
| 0 | 76561198179538505 | Graviti | 0 | 1 | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

### Kills Table
| killer_name | killer_steamid | killer_team_name | victim_name | victim_steamid | victim_side | victim_team_name | weapon_name | headshot | killer_controlling_bot | is_trade_kill | match_checksum | tournament |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Graviti | 76561198179538505 | 3DMAX | Graviti | 76561198179538505 | 3 | 3DMAX | World | 0 | 0 | 0 | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

### Match Table
| checksum | date | map | tournament |
|---|---|---|---|
| 1229e6b33a7c388f | 2025-01-14 13:32:46-03:00 | de_ancient | BLAST Bounty 2025 Season 1 |

### Players Table
| name | steamid | team_name | kills | assists | deaths | headshots | hs_% | k/d | kast | avg_damages_per_round | avg_kills_per_round | avg_death_per_round | utility_damage_per_round | health_damage | armor_damage | utility_damage | first_kill | first_death | trade_kill | trade_death | 1k | 2k | 3k | 4k | 5k | match_checksum | tournament |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Djoko | 76561198047876970 | 3DMAX | 17 | 6 | 21 | 8 | 47 | 0.809524 | 70.0 | 61.733334 | 0.566667 | 0.7 | 3.4 | 1852 | 276 | 102 | 3 | 3 | 4 | 4 | 6 | 4 | 1 | 0 | 0 | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

### Players Economy Table
| steamid | name | player_side | equipment_value | type | match_checksum | tournament |
|---|---|---|---|---|---|---|
| 76561198872013168 | tN1R | Terrorist | 1050 | pistol | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

### Teams Table
| name | team | match_checksum | tournament |
|---|---|---|---|
| 3DMAX | Team A | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

## Technical Stack

- Python 3.13.2
- Pandas for data manipulation
- Selenium for web scraping
- BeautifulSoup4 for HTML parsing
- CSDA for demo analysis
- Custom ETL pipeline

## Requirements
```
beautifulsoup4==4.13.3
pandas==2.2.3
rarfile==4.2
Requests==2.32.3
selenium==4.28.1
tqdm==4.67.1
```	

## Usage

1. Configure tournament IDs in `main.py`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the pipeline: `python main.py`
4. Access processed data in the `match_tables` directory

## Data Applications

This dataset enables various analyses:
- Player performance tracking
- Team strategy analysis
- Meta-game analysis
- Economic decision making
- Clutch situation analysis
- Weapon usage patterns

## Notes

- Requires CSDA executable for demo processing
- Respects HLTV.org rate limits and terms of service
- Handles large-scale data processing efficiently
- Implements robust error handling and logging
=======
# CS2 HLTV Events and Match Data Scraper

[cs-demo-analyzer](https://github.com/akiver/cs-demo-analyzer)


# CS2 Match Data Structure

This repository contains data extracted from CS2 demo files, organized into several tables. Below are the table structures with example data:

### **tbMatchData**
| checksum | date | map | tournament |
|:---|:---|:---|:---|
| 1229e6b33a7c388f | 2025-01-14 13:32:46-03:00 | de_ancient | BLAST Bounty 2025 Season 1 |

### **tbTeams**
| name | team | match_checksum | tournament |
|:---|:---|:---|:---|
| 3DMAX | Team A | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

### **tbPlayers**
| name | steamid | team_name | kills | assists | deaths | headshots | hs_% | k/d | kast | avg_damages_per_round | avg_kills_per_round | avg_death_per_round | utility_damage_per_round | health_damage | armor_damage | utility_damage | first_kill | first_death | trade_kill | trade_death | 1k | 2k | 3k | 4k | 5k | match_checksum | tournament |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| Djoko | 76561198047876970 | 3DMAX | 17 | 6 | 21 | 8 | 47 | 0.809524 | 70.0 | 61.733334 | 0.566667 | 0.7 | 3.4 | 1852 | 276 | 102 | 3 | 3 | 4 | 4 | 6 | 4 | 1 | 0 | 0 | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

### **tbKills**
| killer_name | killer_steamid | killer_team_name | victim_name | victim_steamid | victim_side | victim_team_name | weapon_name | headshot | killer_controlling_bot | is_trade_kill | match_checksum | tournament |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| Graviti | 76561198179538505 | 3DMAX | Graviti | 76561198179538505 | 3 | 3DMAX | World | 0 | 0 | 0 | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

### **tbPlayersEconomy**
| steamid | name | player_side | equipment_value | type | match_checksum | tournament |
|:---|:---|:---|:---|:---|:---|:---|
| 76561198872013168 | tN1R | Terrorist | 1050 | pistol | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

### **tbClutches**
| won | steamid | name | survived | kill_count | match_checksum | tournament |
|:---|:---|:---|:---|:---|:---|:---|
| 0 | 76561198179538505 | Graviti | 0 | 1 | 1229e6b33a7c388f | BLAST Bounty 2025 Season 1 |

Each table is linked by the `match_checksum` field, which uniquely identifies each match. The `tournament` field indicates which event the data is from.
>>>>>>> 9a85bceb1cf6fb5ce3d1ffd602d5c56a5222c5f8
