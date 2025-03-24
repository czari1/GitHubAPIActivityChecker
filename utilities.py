import requests
import datetime

def fetch_github_activity(username: str, days: int = 30):
    """
    Fetch GitHun activity for a user

    Args:
    username (str): GitHub username
    days (int): Number of days to fetch activity for

    Returns:
    List: A list of recent GitHub activity events
    """
    url = f"https://api.github.com/users/{username}/events"

    params = {"per_page": 100,}

    try:
        headers = {'User-Agent': 'Github-Activity-Fetcher'}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            events = response.json()
            if days > 0:
                cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
                filtered_events = []
                for event in events:
                    event_date = datetime.datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    event_timestamp = event_date.timestamp()
                    if event_timestamp >= cutoff_date.timestamp():
                        filtered_events.append(event)
                return filtered_events
            else:
                return events
        elif response.status_code == 404:
            print (f"Error: User {username} not found")
        else:
            print(f"Error: HTTP error occured: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: An unexpected error occured: {e}")
        return None

def format_activity(event):
    """Format Githuhb activity event into readable text"""
    event_type = event['type']
    repo_name = event['repo']['name']

    event_date = datetime.datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    formated_date = event_date.strftime('%Y-%m-%d %H:%M:%S')

    activity_text = ""
    
    if event_type == 'PushEvent':
        try:
            commits_count = len(event['payload']['commits'])
            activity_text = f"Pushed {commits_count} commits to {repo_name}"
        except:
            activity_text = f"Pushed to {repo_name}"
    elif event_type == 'CreateEvent':
        try:
            ref_type = event['payload']['ref_type']
            activity_text = f"Created {ref_type} {repo_name}"
        except:
            activity_text = f"Created something in{repo_name}"
        
    elif event_type == 'IssuesEvent':
        try:
            action = event['payload']['action']
            issue_number = event['payload']['issue']['number']
            activity_text = f"{action.capitalize()} issue #{issue_number} in {repo_name}"
        except:
            activity_text = f"Acted on an issue in {repo_name}"
    
    elif event_type == 'WatchEvent':
        activity_text = f"Starred {repo_name}"
    
    elif event_type == 'ForkEvent':
        activity_text = f"Forked {repo_name}"
    
    else:
        activity_text = f"{event_type} on {repo_name}"

    return f"{formated_date}: {activity_text}"
