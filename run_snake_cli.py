#!/usr/bin/env python3
"""
CLI for the GitHub Contribution Snake Generator
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.append(str(Path(__file__).parent))

from scripts.snake_generator import ContributionSnake

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

HEADER = f"""
{BOLD}{CYAN}
╔════════════════════════════════════════════════════════╗
║           GitHub Contribution Snake Generator          ║
╚════════════════════════════════════════════════════════╝{RESET}
"""

def run_snake_cli():
    print(HEADER)

    username = os.getenv('GITHUB_USERNAME')
    token = os.getenv('GITHUB_TOKEN')

    if not username or not token:
        print(f"{YELLOW}Please set GITHUB_USERNAME and GITHUB_TOKEN in .env{RESET}")
        return

    output_dir = Path('dist')
    output_dir.mkdir(exist_ok=True)

    try:
        print(f"{CYAN}Generating snake for: {BOLD}{username}{RESET}")
        snake = ContributionSnake(username, token)
        success = snake.generate_all(output_dir)

        if success:
            print(f"{GREEN}{BOLD}Snake generation complete!{RESET}")
        else:
            print(f"{RED}{BOLD}Snake generation failed!{RESET}")

    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

if __name__ == "__main__":
    run_snake_cli()
