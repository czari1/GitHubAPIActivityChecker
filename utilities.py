import requests
import datetime

def fetch_github_activity(username: str, days: int = 30, token: str = None):
    """
    Fetch GitHub activity for a user

    Args:
    username (str): GitHub username
    days (int): Number of days to fetch activity for

    Returns:
    List: A list of recent GitHub activity events
    """
    url = f"https://api.github.com/users/{username}/events"
    params = {"per_page": 100,}
    headers = {'User-Agent': 'Github-Activity-Fetcher'}
    all_events = []
    
    if token:
        headers['Authorization'] = f'token {token}'

    try:
        while url:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                remaining_requests = response.headers.get('X-RateLimit-Remaining', 'Unknown')
                print(f"API requests remaining: {remaining_requests}")

                events = response.json()
                all_events.extend(events)
                # Check if there is a next page
                if 'next' in response.links:
                    url = response.links['next']['url']
                else:
                    break
            elif response.status_code == 404:
                print(f"Error: User {username} not found")
                return None
            elif response.status_code == 403:
                print("Error: API rate limit exceeded")
                print("Wait for some time or provide a personal access token to increase the limit")
                return None
            else:
                print(f"Error: HTTP error occurred: {response.status_code}")
                return None
        
        print(f"Total events fetched: {len(all_events)}")

        if days > 0:
            cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
            filtered_events = []
            for event in all_events:
                event_date = datetime.datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
                if event_date >= cutoff_date:
                    filtered_events.append(event)
                    
            return filtered_events
        else:
            return all_events
        
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None

def format_activity(event):
    """Format Github activity event into readable text"""
    event_type = event['type']
    repo_name = event['repo']['name']
    event_date = datetime.datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    formated_date = event_date.strftime('%Y-%m-%d %H:%M:%S')

    activity_text = ""
    
    if event_type == 'PushEvent':
        try:
            commits_count = len(event['payload']['commits'])
            activity_text = f"Pushed {commits_count} commits to {repo_name}"
        except KeyError:
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
        except KeyError:
            activity_text = f"Acted on an issue in {repo_name}"
    
    elif event_type == 'WatchEvent':
        activity_text = f"Starred {repo_name}"
    
    elif event_type == 'ForkEvent':
        activity_text = f"Forked {repo_name}"
    
    elif event_type == 'PullRequestEvent':
        try:
            action = event ['payload']['action']
            pr_number = event['payload']['pull_request']['number']
            activity_text = f"{action.capitalize()} pull request #{pr_number} in {repo_name}"
        except KeyError:
            activity_text = f"Acted on a pull request in {repo_name}"

    elif event_type =='ReleaseEvent':
        try:
            action = event['payload']['action']
            release_name = event['payload']['release']['name']
            activity_text = f"{action.capitalize()} release {release_name} in {repo_name}"
        except KeyError:
            activity_text = f"Acted on a release in {repo_name}"
    elif event_type == 'PublicEvent':
        activity_text = f"Made {repo_name} public"

    elif event_type == 'DeleteEvent':
        try:
            ref_type = event['payload']['ref_type']
            activity_text = f"Deleted {ref_type} {repo_name}"
        except:
            activity_text = f"Deleted something in {repo_name}"

    else:
        activity_text = f"{event_type} on {repo_name}"

    return f"{formated_date}: {activity_text}"
