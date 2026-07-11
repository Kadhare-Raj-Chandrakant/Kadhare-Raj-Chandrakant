#!/usr/bin/env python3
"""
GitHub API module for fetching contribution data
"""

import requests

def fetch_contributions(username, token):
    query = """
    query($username: String!) {
        user(login: $username) {
            contributionsCollection {
                contributionCalendar {
                    weeks {
                        contributionDays {
                            contributionCount
                            date
                            color
                        }
                    }
                }
            }
        }
    }
    """

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'https://api.github.com/graphql',
        json={'query': query, 'variables': {'username': username}},
        headers=headers
    )

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return None

    data = response.json()

    if 'errors' in data:
        print(f"GraphQL errors: {data['errors']}")
        return None

    return data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']

def process_contribution_data(weeks_data):
    grid = []
    max_contributions = 0

    for week in weeks_data:
        week_data = []
        for day in week['contributionDays']:
            count = day['contributionCount']
            max_contributions = max(max_contributions, count)
            week_data.append({
                'count': count,
                'date': day['date'],
                'level': min(4, count // max(1, max_contributions // 4)) if max_contributions > 0 else 0
            })
        grid.append(week_data)

    return grid, max_contributions
