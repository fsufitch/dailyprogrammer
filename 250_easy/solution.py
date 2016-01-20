from datetime import datetime, timedelta
import praw, warnings

warnings.filterwarnings('ignore') # XXX: praw, pls ಠ_ಠ

def get_monday_of_week(t):
    days_after_monday = t.weekday()
    monday_dt = t - timedelta(days=days_after_monday)
    return monday_dt.date()

reddit = praw.Reddit(user_agent='/r/dailyprogrammer [250 Easy]')
r_dp = reddit.get_subreddit('dailyprogrammer')

weeks = {}

for post in r_dp.get_new(limit=None): # Set to 10 for debugging
    post_time = datetime.utcfromtimestamp(int(post.created_utc))
    monday = get_monday_of_week(post_time).toordinal()

    weeks[monday] = weeks.get(monday, {
        'easy': [], 'intermediate': [], 'hard': [], 'other': [],
    })

    lowertitle = post.title.lower()
    if '[easy]' in lowertitle:
        weeks[monday]['easy'].append(post)
    elif '[intermediate]' in lowertitle:
        weeks[monday]['intermediate'].append(post)
    elif ('[hard]' in lowertitle) or ('[difficult]' in lowertitle):
        weeks[monday]['hard'].append(post)
    else:
        weeks[monday]['other'].append(post)

print("Easy | Intermediate | Hard | Weekly / Bonus / Misc")
print("-----|--------------|------|----------------------")

row_template = "|{easy}|{intermediate}|{hard}|{other}|"
link_template = "[{text}]({url})"
empty_link = "[]()"
empty_dash = "**-**"

for monday, week in sorted(list(weeks.items()), reverse=True):
    easy_links = [link_template.format(text=post.title, url=post.short_link)
                  for post in week['easy']]
    easy_text = '; '.join(easy_links) or empty_link

    int_links = [link_template.format(text=post.title, url=post.short_link)
                  for post in week['intermediate']]
    int_text = '; '.join(int_links) or empty_link
    
    hard_links = [link_template.format(text=post.title, url=post.short_link)
                  for post in week['hard']]
    hard_text = '; '.join(hard_links) or empty_link
    
    other_links = [link_template.format(text=post.title, url=post.short_link)
                  for post in week['other']]
    other_text = '; '.join(other_links) or empty_dash

    row = row_template.format(easy=easy_text, intermediate=int_text,
                              hard=hard_text, other=other_text)
    print(row)

