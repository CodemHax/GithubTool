import requests
import json

GITHUB_API_BASE = "https://api.github.com"
CACHE_FILE = "cache.json"
DEFAULT_TIMEOUT = 5


def save_to_cache(data, filename=CACHE_FILE):
    with open(filename, "w") as f:
        json.dump(data, f)


def load_from_cache(filename=CACHE_FILE):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_user_repos(username):
    cached = load_from_cache()
    cache_key = f"{username}repos"

    if cache_key in cached:
        return cached[cache_key]
    response = requests.get(f"{GITHUB_API_BASE}/users/{username}/repos", timeout=DEFAULT_TIMEOUT)
    repos = response.json()
    cached[cache_key] = repos
    save_to_cache(cached)
    return repos

def get_user_info():
    username = input("Enter your username: ")
    cached = load_from_cache()
    if username in cached:
        data = cached[username]

    else:
        try:
            response = requests.get(f"{GITHUB_API_BASE}/users/{username}", timeout=DEFAULT_TIMEOUT)
        except requests.exceptions.Timeout:
            print("Timeout error. Please try again later.")
            return
        except requests.exceptions.ConnectionError:
            print("Connection error. Check your internet connection.")
            return
        if response.status_code != 200:
            print("User not found!")
            get_user_info()
            return
        data = response.json()
        cached[username] = data
        save_to_cache(cached)

    print(f"ID: {data['id'] or 'Not available'}")
    print(f"Name: {data['name'] or 'Not available'}")
    print(f"Profile URL: {data['html_url'] or 'Not available'}")
    print(f"Followers: {data['followers'] or 'Not available'} ")
    print(f"Following: {data['following'] or 'Not available'}")
    print(f"Public Repos: {data['public_repos'] or 'Not available'}")
    print(f"Created At: {data['created_at'] or 'Not available'}")

    while True:
        print("What would you like to do?")
        print("1. Search another user")
        print("2. View repositories for this user")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            return
        elif choice == "2":
            repos = get_user_repos(username)
            if repos:
                print(f"\nRepositories for {username}:")
                for i, repo in enumerate(repos, 1):
                    print(f"{i}. {repo['name']} - {repo['description'] or 'No description'}")
                    print(f"   Stars: {repo['stargazers_count']} | Forks: {repo['forks_count']}")
                    print(f"   URL: {repo['html_url']}")

                while True:
                    print("\nEnter repo number for detailed info (or 0 to go back):")
                    try:
                        repo_choice = int(input("Repo number: ").strip())
                        if repo_choice == 0:
                            break
                        if 1 <= repo_choice <= len(repos):
                            selected_repo = repos[repo_choice - 1]
                            print(f"Repository: {selected_repo['name']}")
                            print(f"Description: {selected_repo['description'] or 'No description'}")
                            print(f"Stars: {selected_repo['stargazers_count']}")
                            print(f"Created: {selected_repo['created_at']}")
                            print(f"Last Updated: {selected_repo['updated_at']}")
                            print(f"\nRepository URL: {selected_repo['html_url']}")
                            print(f"Download ZIP: {selected_repo['html_url']}/archive/refs/heads/{selected_repo['default_branch']}.zip")
                            print(f"Clone URL: {selected_repo['clone_url']}")
                        else:
                            print("Invalid repo number. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                print("No repositories found.")
        elif choice == "3":
            print("bye")
            exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    while True:
        try:
            get_user_info()
        except Exception as e:
            print(f"An error occurred: {e}")


