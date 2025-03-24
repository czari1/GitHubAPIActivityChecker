# GitHub Activity Checker

This project fetches and displays recent GitHub activity for a specified user. It uses the GitHub API to retrieve events and formats them for easy reading.

## Files

- `main.py`: The main script that handles command line arguments and calls the utility functions.
- `utilities.py`: Contains utility functions for fetching and formatting GitHub activity.

## Requirements

- Python 3.6+
- `requests` library

You can install the required library using pip:

```sh
pip install requests
```

## Usage

Run the script with the following command:

```sh
python main.py <username> [-d DAYS] [-l LIMIT]
```

- `<username>`: GitHub username to fetch activity for.
- `-d, --days`: Number of days to fetch activity for (default: 30, 0 for all available).
- `-l, --limit`: Limit the number of events to display (default: 10, 0 for all available).

### Examples

Fetch activity for user `octocat` for the last 30 days (default):

```sh
python main.py octocat
```

Fetch activity for user `octocat` for the last 7 days:

```sh
python main.py octocat -d 7
```

Fetch all available activity for user `octocat`:

```sh
python main.py octocat -d 0
```

Fetch activity for user `octocat` and display only the last 5 events:

```sh
python main.py octocat -l 5
```

## Functions

### `fetch_github_activity(username: str, days: int = 30)`

Fetches GitHub activity for a user.

- `username`: GitHub username.
- `days`: Number of days to fetch activity for.

Returns a list of recent GitHub activity events.

### `format_activity(event)`

Formats a GitHub activity event into readable text.

- `event`: A GitHub activity event.

Returns a formatted string representing the event.

## License

This project is licensed under the MIT License.