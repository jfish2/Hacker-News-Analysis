import requests
from plotly.graph_objs import Bar
from plotly import offline
from operator import itemgetter

url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print("Status code", r.status_code)

submission_ids = r.json()
submission_dicts = []
i = 0
while i < 30:
    url = ('https://hacker-news.firebaseio.com/v0/item/' + str(submission_ids[i]) + '.json')
    submission_r = requests.get(url)
    i+=1
    print("Analyzing articles...", i)
    response_dict = submission_r.json()

    submission_dict = {
        'title': response_dict['title'],
        'link': 'http://news.ycombinator.com/item?id=' + str(submission_ids[i]),
        'comments': response_dict.get('descendents', 0)
    }

    submission_dicts.append(submission_dict)


submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)


for submission_dict in submission_dicts:
    print('\nTitle:', submission_dict['title'])
    print('Discussion link:', submission_dict['link'])
    print('Comments:', submission_dict['comments'])

titles, num_comments, discn_links = [], [], []
for sd in submission_dicts:
    title = sd['title']
    hn_link = sd['link']
    discn_link = f"<a href='{hn_link}'>{title[:15]}...</a>"

    titles.append(title)
    num_comments.append(sd['comments'])
    discn_links.append(discn_link)

# Make visualization.
data = [{
    'type': 'bar',
    'x': discn_links,
    'y': num_comments,
    'hovertext': titles,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
}]

my_layout = {
    'title': 'Most-discussed articles on Hacker News',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Article',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': 'Number of Comments',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },

}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='hn_discussions.html')
