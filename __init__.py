"""
Fetches json data, counts user posts, unique post titles, checks user proximity\n
:imports requests, pandas, geo
"""
import requests
import pandas as pd
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
    Returns dataframes: posts, users in a tuple
    """
    posts = fetch_json('https://jsonplaceholder.typicode.com/posts')
    users = fetch_json('https://jsonplaceholder.typicode.com/users')
    return make_dataframe(posts), make_dataframe(users)

def get_user_post_count(posts, users):
    posts_per_user = posts.groupby('userId').count().iloc[:,0]
    posts_per_user.name = 'posts_count'
    users = pd.concat([users, posts_per_user], axis=1)
    msg = lambda x: "{0} napisał(a) {1} postów".format(x['username'], x['posts_count'])
    return [msg(users.iloc[i,:]) for i in range(0,len(users))]

def get_unique_post_titles(posts):
    pass

def get_nearest_users(users):
    pass

def main():
    posts, users = get_data()
    print(get_user_post_count(posts, users))
    print(get_unique_post_titles(posts))
    print(get_nearest_users(users))

if __name__ == "__main__":
    main()
