import requests

def fetch_json(url):
    response = requests.get(url)
    return response.json()

def main():
    posts = fetch_json('https://jsonplaceholder.typicode.com/posts')
    users = fetch_json('https://jsonplaceholder.typicode.com/users')
    print((len(posts), len(users)))

if __name__ == "__main__":
    main()
