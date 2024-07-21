import requests
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

class HackerNewsDataCollector:
    """
    A class to collect, analyze, and visualize data from Hacker News.
    """

    BASE_URL = "https://hacker-news.firebaseio.com/v0/"
    TOP_STORIES_URL = BASE_URL + "topstories.json"
    ITEM_URL = BASE_URL + "item/{}.json"
    TOP_STORIES_CSV = "top_stories.csv"
    COMMENTS_CSV = "comments.csv"
    STATS_CSV = "summary_stats.csv"

    def __init__(self, num_top_stories=3):
        """
        Initialize the data collector with the number of top stories to fetch.

        Args:
            num_top_stories (int): Number of top stories to fetch and process.
        """
        self.num_top_stories = num_top_stories
        self.top_stories = []
        self.comments = []

    def fetch_top_stories(self):
        """
        Fetch the IDs of the top stories from Hacker News.

        Returns:
            list: A list of IDs of the top stories limited to num_top_stories.
        """
        response = requests.get(self.TOP_STORIES_URL)
        top_stories = response.json()
        return top_stories[:self.num_top_stories]

    def fetch_story_details(self, story_id):
        """
        Fetch the details of a story given its ID.

        Args:
            story_id (int): The ID of the story.

        Returns:
            dict: A dictionary containing the story details.
        """
        response = requests.get(self.ITEM_URL.format(story_id))
        story_details = response.json()
        return story_details

    def fetch_comment_details(self, comment_id):
        """
        Fetch the details of a comment given its ID.

        Args:
            comment_id (int): The ID of the comment.

        Returns:
            dict: A dictionary containing the comment details.
        """
        response = requests.get(self.ITEM_URL.format(comment_id))
        comment_details = response.json()
        return comment_details

    def save_top_stories_to_csv(self):
        """
        Save the top stories to a CSV file.
        """
        df = pd.DataFrame(self.top_stories)
        df.to_csv(self.TOP_STORIES_CSV, index=False)

    def save_comments_to_csv(self):
        """
        Save the comments to a CSV file.
        """
        df = pd.DataFrame(self.comments)
        df.to_csv(self.COMMENTS_CSV, index=False)

    def analyze_and_save_stats(self):
        """
        Analyze the top stories to generate summary statistics and save them to a CSV file.

        Returns:
            dict: A dictionary containing the summary statistics.
        """
        df = pd.DataFrame(self.top_stories)
        avg_score = df['score'].mean()
        avg_comments = df['descendants'].mean()
        stats = {'average_score': avg_score, 'average_comments': avg_comments}
        stats_df = pd.DataFrame(stats, index=[0])
        stats_df.to_csv(self.STATS_CSV, index=False)
        return stats

    def plot_stats(self, stats):
        """
        Plot the summary statistics using a bar chart.

        Args:
            stats (dict): A dictionary containing the summary statistics.
        """
        plt.figure(figsize=(10, 5))
        plt.bar(stats.keys(), stats.values(), color=['blue', 'green'])
        plt.xlabel('Metrics')
        plt.ylabel('Values')
        plt.title('Summary Statistics of Top Stories')
        plt.show()

    def collect_data(self):
        """
        Orchestrate the data collection, saving, analysis, and plotting.
        """
        # Fetch top stories
        print("Fetching top stories...")
        top_stories_ids = self.fetch_top_stories()
        for story_id in tqdm(top_stories_ids, desc="Fetching story details..."):
            story_details = self.fetch_story_details(story_id)
            self.top_stories.append(story_details)
        print("Complete.")

        # Save top stories to CSV
        self.save_top_stories_to_csv()

        # Fetch all comment IDs for each story
        comments_ids = []
        for story in tqdm(self.top_stories, desc="Fetching comment IDs..."):
            if 'kids' in story:
                comments_ids.extend(story['kids'])
        print("Complete.")

        # Fetch details for each comment
        for comment_id in tqdm(comments_ids, desc="Fetching comment details..."):
            comment_details = self.fetch_comment_details(comment_id)
            self.comments.append(comment_details)
        print("Complete.")

        # Save comment details to CSV
        self.save_comments_to_csv()

        # Analyze and save stats
        stats = self.analyze_and_save_stats()

        # Plot stats
        self.plot_stats(stats)

if __name__ == "__main__":
    # Create an instance of HackerNewsDataCollector with the desired number of top stories
    collector = HackerNewsDataCollector(num_top_stories=3)
    # Collect and process data
    collector.collect_data()