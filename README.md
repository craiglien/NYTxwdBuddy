# NYT Crossword Buddy

## Introduction

This repository contains a puzzle cracker I've developed to help with the crossword game I play on my phone.
The project has been a personal endeavor over the past few months and is now being made public for others to use and possibly contribute to.

## The Game

The Game is the New York Times Mini Crossword available for iPhone and Android.

## Features

- **Automated Puzzle Help:** Automatically cracks the puzzle daily and stores it in [daily.txt](./daily.txt).
- **GitHub Actions:** Utilizes GitHub Action "cron" to run the cracker daily.

## To run locally

### Prerequisites

This runs with standard Python, no additional modules are needed.

You can verify your Python version by running:

```bash
python --version
```
  
### Clone and Run

1. Clone the repository with the following command:
   ```bash
   git clone https://github.com/craiglien/NYTxwdBuddy.git
   ```
2. Run.
   ```bash
   python fetch_and_crack.py
   ```
   output
   ```bash
   [board will be here]
   Content fetched and stored in data/[current date].json
   [list of files added]
   ```
