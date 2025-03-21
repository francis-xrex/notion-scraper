# Script Execution Guide

This repository contains scripts for scraping SQL queries from Notion and executing them to estimate and clean up data.

## Scripts Overview

## `scraper_stable.py`
- Scrapes SQL queries from Notion pages listed in `notion_links.txt`
- Extracts SQL statements between markers:
  - `#count_tw_start` & `#count_tw_end`
  - `#count_ky_start` & `#count_ky_end`
  - `#clean_tw_start` & `#clean_tw_end`
  - `#clean_ky_start` & `#clean_ky_end`
- Saves extracted SQL files to:
  - `/count/count_tw/` and `/count/count_ky/` for count queries
  - `/delete/delete_tw/` and `/delete/delete_ky/` for cleanup queries

## `estimate_count.py`
  - Generates CSV files that estimate SQL execution time for the SQL files in the `/count` folder.

## `execute_sql.py`
  - This will execute all the SQL files under `/delete` folder.

## Setup Instructions

### Prerequisites
1. Python 3.x

### Installation

1. Install Python dependencies:
```
pip install -r requirements.txt
```

2. Configure properties files in `/properties` directory:
   - `credentials.properties`: Google login credentials for Notion
   - `config.properties`: Database and directory configurations
   - `notion_links.txt`: URLs of Notion pages to scrape

### Directory Structure
```
count_result/
├── script/
│   ├── scraper_stable.py
│   ├── estimate_count.py
│   └── execute_sql.py
├── properties/
│   ├── credentials.properties
│   ├── config.properties
│   └── notion_links.txt
├── count/
│   ├── count_tw/
│   └── count_ky/
├── delete/
│   ├── delete_tw/
│   └── delete_ky/
└── estimate/
    ├── estimate_tw/
    └── estimate_ky/
```


## Flow Chart
### run_count.py
```mermaid
flowchart TD
    A[Start] --> B[Clean up directories]
    B --> E[Use Selenium Login to Notion with Google]
    E --> F[Read services URLs from config file]
    F --> O[Access Notion page]
    
    O --> Q[Collect TW count SQL]
    O --> R[Collect KY count SQL]
    O --> S[Collect TW clean SQL]
    O --> T[Collect KY clean SQL]
    
    Q --> Z
    R --> Z
    S --> Z
    T --> Z[Persist as SQL file]
    
    Z --> V{Has next URLs?}
    
    V --> |Yes|O
    V --> |No|G[Done]
```

### execute.py
```mermaid
flowchart TD
    A[Start] --> D[Establish DB Connection]
    D --> G[Get SQL Files from delete directory]
    
    G --> L[Read SQL File]
    L --> P[Execute Each Command]
    
    P --> F{Has next file?}
    F --> |Yes|G
    F --> |No|GG[Done]
```
