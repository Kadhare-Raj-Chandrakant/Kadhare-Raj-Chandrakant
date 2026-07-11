#!/usr/bin/env python3
"""
GIF animation generator for GitHub Contribution Snake
"""

from PIL import Image, ImageDraw
from .config import SNAKE_CONFIG, COLORS

def generate_gif_animation(grid, snake_path, output_path, dark_mode=True):
    if not grid:
        print("No grid data available")
        return

    rows = len(grid[0])
    cols = len(grid)

    cell_size = SNAKE_CONFIG['cell_size']
    cell_spacing = SNAKE_CONFIG['cell_spacing']
    snake_length = SNAKE_CONFIG['snake_length']
    animation_duration = SNAKE_CONFIG['animation_duration']
    padding = SNAKE_CONFIG['padding']

    colors = COLORS['dark'] if dark_mode else COLORS['light']

    width = cols * (cell_size + cell_spacing) - cell_spacing + (padding * 2)
    height = rows * (cell_size + cell_spacing) - cell_spacing + (padding * 2)

    path_len = len(snake_path)
    forward_frames = []
    eaten_positions = set()

    print(f"Creating {path_len * 2} frames for continuous GIF...")

    for frame_idx in range(path_len):
        eaten_positions.add((snake_path[frame_idx][0], snake_path[frame_idx][1]))
        forward_frames.append(_render_frame(frame_idx, grid, snake_path, snake_length, eaten_positions, cell_size, cell_spacing, padding, colors, width, height, dark_mode))

    backward_frames = []
    eaten_reverse = set(eaten_positions)

    for frame_idx in range(path_len - 1, -1, -1):
        if frame_idx < path_len:
            eaten_reverse.discard((snake_path[frame_idx][0], snake_path[frame_idx][1]))
        backward_frames.append(_render_frame(frame_idx, grid, snake_path, snake_length, eaten_reverse, cell_size, cell_spacing, padding, colors, width, height, dark_mode))

    all_frames = forward_frames + backward_frames

    all_frames[0].save(
        output_path,
        save_all=True,
        append_images=all_frames[1:],
        duration=animation_duration,
        loop=0,
        optimize=True
    )
    theme = "dark" if dark_mode else "light"
    print(f"GIF ({theme}) saved to: {output_path}")


def _render_frame(frame_idx, grid, snake_path, snake_length, eaten_positions, cell_size, cell_spacing, padding, colors, width, height, dark_mode):
    img = Image.new('RGB', (width, height), colors['background'])
    draw = ImageDraw.Draw(img)

    rows = len(grid[0])
    cols = len(grid)

    for col in range(cols):
        for row in range(rows):
            if row >= len(grid[col]):
                continue

            x = col * (cell_size + cell_spacing) + padding
            y = row * (cell_size + cell_spacing) + padding

            if (col, row) in eaten_positions:
                level = 0
            else:
                level = min(4, grid[col][row]['level'])

            color = colors['levels'][level]

            draw.rounded_rectangle(
                [x, y, x + cell_size, y + cell_size],
                radius=2,
                fill=color
            )

    for i in range(snake_length):
        snake_pos = frame_idx - i
        if 0 <= snake_pos < len(snake_path):
            col, row, contribution_count = snake_path[snake_pos]

            if col >= cols or row >= len(grid[col]):
                continue

            x = col * (cell_size + cell_spacing) + padding
            y = row * (cell_size + cell_spacing) + padding

            if i == 0:
                color = colors['snake_head']
                if contribution_count > 0:
                    offset = 2
                    if dark_mode:
                        glow_color = '#ff9999'
                    else:
                        glow_color = '#ff6666'
                    draw.rounded_rectangle(
                        [x - offset - 1, y - offset - 1, x + cell_size + offset + 1, y + cell_size + offset + 1],
                        radius=4,
                        fill=glow_color
                    )
                offset = 1 if contribution_count > 0 else 0
                draw.rounded_rectangle(
                    [x - offset, y - offset, x + cell_size + offset, y + cell_size + offset],
                    radius=3,
                    fill=color
                )
            else:
                alpha = 1.0 - (i / snake_length) * 0.6
                snake_color = colors['snake']
                if snake_color.startswith('#'):
                    rgb = tuple(int(snake_color[j:j+2], 16) for j in (1, 3, 5))
                    bg_rgb = tuple(int(colors['background'][j:j+2], 16) for j in (1, 3, 5))
                    blended = tuple(int(rgb[k] * alpha + bg_rgb[k] * (1 - alpha)) for k in range(3))
                    color = f"#{blended[0]:02x}{blended[1]:02x}{blended[2]:02x}"
                else:
                    color = snake_color

                draw.rounded_rectangle(
                    [x, y, x + cell_size, y + cell_size],
                    radius=2,
                    fill=color
                )

    return img
