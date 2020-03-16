"""
Fetches json data, counts user posts, unique post titles, checks user proximity\n
:imports requests, pandas, math, unittest
"""
import requests
import pandas as pd
from solvers import MatrixSolver
from geo import Geo

def fetch_json(url):
    """
    Sends a get request and returns parsed json\n
    :raises ValueError: invalid json received
    """
    response = requests.get(url)
    return response.json()

def make_dataframe(data):
    """
    Create dataframe with index set at id column
    """
    return pd.DataFrame(data).set_index(['id'])

def get_data():
    """
    Returns tuple of posts,users dataframes
    """
    posts = fetch_json('https://jsonplaceholder.typicode.com/posts')
    users = fetch_json('https://jsonplaceholder.typicode.com/users')
    return make_dataframe(posts), make_dataframe(users)

def get_user_post_count(posts, users):
    """
    Returns list of strings with usernames and their post counts
    """
    posts_per_user = posts.loc[:,'userId'].value_counts()
    posts_per_user.name = 'posts_count'
    users = pd.concat([users, posts_per_user], axis=1)
    msg = lambda x: "{0} napisał(a) {1} postów".format(x['username'], x['posts_count'])
    return [msg(users.iloc[i,:]) for i in range(0,len(users))]

def get_duplicated_titles(posts):
    """
    Returns duplicated titles in posts
    """
    is_dupl = posts.loc[:,'title'].duplicated()
    return posts.loc[is_dupl, 'title'].to_list()

def get_nearest_users(users):
    """
    Returns dict mapping user id to its closest user id
    """
    address = users.columns.get_loc('address')
    geoloc = users.iloc[:, address]
    f = lambda i,label: float(geoloc[i]['geo'][label])
    coords = [{'id':i, 'geo':Geo(f(i,'lat'), f(i,'lng'))} for i in geoloc.index]

    solver = MatrixSolver(lambda x,y: x['geo'].distance(y['geo']))
    nearest = solver.solve(coords).min()

    return {coords[i]['id']:coords[nearest[i]]['id'] for i in range(0,len(nearest))}

def main():
    posts, users = get_data()
    print("Users post count:")
    print(get_user_post_count(posts, users))
    print("Duplicated post titles:")
    print(get_duplicated_titles(posts))
    print("Nearest user:")
    print(get_nearest_users(users))

if __name__ == "__main__":
    main()
