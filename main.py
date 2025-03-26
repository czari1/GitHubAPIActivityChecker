import argparse
from utilities import fetch_github_activity, format_activity
from plots import plot_activity_overview, generate_activity_report, export_events_to_csv

def main():
    """Main function with command line arguments for time frame and limit"""
    parser = argparse.ArgumentParser(description="Fetch recent GitHub activity for a user")
    parser.add_argument("username", help="Github username to fetch activity for")
    parser.add_argument("-d", "--days", type=int, default=30, 
                        help="Number of days to fetch activity for(default: 30, o for all available)")
    parser.add_argument("-l", "--limit", type=int, default=10,
                        help="Limit the number of events to display (default: 10, 0 for all avalailable)")
    parser.add_argument("--plot", action="store_true", help="Generate plots for activity overview")
    parser.add_argument("--report", action="store_true", help="Generate activity report")
    parser.add_argument("--export", action="store_true", help="Export events to CSV file")
    
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

        if args.plot:
            plot_activity_overview(events)

        if args.report:
            report = generate_activity_report(events, args.username)
            print("\n" +report)

        if args.export:
            export_events_to_csv(events, args.username)

    else:
        print("No activity found")

if __name__ == "__main__":
    main()