# NTU Courses Web Scraper
A script to scrape courses that are available on the NTUCOOL. 

## Prerequisites

- Python (version 3.x recommended)
- Selenium ChromeDriver (compatible with your Chrome browser version)
- argparse, re, os, json, threading libraries (these typically come pre-installed with Python)

## Usage

### Basic
To run the scraper with default settings
```python cool_scraper.py```

### Arguments

- `--verbose`: Enable verbose output. If you want to see detailed logs while the script is running, include this flag.
- `--cookie`:  Use a cookie for authentication. If you have a `cookie.json` file for the website authentication, include this flag to use it. The format for the cookie should be a JSON list containing the necessary cookie data.
- `--counts`: Define the number of threads for multi-threading. By default, it's set to 25. E.g., `--counts 50` will use 50 threads.

## Output

The script will generate an output file final_output.txt that will contain the list of course IDs and their names.

## Note

If you're using the --cookie argument, make sure you have a cookie.json file in the same directory as the script.

