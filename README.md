# Script Execution Guide

The script `/script/run_count.py` will execute the following steps:

## 1. `scraper_stable.py`
   - Scrapes links from `notion_links.txt`.
   - Extracts SQL statements between the following markers:
     - `#count_tw_start` & `#count_tw_end`
     - `#count_ky_start` & `#count_ky_end`
     - `#clean_tw_start` & `#clean_tw_end`
     - `#clean_ky_start` & `#clean_ky_end`
   - Saves the extracted SQL files under the `/count` and `/delete` folders.

## 2. `estimate_count.py`
   - Generates CSV files that estimate SQL execution time for the SQL files in the `/count` folder.

## Flow Chart
```mermaid
graph TD
    A[Start] --> E[Use Selenium Login Notion]
    E --> F[Read URLs from File]
    
    F --> J[Access Notion Page]
    
    J --> N{Has #count_tw_start?}
    N -->|Yes| O[Save TW Content to File]
    N -->|No| P{Has #count_ky_start?}
    O --> P
    
    P -->|Yes| Q[Save KY Content to File]
    P -->|No| R[Process Next URL]
    Q --> R
    
    R --> S{More URLs?}
    S -->|Yes| J
    S -->|No| U[End]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style U fill:#f9f,stroke:#333,stroke-width:2px
    style O fill:#6f6,stroke:#333,stroke-width:2px
    style Q fill:#6f6,stroke:#333,stroke-width:2px
