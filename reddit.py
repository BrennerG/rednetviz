import praw
import statics


# ENABLE REDDIT DEV CONNECTION
def reddit_connect():
    reddit = praw.Reddit(client_id=statics.reddit_data['client_id'],
                         client_secret=statics.reddit_data['client_secret'],
                         user_agent=statics.reddit_data['user_agent'])
    return reddit


# GET STARTING POINT eg r/popular and extract all subreddits
def starting_posts():
    reddit = reddit_connect()
    for submission in reddit.subreddit('popular').hot(limit=10):
        print('---')
        print(submission.subreddit)
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]
        while comment_queue:
            comment = comment_queue.pop(0)
            refs = [sub.lower() for sub in comment.body.split() if sub.startswith('r/')]
            if refs:
                print(refs)
            comment_queue.extend(comment.replies)


def search_subs():
    pass
    return None


if __name__ == '__main__':
    starting_posts()
