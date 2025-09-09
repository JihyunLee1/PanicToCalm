import praw
import json
import time
# Reddit API credentials
    client_id = FROM_REDDIT_CLIENT_ID
    client_secret = FROM_REDDIT_CLIENT_SECRET_KEY
    user_agent = USER_NAME

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_reddit_data(subreddit_name, keyword, sort_by="hot", limit=100):
    """
    Fetches Reddit posts and comments based on the subreddit and keyword.

    Parameters:
        subreddit_name (str): Name of the subreddit to search.
        keyword (str): Keyword to search for.
        sort_by (str): Sorting method ("hot", "new", "top", etc.).
        limit (int): Maximum number of posts to fetch.

    Returns:
        dict: A dictionary containing posts and their details.
    """
    subreddit = reddit.subreddit(subreddit_name)
    print(f"Searching '{subreddit_name}' for keyword '{keyword}' sorted by '{sort_by}'...\n")
    result_data = {}

    submissions = subreddit.search(keyword, sort=sort_by, limit=limit)
    
    for idx, submission in enumerate(submissions):
        print(f"{len(list(submissions))} posts...")
            
        time.sleep(0.05)
        post_data = {
            "title": submission.title,
            "text": submission.selftext,
            "author": submission.author.name if submission.author else "Unknown",
            "created_utc": submission.created_utc,
            "score": submission.score,
            "comments": []
        }

        # Fetch top-level comments
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comment_data = {
                "author": comment.author.name if comment.author else "Unknown",
                "text": comment.body,
                "created_utc": comment.created_utc,
                "score": comment.score
            }
            post_data["comments"].append(comment_data)

        # Use the submission ID as the key
        result_data[submission.id] = post_data

    return result_data


def save_results_to_json(data, subreddit_name, keyword):
    """
    Saves the data to a JSON file.

    Parameters:
        data (dict): The data to save.
        subreddit_name (str): Name of the subreddit.
        keyword (str): Keyword used in the search.
    """
    output_file = f"done/{subreddit_name}_{keyword.replace(' ', '_')}_results.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Results saved to {output_file}")


def main():
    """
    Main function to fetch data from multiple subreddits and keywords and save results to JSON files.
    """
    # List of subreddits and keywords
    # List of subreddits
    subreddits = ["PanicDisorder", "PanicAttack", "Anxiety", "MentalHealth"]

    # List of keywords
    keywords = [
        'faint',
        'collapse',
        'go crazy'
    ]


        # "panic",
        # 'heart attack',
        # "heart racing",
        # "trouble breathing",
        # "feeling dizzy",
        # "chest",
        # "feeling out of control",
        # "fear of dying",
        # "shaking or trembling",
        # "sudden fear",
        # "numbness or tingling",
        # "overwhelming fear",
        # "feeling detached",
        # "losing control",
        # "feeling trapped",
        
    # Iterate through subreddits and keywords
    for subreddit_name in subreddits:
        for keyword in keywords:
            data = fetch_reddit_data(subreddit_name, keyword, sort_by="hot", limit=10000)
            save_results_to_json(data, subreddit_name, keyword)


if __name__ == "__main__":
    main()
