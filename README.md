# Datheon Python Programming Internship

This repository contains my completed tasks for the Datheon Python Programming Internship.

## Project Structure

Datheon_Python_Programming_Internship/
- Task1_Hangman/
  - hangman.py
- Task2_Portfolio/
  - portfolio.py
  - sample_prices.csv
  - portfolio_summary.csv
- Task3_Organizer/
  - organizer.py
  - organizer.log
  - demo_messy_folder/
- README.md

## Task 1: Hangman Word Guessing Game (Console)

Folder: `Task1_Hangman`

A terminal-based Hangman game in Python.

- Random word selection with `random.choice()`
- ASCII gallows art that updates with each wrong guess
- Tracks guessed letters using a set
- No penalty for repeated guesses
- Input validation (single letters only)
- Victory and defeat screens
- Play again option

How to run:

    py Task1_Hangman/hangman.py

## Task 2: Stock Portfolio Performance Tracker

Folder: `Task2_Portfolio`

A console utility that tracks an investment portfolio.

- Takes stock tickers, buy prices, and share quantities
- Validates tickers against the dataset (`sample_prices.csv`)
- Fetches live prices with `yfinance` (manual entry as a fallback)
- Calculates invested capital, market value, and gain/loss % per holding
- Combines repeated tickers using the weighted average buy price
- Saves results to `portfolio_summary.csv` using Python's `csv` module

How to run:

    cd Task2_Portfolio
    py portfolio.py

## Task 3: Automated File Organizer and Cleanup Utility

Folder: `Task3_Organizer`

A desktop automation script that sorts a cluttered folder into category subfolders.

- Maps file extensions to categories (Documents, Images, Videos, Archives, Code, Others)
- Scans files with `os.scandir()` and moves them with `shutil.move()`
- Handles `PermissionError` and `FileExistsError` with try/except
- Resolves naming collisions automatically (e.g. `report (1).pdf`)
- Dry run mode to preview changes before moving anything
- Demo mode that creates a safe sample folder for testing
- Prints a formatted execution summary and writes a log file (`organizer.log`)

How to run:

    cd Task3_Organizer
    py organizer.py

Press Enter at the folder prompt to use the demo folder, or enter the path of a folder to organize.

## Requirements

- Python 3
- `yfinance` (optional, for live prices in Task 2): `py -m pip install yfinance`

## Skills Demonstrated

- String manipulation and control flow
- Dictionaries, sets, and functions
- File I/O, CSV handling, and the `os`, `shutil`, and `pathlib` modules
- Exception handling and logging
- Input validation
- Working with an external library

