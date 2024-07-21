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
NUM_TOP_STORIES = 3


def fetch_top_stories():
    response = requests.get(TOP_STORIES_URL)
    top_stories = response.json()
    return top_stories[:NUM_TOP_STORIES]  # limiting top stories num


def fetch_story_details(story_id):
    response = requests.get(ITEM_URL.format(story_id))
    story_details = response.json()
    return story_details

def fetch_comment_details(comment_id):
    response = requests.get(ITEM_URL.format(comment_id))
    comment_details = response.json()
    return comment_details


def save_top_stories_to_csv(stories):
    df = pd.DataFrame(stories)
    df.to_csv(TOP_STORIES_CSV, index=False)


def save_comments_to_csv(comments):
    df = pd.DataFrame(comments)
    df.to_csv(COMMENTS_CSV, index=False)


def analyze_and_save_stats(stories):
    df = pd.DataFrame(stories)
    avg_score = df['score'].mean()
    avg_comments = df['descendants'].mean()
    stats = {'average_score': avg_score, 'average_comments': avg_comments}
    print(stats)
    stats_df = pd.DataFrame(stats, index=[0])
    print(stats_df)
    stats_df.to_csv(STATS_CSV, index=False)
    return stats


def plot_stats(stats):
    plt.figure(figsize=(10, 5))
    plt.bar(stats.keys(), stats.values(), color=['blue', 'orange'])
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.title('Summary Statistics of Top Stories')
    plt.show()


def main():
    # Fetch top stories
    print("fetching top stories...")
    top_stories_ids = fetch_top_stories()
    top_stories = []
    print("Complete.")
    
    # Fetch and save story details for each story
    for i in tqdm (range (NUM_TOP_STORIES), desc="fetching story details..."):
        story_id = top_stories_ids[i]
        story_details = fetch_story_details(story_id)
        top_stories.append(story_details)
    print("Complete.")

    # Save top stories to CSV
    save_top_stories_to_csv(top_stories)

    # Fetch and save all comments ids
    comments_ids = []
    for i in tqdm (range (len(top_stories)), desc="fetching comment ids..."):
        story = top_stories[i]
        if 'kids' in story:
                comments_ids.extend(story['kids'])
    print("Complete.")

    # Fetch and save comment details for each story
    all_comments = []
    for i in tqdm (range (len(comments_ids)), desc="fetching comment details..."):
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

