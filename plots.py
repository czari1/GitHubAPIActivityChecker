import matplotlib.pyplot as plt
import pandas as pd
import datetime
from typing import List, Dict
import os



def plot_activity_overview(events: List[Dict]):
    """
    Create visualization of Github activity

    Args:
    events (List[Dict]): List of Github activity events

    Generate multiple plots
    1. Activity distribution by type
    2. Commits over time
    3. Repository activity breakdown
    """

    if not events: 
        print("No activity found")
        return
    
    df = pd.DataFrame(events)

    df['created_at'] = pd.to_datetime(df['created_at'])
    
    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    event_counts = df['type'].value_counts()
    event_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, 
                      explode=[0.1 if i == 0 else 0 for i in range(len(event_counts))],
                      wedgeprops={'edgecolor': 'white', 'linewidth': 1},)
    plt.title('GitHub Event Types')
    
    # Plot 2: Events Over Time
    plt.subplot(132)
    daily_events = df.groupby(df['created_at'].dt.date).size()
    daily_events.plot(kind='line', marker='o')
    plt.title('Daily Activity')
    plt.xlabel('Date')
    plt.ylabel('Number of Events')
    plt.xticks(rotation=45)
    
    # Plot 3: Repository Activity
    plt.subplot(133)
    repo_counts = df['repo'].apply(lambda x: x['name']).value_counts().head(10)
    repo_counts.plot(kind='bar')
    plt.title('Top 10 Active Repositories')
    plt.xlabel('Repository')
    plt.ylabel('Event Count')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()


def generate_activity_report(events: List[Dict],username: str):
    """
    Generate Github activity report

    Args:
    Events (List[Dict]): List of Github activity events
    username (str): Github username

    Returns:
    str: Formatted Github activity report
    """

    if not events:
        return "No activity found"
    
    df = pd.DataFrame(events)
    df['created_at'] = pd.to_datetime(df['created_at'])

    report = f"Github activity report for {username}\n"
    report += "=" * 40 + "\n\n"

    report += f'Total events: {len(events)}\n'

    event_breakdown = df["type"].value_counts()
    report += "\nEvent breakdown:\n"
    for event_type, count in event_breakdown.items():
        report += f"- {event_type}: {count}\n events ( {count/len(events)*100:.1f}% )\n"

    top_repos = df['repo'].value_counts().head(5)
    report += f"Top 5 most active repositories:\n"
    for repo, count in top_repos.items():
        report += f"- {repo}: {count} events\n"

    first_activity = df['created_at'].min()
    last_activity = df['created_at'].max()
    report += f"\nActivity span : {first_activity} to {last_activity}\n"

    return report

def export_events_to_csv(events: List[Dict], username: str):
    """
    Export Github activity events to a CSV file

    Args:
    events (List[Dict]): List of Github activity events
    username (str): Github username
    filename (str): Name of the CSV file to export

    Returns:
    str: Path to exported CSV file
    """

    if not events:
        print("No activity found")
        return
    
    try:
        # Utworzenie folderu CSV, jeśli nie istnieje
        csv_folder = 'github_activity_csv'
        os.makedirs(csv_folder, exist_ok=True)

        # Stała nazwa pliku dla danego użytkownika
        filename = os.path.join(csv_folder, 
                                f"{username}_github_activity_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv")

        # Przygotowanie DataFrame
        df = pd.DataFrame(events)

        # Bezpieczne wyodrębnienie nazw repozytoriów
        df['repo_name'] = df['repo'].apply(lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown')

        # Przygotowanie kolumn do eksportu
        columns_to_export = [
            'type', 
            'created_at', 
            'repo_name'
        ]

        # Opcjonalnie dodaj więcej kolumn payload
        try:
            df['payload_action'] = df['payload'].apply(lambda x: x.get('action', 'N/A') if isinstance(x, dict) else 'N/A')
            columns_to_export.append('payload_action')
        except Exception as e:
            print(f"Warning: Could not extract payload details: {e}")

        # Sprawdzenie, czy plik już istnieje
        try:
            existing_df = pd.read_csv(filename)
            # Usuwanie duplikatów przed dołączeniem nowych danych
            df = pd.concat([existing_df, df[columns_to_export]]).drop_duplicates()
        except FileNotFoundError:
            # Jeśli plik nie istnieje, użyj bieżącego DataFrame
            pass

        # Eksport do CSV, nadpisanie lub utworzenie nowego pliku
        df[columns_to_export].to_csv(filename, index=False, encoding='utf-8')

        print(f"Github activity exported successfully to {filename}")
        return filename

    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return None


    