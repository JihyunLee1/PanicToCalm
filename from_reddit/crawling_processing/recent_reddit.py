import praw
import time
import json
import datetime

def fetch_reddit_posts(reddit_name):
    # Replace with your Reddit API credentials
    client_id = FROM_REDDIT_CLIENT_ID
    client_secret = FROM_REDDIT_CLIENT_SECRET_KEY
    user_agent = USER_NAME

    # Initialize the Reddit client
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    subreddit = reddit.subreddit(reddit_name)  # Target subreddit

    save_list = {}
    idx = 0

    # Fetch recent posts (limit 1000)
    for submission in subreddit.new(limit=1000):
        idx += 1
        print(f"Fetching post {idx}/1000")
        post_id = submission.id
        save_list[post_id] = {
            "title": submission.title,
            "text": submission.selftext,
            "author": str(submission.author),
            "created_utc": submission.created_utc,
            "score": submission.score,
            "comments": []
        }

        # Fetch comments for the submission
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            save_list[post_id]["comments"].append({
                "author": str(comment.author),
                "text": comment.body,
                "created_utc": comment.created_utc,
                "score": comment.score
            })

            time.sleep(0.5)

    # Save any remaining posts after the loop
    if save_list:
        with open(f'./done/{reddit_name}_recent.json', 'a') as f:
            json.dump(save_list, f, indent=4)
        print("Saved remaining posts to file.")

if __name__ == "__main__":
    
    reddit_names = ["PanicAttack", "panicdisorder"]
    for reddit_name in reddit_names:
        fetch_reddit_posts(reddit_name)