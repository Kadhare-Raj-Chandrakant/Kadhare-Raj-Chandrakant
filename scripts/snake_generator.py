#!/usr/bin/env python3
"""
Main snake generator module
"""

import sys
from pathlib import Path
from .config import validate_config, get_github_username, get_github_token
from .github_api import fetch_contributions, process_contribution_data
from .snake_path import create_snake_path
from .svg_generator import generate_svg_animation
from .gif_generator import generate_gif_animation

class ContributionSnake:
    def __init__(self, username=None, token=None):
        self.username = username or get_github_username()
        self.token = token or get_github_token()

        if not self.username or not self.token:
            raise ValueError("GitHub username and token are required")

    def generate_all(self, output_dir="dist"):
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        weeks_data = fetch_contributions(self.username, self.token)

        if not weeks_data:
            print("Failed to fetch contribution data")
            return False

        grid, max_contributions = process_contribution_data(weeks_data)
        print(f"Processed contribution grid: {len(grid)} weeks, max: {max_contributions}")

        snake_path = create_snake_path(grid)

        if not snake_path:
            print("Failed to create snake path")
            return False

        print("Generating SVG animations...")
        generate_svg_animation(grid, snake_path, output_path / 'github-contribution-grid-snake.svg', dark_mode=False)
        generate_svg_animation(grid, snake_path, output_path / 'github-contribution-grid-snake-dark.svg', dark_mode=True)

        print("Generating GIF animations...")
        generate_gif_animation(grid, snake_path, output_path / 'github-contribution-grid-snake.gif', dark_mode=True)
        generate_gif_animation(grid, snake_path, output_path / 'github-contribution-grid-snake-light.gif', dark_mode=False)

        print("Snake generation complete!")
        return True

def main():
    if not validate_config():
        sys.exit(1)

    snake = ContributionSnake()
    success = snake.generate_all()

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
