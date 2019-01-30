import re
import os
import praw

SUB_REDDIT = ['femalefashionadvice','malefashionadvice','ABraThatFits']
LIMIT = 30
SEARCH = [' ']
MESSAGE = "For anyone here that likes amazing dresses, lingerie or modern coats, check out https://www.elenalda.com/ . I recently bought a dress for my girlfriend and she loved it! ^.^"

if __name__ == '__main__':

    reddit = praw.Reddit('FinBot')

    # Create a list
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []

    # Or load the list of posts we have replied to
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

    replies = 0
    for s in SUB_REDDIT:
        print(' ----------------------------- /r/' + s + ' -----------------------------')
        subreddit = reddit.subreddit(s)
        for submission in subreddit.top(limit=LIMIT):

            if submission.id not in posts_replied_to:

                # Not case sensitive
                for phrase in SEARCH:

                    if re.search(phrase, submission.title, re.IGNORECASE):
                        # Reply
                        try:
                            submission.reply(MESSAGE)
                            print("Bot replying to : ", submission.title)
                            replies += 1
                            # Store id in list
                            posts_replied_to.append(submission.id)
                        except:
                            print('Bot could not reply to post: ' + submission.title)



    # Write updated list to file
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

    print('Bot replied to ' + str(replies) + ' posts!')
