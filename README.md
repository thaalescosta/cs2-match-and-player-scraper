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
