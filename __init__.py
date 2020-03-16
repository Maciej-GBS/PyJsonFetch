"""
Fetches json data, counts user posts, unique post titles, checks user proximity\n
:imports requests, pandas, math, unittest
"""
from implementation import *

def main():
    posts, users = get_data()
    print("Users post count:")
    print(get_user_post_count(posts, users))
    print("\nDuplicated post titles:")
    print(get_duplicated_titles(posts))
    print("\nNearest user:")
    print(get_nearest_users(users))

if __name__ == "__main__":
    main()
