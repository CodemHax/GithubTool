# GitHub CLI Tool

A simple command-line tool to fetch and display GitHub user information and repositories.

## Features

- Search for GitHub users by username
- View user profile information (ID, name, followers, following, public repos)
- Browse user repositories with details (stars, forks, description)
- View detailed repository information including clone URLs
- Local caching to reduce API calls

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CodemHax/GithubTool.git
cd GithubTool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the tool:
```bash
python main.py
```

Then follow the prompts to:
1. Enter a GitHub username to search
2. View user information
3. Browse their repositories
4. Get detailed repo info including download/clone URLs

## Requirements

- Python 3.x
- requests library

