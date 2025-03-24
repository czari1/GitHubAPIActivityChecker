import argparse
from utilities import fetch_github_activity, format_activity

def main():
    """Main function with command line arguments for time frame and limit"""
    parser = argparse.ArgumentParser(description="Fetch recent GitHub activity for a user")
    parser.add_argument("username", help="Github username to fetch activity for")
    parser.add_argument("-d", "--days", type=int, default=30, 
                        help="Number of days to fetch activity for(default: 30, o for all available)")
    parser.add_argument("-l", "--limit", type=int, default=10,
                        help="Limit the number of events to display (default: 10, 0 for all avalailable)")
    
    args = parser.parse_args()

    print(f"Fetching GitHub activity for {args.username}...")

    if args.days > 0:
        print(f"Fetching activity for last {args.days} days")
    elif args.days == 0:
        print("Fetching all available activity")
    else:
        print("Invalid value for days. Please provide a positive integer")
    
    events = fetch_github_activity(args.username, args.days)

    if events:
        count = min(len(events),args.limit)
        print(f"Displaying {count} out of {len(events)} events")

        for i,event in enumerate(events):
            if i >= args.limit:
                break
            print(format_activity(event))
        if len(events) > args.limit:
            print(f"Showing {args.limit} out of {len(events)} events. Use --limit to display more")
    else:
        print("No activity found")

if __name__ == "__main__":
    main()