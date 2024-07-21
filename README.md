# Hacker News Data Collection and Analysis

This Python program interacts with the Hacker News website and its API to perform various data collection and analysis operations. It fetches details about top stories and their comments, saves the data in CSV files, analyzes the collected data, and plots the results.

## Features

- Fetches the IDs of the top stories using the Hacker News API.
- Fetches details for each story including title, URL, score, author, time, and number of comments.
- Saves the story details in a structured CSV file.
- Fetches top-level comments for each top story.
- Saves the comment details in a separate structured CSV file.
- Analyzes the collected data to generate summary statistics (e.g., average score of top stories, average number of comments per story).
- Saves the summary statistics in a CSV file.
- Plots the analysis results using appropriate visualization libraries.

## Installation

1. Clone the repository:
    ```bash
    git clone <your-repository-url>
    ```

2. Navigate to the project directory:
    ```bash
    cd <your-project-directory>
    ```

3. Install the required libraries:
    ```bash
    pip install tqdm
    ```

## Usage

Run the `hacker_news.py` script to start the data collection and analysis process:
```bash
python hacker_news.py
```

## Project Structure

- hacker_news.py: The main script that orchestrates the data collection, saving, analysis, and plotting.
- top_stories.csv: The CSV file where top stories are saved.
- comments.csv: The CSV file where comments are saved.
- summary_stats.csv: The CSV file where summary statistics are saved.

## Output

The program generates the following output files:

- top_stories.csv: Contains details of the top stories.
- comments.csv: Contains details of the comments for the top stories.
- summary_stats.csv: Contains summary statistics of the top stories.

## Example

Here is a brief overview of what the script does:

- Fetches the IDs of the top stories.
- Fetches details for each top story and saves them in top_stories.csv.
- Fetches the top-level comments for each top story and saves them in comments.csv.
- Analyzes the data to compute average scores and comments, saving the results in summary_stats.csv.
- Plots the summary statistics.


## Acknowledgments

Thanks to the Hacker News API for providing the data.