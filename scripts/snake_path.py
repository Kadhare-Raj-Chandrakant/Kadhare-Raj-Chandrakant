#!/usr/bin/env python3
"""
Snake path generation module
"""

import random

def create_snake_path(grid):
    path = []
    if not grid:
        return path

    rows = len(grid[0]) if grid else 0
    cols = len(grid)

    contributions = []
    empty_spaces = []

    for col in range(cols):
        for row in range(min(rows, len(grid[col]))):
            pos = (col, row, grid[col][row]['count'])
            if grid[col][row]['count'] > 0:
                contributions.append(pos)
            else:
                empty_spaces.append(pos)

    contributions.sort(key=lambda x: x[2], reverse=True)

    start_pos = None
    for col in range(min(3, cols)):
        for row in range(min(rows, len(grid[col]))):
            start_pos = (col, row, grid[col][row]['count'])
            break
        if start_pos:
            break

    if not start_pos:
        if cols > 0 and rows > 0:
            start_pos = (0, 0, grid[0][0]['count'] if len(grid[0]) > 0 else 0)
        else:
            start_pos = (0, 0, 0)

    visited = set()
    path.append(start_pos)
    visited.add((start_pos[0], start_pos[1]))

    def get_valid_moves(col, row):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dc, dr in directions:
            new_col, new_row = col + dc, row + dr
            if (0 <= new_col < cols and
                0 <= new_row < rows and
                new_row < len(grid[new_col]) and
                (new_col, new_row) not in visited):
                moves.append((new_col, new_row, grid[new_col][new_row]['count']))
        return moves

    def move_towards_target(current_col, current_row, target_col, target_row):
        if current_col != target_col:
            if current_col < target_col:
                next_col, next_row = current_col + 1, current_row
            else:
                next_col, next_row = current_col - 1, current_row
        elif current_row != target_row:
            if current_row < target_row:
                next_col, next_row = current_col, current_row + 1
            else:
                next_col, next_row = current_col, current_row - 1
        else:
            return None

        if (0 <= next_col < cols and
            0 <= next_row < rows and
            next_row < len(grid[next_col]) and
            (next_col, next_row) not in visited):
            return (next_col, next_row, grid[next_col][next_row]['count'])
        return None

    def find_path_to_nearest_unvisited():
        current_col, current_row = path[-1][0], path[-1][1]

        unvisited_contributions = [(col, row, count) for col, row, count in contributions
                                 if (col, row) not in visited]

        if not unvisited_contributions:
            unvisited_spaces = [(col, row, count) for col, row, count in empty_spaces
                              if (col, row) not in visited]
            if unvisited_spaces:
                distances = []
                for col, row, count in unvisited_spaces:
                    distance = abs(col - current_col) + abs(row - current_row)
                    distances.append((distance, col, row, count))
                distances.sort()
                if distances:
                    return distances[0][1], distances[0][2], distances[0][3]
            return None

        distances = []
        for col, row, count in unvisited_contributions:
            distance = abs(col - current_col) + abs(row - current_row)
            distances.append((distance, col, row, count))

        distances.sort()
        return distances[0][1], distances[0][2], distances[0][3]

    max_moves = cols * rows * 2
    moves_made = 0
    stuck_count = 0

    while moves_made < max_moves:
        current_col, current_row = path[-1][0], path[-1][1]

        target = find_path_to_nearest_unvisited()

        if target:
            target_col, target_row, target_count = target
            next_move = move_towards_target(current_col, current_row, target_col, target_row)

            if next_move:
                path.append(next_move)
                visited.add((next_move[0], next_move[1]))
                moves_made += 1
                stuck_count = 0
                continue

        valid_moves = get_valid_moves(current_col, current_row)

        if valid_moves:
            contribution_moves = [move for move in valid_moves if move[2] > 0]
            if contribution_moves:
                next_move = random.choice(contribution_moves)
            else:
                next_move = random.choice(valid_moves)

            path.append(next_move)
            visited.add((next_move[0], next_move[1]))
            moves_made += 1
            stuck_count = 0
        else:
            stuck_count += 1
            if stuck_count > 5:
                break

            all_unvisited = []
            for col in range(cols):
                for row in range(min(rows, len(grid[col]))):
                    if (col, row) not in visited:
                        all_unvisited.append((col, row, grid[col][row]['count']))

            if not all_unvisited:
                break

            target_col, target_row, target_count = random.choice(all_unvisited)
            next_move = move_towards_target(current_col, current_row, target_col, target_row)
            if next_move and (next_move[0], next_move[1]) not in visited:
                path.append(next_move)
                visited.add((next_move[0], next_move[1]))
                moves_made += 1
                stuck_count = 0
            else:
                break

    remaining_unvisited = []
    for col in range(cols):
        for row in range(min(rows, len(grid[col]))):
            if (col, row) not in visited:
                remaining_unvisited.append((col, row, grid[col][row]['count']))

    while remaining_unvisited and len(remaining_unvisited) > 0:
        current_col, current_row = path[-1][0], path[-1][1]

        closest = min(remaining_unvisited,
                     key=lambda x: abs(x[0] - current_col) + abs(x[1] - current_row))

        next_move = move_towards_target(current_col, current_row, closest[0], closest[1])

        if next_move and (next_move[0], next_move[1]) not in visited:
            path.append(next_move)
            visited.add((next_move[0], next_move[1]))
            remaining_unvisited = [(col, row, count) for col, row, count in remaining_unvisited
                                 if (col, row) not in visited]
        else:
            break

    total_positions = sum(min(rows, len(grid[col])) for col in range(cols))
    coverage = len(visited) / total_positions * 100 if total_positions > 0 else 0

    print(f"Snake path: {len(path)} moves, visited {len(visited)}/{total_positions} ({coverage:.1f}%)")

    return path
