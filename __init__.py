"""
Allows to fetch and process json from database web api.\n
:imports requests, pandas, math
"""
import requests
import pandas as pd

def fetch_json(url):
    """
    Sends a get request and returns parsed json\n
    :raises ValueError: invalid json received
    """
    response = requests.get(url)
    return response.json()

def make_dataframe(data):
    return pd.DataFrame(data).set_index(['id'])

def main():
    posts = fetch_json('https://jsonplaceholder.typicode.com/posts')
    users = fetch_json('https://jsonplaceholder.typicode.com/users')

    posts = make_dataframe(posts)
    users = make_dataframe(users)

if __name__ == "__main__":
    main()
