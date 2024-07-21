import requests
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# Constants
BASE_URL = "https://hacker-news.firebaseio.com/v0/"
TOP_STORIES_URL = BASE_URL + "topstories.json"
ITEM_URL = BASE_URL + "item/{}.json"
TOP_STORIES_CSV = "top_stories.csv"
COMMENTS_CSV = "comments.csv"
STATS_CSV = "summary_stats.csv"
NUM_TOP_STORIES = 3  # Number of top stories to fetch and process

def fetch_top_stories():
    """
    Fetch the IDs of the top stories from Hacker News.
    
    Returns:
        list: A list of IDs of the top stories limited to NUM_TOP_STORIES.
    """
    response = requests.get(TOP_STORIES_URL)
    top_stories = response.json()
    return top_stories[:NUM_TOP_STORIES]  # limiting top stories num

def fetch_story_details(story_id):
    """
    Fetch the details of a story given its ID.
    
    Args:
        story_id (int): The ID of the story.
        
    Returns:
        dict: A dictionary containing the story details.
    """
    response = requests.get(ITEM_URL.format(story_id))
    story_details = response.json()
    return story_details

def fetch_comment_details(comment_id):
    """
    Fetch the details of a comment given its ID.
    
    Args:
        comment_id (int): The ID of the comment.
        
    Returns:
        dict: A dictionary containing the comment details.
    """
    response = requests.get(ITEM_URL.format(comment_id))
    comment_details = response.json()
    return comment_details

def save_top_stories_to_csv(stories):
    """
    Save the top stories to a CSV file.
    
    Args:
        stories (list): A list of dictionaries, each containing details of a story.
    """
    df = pd.DataFrame(stories)
    df.to_csv(TOP_STORIES_CSV, index=False)

def save_comments_to_csv(comments):
    """
    Save the comments to a CSV file.
    
    Args:
        comments (list): A list of dictionaries, each containing details of a comment.
    """
    df = pd.DataFrame(comments)
    df.to_csv(COMMENTS_CSV, index=False)

def analyze_and_save_stats(stories):
    """
    Analyze the top stories to generate summary statistics and save them to a CSV file.
    
    Args:
        stories (list): A list of dictionaries, each containing details of a story.
        
    Returns:
        dict: A dictionary containing the summary statistics.
    """
    df = pd.DataFrame(stories)
    avg_score = df['score'].mean()
    avg_comments = df['descendants'].mean()
    stats = {'average_score': avg_score, 'average_comments': avg_comments}
    stats_df = pd.DataFrame(stats, index=[0])
    stats_df.to_csv(STATS_CSV, index=False)
    return stats

def plot_stats(stats):
    """
    Plot the summary statistics using a bar chart.
    
    Args:
        stats (dict): A dictionary containing the summary statistics.
    """
    plt.figure(figsize=(10, 5))
    plt.bar(stats.keys(), stats.values(), color=['blue', 'orange'])
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.title('Summary Statistics of Top Stories')
    plt.show()

def main():
    """
    Main function to orchestrate the data collection, saving, analysis, and plotting.
    """
    # Fetch top stories
    print("Fetching top stories...")
    top_stories_ids = fetch_top_stories()
    top_stories = []
    print("Complete.")
    
    # Fetch and save story details for each story
    for i in tqdm(range(NUM_TOP_STORIES), desc="Fetching story details..."):
        story_id = top_stories_ids[i]
        story_details = fetch_story_details(story_id)
        top_stories.append(story_details)
    print("Complete.")

    # Save top stories to CSV
    save_top_stories_to_csv(top_stories)

    # Fetch and save all comments IDs
    comments_ids = []
    for i in tqdm(range(len(top_stories)), desc="Fetching comment IDs..."):
        story = top_stories[i]
        if 'kids' in story:
            comments_ids.extend(story['kids'])
    print("Complete.")

    # Fetch and save comment details for each story
    all_comments = []
    for i in tqdm(range(len(comments_ids)), desc="Fetching comment details..."):
        comment_details = fetch_comment_details(comments_ids[i])
        all_comments.append(comment_details)
    print("Complete.")

    # Save comment details to CSV
    save_comments_to_csv(all_comments)

    # Analyze and save stats
    stats = analyze_and_save_stats(top_stories)
    
    # Plot stats
    plot_stats(stats)

if __name__ == "__main__":
    main()