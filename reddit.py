import praw
import statics
import persistor as db


# THINGS TO DO
# TODO filter fuer r/all und r/popular
# TODO passen exceptions so? bessere setzung? fehlen exceptions?
# TODO post production package (value 0 edges herausnehmen, eigenverweise herausnehmen, ...)


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


# RECURSIVELY SEARCH SUBS
def search_subs(starting_subs: []):
    reddit = reddit_connect()
    next_subs = []

    for start_sub in starting_subs:
        try:
            print('---')
            print(start_sub)
            subreddit = reddit.subreddit(start_sub).hot(limit=statics.POST_LIMIT)
        except:
            break

        try:
            for submission in subreddit:
                submission.comments.replace_more(limit=None)
                comment_queue = submission.comments[:]
                while comment_queue:
                    comment = comment_queue.pop(0)
                    refs = [sub.lower() for sub in comment.body.split() if sub.startswith('r/')]
                    for ref in refs:
                        # add names of references to next_subs
                        if ref[2:] not in next_subs and ref[2:] not in starting_subs:
                            next_subs.append(ref[2:])

                        # persist as graph
                        source = str(submission.subreddit).lower()
                        target = ref[2:].lower()
                        db.connect(source, target)
                    comment_queue.extend(comment.replies)
        except:
            break

    return next_subs


if __name__ == '__main__':
    # PREPARE PERSISTENCE
    db.write_graph(db.create_new_graph())

    # START ALGORITHM
    start = ['popular']
    for i in range(0, statics.DEPTH):
        print('***', i, '***')
        start = search_subs(start)
        print(start)
