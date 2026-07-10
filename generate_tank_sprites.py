#!/usr/bin/env python3
"""
Cyberpunk Tank Sprite Generator
Generates improved tank and mech sprites with cyberpunk aesthetics.
Creates a 3x4 grid spritesheet (12 enemies total).
"""

from PIL import Image, ImageDraw, ImageFilter
import math
import random

# Configuration
SPRITE_WIDTH = 640
SPRITE_HEIGHT = 320
GRID_COLS = 3
GRID_ROWS = 4
OUTPUT_SIZE = (SPRITE_WIDTH * GRID_COLS, SPRITE_HEIGHT * GRID_ROWS)

# Cyberpunk color palette
COLORS = {
    'dark_metal': (25, 28, 35, 255),
    'medium_metal': (55, 60, 70, 255),
    'light_metal': (85, 90, 100, 255),
    'cyan_neon': (0, 255, 255, 255),
    'blue_neon': (0, 150, 255, 255),
    'orange_neon': (255, 140, 0, 255),
    'purple_neon': (180, 50, 255, 255),
    'green_neon': (0, 255, 128, 255),
    'red_neon': (255, 50, 50, 255),
    'yellow_neon': (255, 220, 0, 255),
    'glow_cyan': (0, 255, 255, 180),
    'glow_orange': (255, 140, 0, 180),
}

def create_transparent_base():
    """Create a transparent base image for a sprite."""
    return Image.new('RGBA', (SPRITE_WIDTH, SPRITE_HEIGHT), (0, 0, 0, 0))

def draw_polygon_with_gradient(draw, points, colors, vertical=True):
    """Draw a polygon with a simple gradient effect."""
    if len(colors) < 2:
        draw.polygon(points, fill=colors[0])
        return
    
    # Simple gradient approximation
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    for y in range(min_y, max_y + 1):
        t = (y - min_y) / max(max_y - min_y, 1)
        r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
        g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
        b = int(colors[0][2] * (1 - t) + colors[1][2] * t)
        
        # Find x range at this y
        x_points = []
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                if p2[1] != p1[1]:
                    x = int(p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]))
                    x_points.append(x)
        
        if len(x_points) >= 2:
            x_points.sort()
            draw.line([(x_points[0], y), (x_points[-1], y)], fill=(r, g, b, 255))

def add_neon_outline(draw, points, color, thickness=3):
    """Add a neon outline effect around a shape."""
    # Draw multiple offset lines for glow effect
    for offset in range(thickness, 0, -1):
        alpha = int(255 * (offset / thickness) * 0.5)
        glow_color = (*color[:3], alpha)
        offset_points = [(x + dx, y + dy) for x, y in points for dx in [-offset, 0, offset] for dy in [-offset, 0, offset]]
        # Simplified: just draw the original with lower alpha
        draw.polygon(points, outline=glow_color, width=1)
    
    # Main neon line
    draw.polygon(points, outline=color, width=2)

def draw_tank_chassis(draw, cx, cy, width, height, color_scheme, tank_type='standard'):
    """Draw the main chassis of a tank."""
    # Main body - trapezoid shape for tank-like appearance
    top_width = width * 0.7
    bottom_width = width * 0.9
    
    body_points = [
        (cx - top_width/2, cy - height/2),
        (cx + top_width/2, cy - height/2),
        (cx + bottom_width/2, cy + height/2),
        (cx - bottom_width/2, cy + height/2),
    ]
    
    # Fill with gradient
    dark_color = color_scheme['dark']
    mid_color = color_scheme['medium']
    draw.polygon(body_points, fill=dark_color)
    
    # Add panel details
    panel_margin = 15
    inner_points = [
        (cx - top_width/2 + panel_margin, cy - height/2 + panel_margin),
        (cx + top_width/2 - panel_margin, cy - height/2 + panel_margin),
        (cx + bottom_width/2 - panel_margin, cy + height/2 - panel_margin),
        (cx - bottom_width/2 + panel_margin, cy + height/2 - panel_margin),
    ]
    draw.polygon(inner_points, fill=mid_color)
    
    return body_points

def draw_tank_tracks(draw, cx, cy, width, height, color_scheme):
    """Draw tank tracks on both sides."""
    track_width = width * 0.15
    track_height = height * 0.85
    
    # Left track
    left_track_points = [
        (cx - width/2 - track_width/2, cy - track_height/2),
        (cx - width/2 + track_width/2, cy - track_height/2),
        (cx - width/2 + track_width/2, cy + track_height/2),
        (cx - width/2 - track_width/2, cy + track_height/2),
    ]
    
    # Right track
    right_track_points = [
        (cx + width/2 - track_width/2, cy - track_height/2),
        (cx + width/2 + track_width/2, cy - track_height/2),
        (cx + width/2 + track_width/2, cy + track_height/2),
        (cx + width/2 - track_width/2, cy + track_height/2),
    ]
    
    draw.polygon(left_track_points, fill=color_scheme['dark'])
    draw.polygon(right_track_points, fill=color_scheme['dark'])
    
    # Add track tread details
    tread_spacing = 20
    for i in range(int(track_height / tread_spacing)):
        y_offset = -track_height/2 + i * tread_spacing + tread_spacing/2
        # Left tread
        draw.rectangle([
            cx - width/2 - track_width/2 + 2,
            cy + y_offset - 3,
            cx - width/2 + track_width/2 - 2,
            cy + y_offset + 3
        ], fill=color_scheme['medium'])
        # Right tread
        draw.rectangle([
            cx + width/2 - track_width/2 + 2,
            cy + y_offset - 3,
            cx + width/2 + track_width/2 - 2,
            cy + y_offset + 3
        ], fill=color_scheme['medium'])

def draw_turret(draw, cx, cy, size, color_scheme, turret_type='cannon'):
    """Draw various turret types."""
    if turret_type == 'cannon':
        # Single large cannon
        barrel_length = size * 1.2
        barrel_width = size * 0.25
        
        # Barrel
        barrel_points = [
            (cx - barrel_width/2, cy),
            (cx + barrel_width/2, cy),
            (cx + barrel_width/2 + barrel_length, cy + barrel_width/4),
            (cx - barrel_width/2, cy + barrel_width/4),
        ]
        draw.polygon(barrel_points, fill=color_scheme['medium'])
        
        # Barrel tip glow
        draw.ellipse([
            cx + barrel_length - 10,
            cy - 5,
            cx + barrel_length + 10,
            cy + 15
        ], fill=COLORS['glow_cyan'])
        
        # Turret base (dome)
        dome_radius = size * 0.6
        draw.ellipse([
            cx - dome_radius,
            cy - dome_radius,
            cx + dome_radius,
            cy + dome_radius
        ], fill=color_scheme['light'])
        
    elif turret_type == 'dual_cannon':
        # Two parallel cannons
        barrel_length = size * 1.0
        barrel_width = size * 0.18
        spacing = size * 0.3
        
        for offset in [-spacing/2, spacing/2]:
            barrel_points = [
                (cx + offset - barrel_width/2, cy),
                (cx + offset + barrel_width/2, cy),
                (cx + offset + barrel_width/2 + barrel_length, cy + barrel_width/4),
                (cx + offset - barrel_width/2, cy + barrel_width/4),
            ]
            draw.polygon(barrel_points, fill=color_scheme['medium'])
            
            # Barrel tip glow
            draw.ellipse([
                cx + offset + barrel_length - 8,
                cy - 4,
                cx + offset + barrel_length + 8,
                cy + 12
            ], fill=COLORS['glow_orange'])
        
        # Central turret housing
        turret_size = size * 0.7
        draw.rectangle([
            cx - turret_size/2,
            cy - turret_size/2,
            cx + turret_size/2,
            cy + turret_size/2
        ], fill=color_scheme['light'], outline=COLORS['orange_neon'], width=2)
        
    elif turret_type == 'missile':
        # Missile pod launcher
        pod_width = size * 1.0
        pod_height = size * 0.6
        
        # Main pod
        draw.rounded_rectangle([
            cx - pod_width/2,
            cy - pod_height/2,
            cx + pod_width/2,
            cy + pod_height/2
        ], radius=10, fill=color_scheme['dark'], outline=COLORS['red_neon'], width=2)
        
        # Missile tubes
        tube_count = 4
        tube_spacing = pod_width / (tube_count + 1)
        for i in range(tube_count):
            tube_x = cx - pod_width/2 + tube_spacing * (i + 1)
            draw.ellipse([
                tube_x - 12,
                cy - 15,
                tube_x + 12,
                cy + 15
            ], fill=color_scheme['medium'])
            # Tube glow
            draw.ellipse([
                tube_x - 8,
                cy - 10,
                tube_x + 8,
                cy + 10
            ], fill=COLORS['glow_cyan'])
        
    elif turret_type == 'energy':
        # Energy weapon turret
        core_radius = size * 0.5
        
        # Outer ring
        draw.ellipse([
            cx - core_radius * 1.3,
            cy - core_radius * 1.3,
            cx + core_radius * 1.3,
            cy + core_radius * 1.3
        ], outline=COLORS['purple_neon'], width=4)
        
        # Inner core
        draw.ellipse([
            cx - core_radius,
            cy - core_radius,
            cx + core_radius,
            cy + core_radius
        ], fill=COLORS['glow_cyan'])
        
        # Energy beam emitter
        emitter_length = size * 0.8
        draw.polygon([
            (cx + core_radius, cy - 10),
            (cx + core_radius + emitter_length, cy),
            (cx + core_radius, cy + 10),
        ], fill=COLORS['glow_cyan'])
        
    elif turret_type == 'hover':
        # Hover tank - no tracks, floating底盘
        # Main body (more angular)
        body_width = size * 1.4
        body_height = size * 0.8
        
        hover_points = [
            (cx - body_width/2, cy - body_height/3),
            (cx + body_width/2, cy - body_height/3),
            (cx + body_width/2 - 20, cy + body_height/2),
            (cx - body_width/2 + 20, cy + body_height/2),
        ]
        draw.polygon(hover_points, fill=color_scheme['medium'])
        
        # Glow underneath (hover effect)
        glow_points = [
            (cx - body_width/2 + 10, cy + body_height/2 + 5),
            (cx + body_width/2 - 10, cy + body_height/2 + 5),
            (cx + body_width/2 - 30, cy + body_height/2 + 15),
            (cx - body_width/2 + 30, cy + body_height/2 + 15),
        ]
        draw.polygon(glow_points, fill=(*COLORS['cyan_neon'][:3], 100))
        
        # Small turret
        small_turret_radius = size * 0.35
        draw.ellipse([
            cx - small_turret_radius,
            cy - small_turret_radius - 10,
            cx + small_turret_radius,
            cy + small_turret_radius - 10
        ], fill=color_scheme['light'])
        
        # Mini cannon
        draw.rectangle([
            cx + small_turret_radius,
            cy - 15,
            cx + small_turret_radius + size * 0.6,
            cy - 5
        ], fill=color_scheme['medium'])

def draw_mech_boss(draw, cx, cy, size, color_scheme, boss_type='heavy'):
    """Draw mech-like boss enemies with robotic features."""
    
    if boss_type == 'heavy_mech':
        # Large bipedal mech
        # Legs
        leg_width = size * 0.25
        leg_height = size * 0.9
        
        # Left leg
        draw.polygon([
            (cx - size/3 - leg_width/2, cy + leg_height/2),
            (cx - size/3 + leg_width/2, cy + leg_height/2),
            (cx - size/3 + leg_width/2 + 10, cy - leg_height/2),
            (cx - size/3 - leg_width/2 - 10, cy - leg_height/2),
        ], fill=color_scheme['dark'], outline=COLORS['orange_neon'], width=2)
        
        # Right leg
        draw.polygon([
            (cx + size/3 - leg_width/2, cy + leg_height/2),
            (cx + size/3 + leg_width/2, cy + leg_height/2),
            (cx + size/3 + leg_width/2 + 10, cy - leg_height/2),
            (cx + size/3 - leg_width/2 - 10, cy - leg_height/2),
        ], fill=color_scheme['dark'], outline=COLORS['orange_neon'], width=2)
        
        # Torso
        torso_width = size * 0.9
        torso_height = size * 0.7
        draw.rounded_rectangle([
            cx - torso_width/2,
            cy - torso_height/2 - 20,
            cx + torso_width/2,
            cy + torso_height/2 - 20
        ], radius=15, fill=color_scheme['medium'], outline=COLORS['red_neon'], width=3)
        
        # Chest reactor (glowing core)
        reactor_radius = size * 0.15
        draw.ellipse([
            cx - reactor_radius,
            cy - reactor_radius - 20,
            cx + reactor_radius,
            cy + reactor_radius - 20
        ], fill=COLORS['glow_cyan'])
        
        # Head
        head_size = size * 0.3
        draw.rounded_rectangle([
            cx - head_size/2,
            cy - torso_height/2 - head_size - 25,
            cx + head_size/2,
            cy - torso_height/2 - 25
        ], radius=8, fill=color_scheme['light'])
        
        # Visor (glowing eyes)
        draw.rectangle([
            cx - head_size/3,
            cy - torso_height/2 - head_size - 20,
            cx + head_size/3,
            cy - torso_height/2 - head_size - 12
        ], fill=COLORS['glow_orange'])
        
        # Arms with weapons
        arm_width = size * 0.15
        arm_length = size * 0.6
        
        # Left arm (gun)
        draw.polygon([
            (cx - torso_width/2 - arm_width/2, cy - 20),
            (cx - torso_width/2 + arm_width/2, cy - 20),
            (cx - torso_width/2 + arm_width/2 - arm_length/2, cy + arm_length),
            (cx - torso_width/2 - arm_width/2 - arm_length/2, cy + arm_length),
        ], fill=color_scheme['medium'])
        
        # Right arm (claw/blade)
        draw.polygon([
            (cx + torso_width/2 - arm_width/2, cy - 20),
            (cx + torso_width/2 + arm_width/2, cy - 20),
            (cx + torso_width/2 + arm_width/2 + arm_length/2, cy + arm_length),
            (cx + torso_width/2 - arm_width/2 + arm_length/2, cy + arm_length),
        ], fill=color_scheme['medium'])
        
        # Shoulder pads
        shoulder_size = size * 0.25
        draw.ellipse([
            cx - torso_width/2 - shoulder_size,
            cy - torso_height/2 - shoulder_size - 10,
            cx - torso_width/2,
            cy - torso_height/2 + shoulder_size - 10
        ], fill=color_scheme['dark'], outline=COLORS['orange_neon'], width=2)
        
        draw.ellipse([
            cx + torso_width/2,
            cy - torso_height/2 - shoulder_size - 10,
            cx + torso_width/2 + shoulder_size,
            cy - torso_height/2 + shoulder_size - 10
        ], fill=color_scheme['dark'], outline=COLORS['orange_neon'], width=2)
        
    elif boss_type == 'spider_mech':
        # Spider-like mech with multiple legs
        body_radius = size * 0.35
        
        # Central body
        draw.ellipse([
            cx - body_radius,
            cy - body_radius,
            cx + body_radius,
            cy + body_radius
        ], fill=color_scheme['medium'], outline=COLORS['purple_neon'], width=3)
        
        # Glowing core
        draw.ellipse([
            cx - body_radius * 0.4,
            cy - body_radius * 0.4,
            cx + body_radius * 0.4,
            cy + body_radius * 0.4
        ], fill=COLORS['glow_purple'] if 'glow_purple' in COLORS else COLORS['glow_cyan'])
        
        # Legs (8 legs for spider)
        leg_count = 8
        for i in range(leg_count):
            angle = (2 * math.pi / leg_count) * i
            leg_start_x = cx + math.cos(angle) * body_radius * 0.8
            leg_start_y = cy + math.sin(angle) * body_radius * 0.8
            leg_end_x = cx + math.cos(angle) * size * 0.8
            leg_end_y = cy + math.sin(angle) * size * 0.8
            
            # Leg segments
            mid_x = (leg_start_x + leg_end_x) / 2 + math.cos(angle + math.pi/2) * 20
            mid_y = (leg_start_y + leg_end_y) / 2 + math.sin(angle + math.pi/2) * 20
            
            # Draw main leg line (thick, dark)
            draw.line([
                (leg_start_x, leg_start_y),
                (mid_x, mid_y),
                (leg_end_x, leg_end_y)
            ], fill=color_scheme['dark'], width=12)
            
            # Draw neon outline as separate thinner line
            draw.line([
                (leg_start_x, leg_start_y),
                (mid_x, mid_y),
                (leg_end_x, leg_end_y)
            ], fill=COLORS['purple_neon'], width=3)
        
        # Weapon mount on top
        weapon_size = size * 0.3
        draw.polygon([
            (cx, cy - weapon_size),
            (cx + weapon_size * 0.8, cy + weapon_size * 0.5),
            (cx, cy + weapon_size * 0.3),
            (cx - weapon_size * 0.8, cy + weapon_size * 0.5),
        ], fill=color_scheme['dark'], outline=COLORS['red_neon'], width=2)
        
    elif boss_type == 'walker_tank':
        # Hybrid walker-tank design
        # Wide stance legs
        leg_width = size * 0.3
        leg_height = size * 0.7
        
        # Left leg (thick, armored)
        draw.polygon([
            (cx - size/2 - leg_width/2, cy + leg_height/2),
            (cx - size/2 + leg_width/2, cy + leg_height/2),
            (cx - size/2 + leg_width/3, cy - leg_height/2),
            (cx - size/2 - leg_width/3, cy - leg_height/2),
        ], fill=color_scheme['dark'], outline=COLORS['blue_neon'], width=3)
        
        # Right leg
        draw.polygon([
            (cx + size/2 - leg_width/2, cy + leg_height/2),
            (cx + size/2 + leg_width/2, cy + leg_height/2),
            (cx + size/2 + leg_width/3, cy - leg_height/2),
            (cx + size/2 - leg_width/3, cy - leg_height/2),
        ], fill=color_scheme['dark'], outline=COLORS['blue_neon'], width=3)
        
        # Main body (tank-like but elevated)
        body_width = size * 1.2
        body_height = size * 0.6
        draw.rounded_rectangle([
            cx - body_width/2,
            cy - body_height/2 - 10,
            cx + body_width/2,
            cy + body_height/2 - 10
        ], radius=10, fill=color_scheme['medium'], outline=COLORS['cyan_neon'], width=3)
        
        # Rotating turret on top
        turret_radius = size * 0.35
        draw.ellipse([
            cx - turret_radius,
            cy - turret_radius - 15,
            cx + turret_radius,
            cy + turret_radius - 15
        ], fill=color_scheme['light'])
        
        # Long cannon
        cannon_length = size * 1.3
        cannon_width = size * 0.2
        draw.rectangle([
            cx + turret_radius - 10,
            cy - cannon_width/2 - 15,
            cx + turret_radius + cannon_length,
            cy + cannon_width/2 - 15
        ], fill=color_scheme['medium'], outline=COLORS['cyan_neon'], width=2)
        
        # Cannon tip glow
        draw.ellipse([
            cx + turret_radius + cannon_length - 15,
            cy - cannon_width/2 - 20,
            cx + turret_radius + cannon_length + 15,
            cy + cannon_width/2 - 10
        ], fill=COLORS['glow_cyan'])

def add_cyberpunk_details(draw, cx, cy, size, accent_color):
    """Add cyberpunk detailing: vents, conduits, holographic elements."""
    
    # Glowing vents
    vent_count = 3
    vent_width = size * 0.15
    vent_height = 8
    for i in range(vent_count):
        vent_x = cx - size * 0.2 + i * (vent_width + 10)
        vent_y = cy + size * 0.2
        draw.rounded_rectangle([
            vent_x,
            vent_y,
            vent_x + vent_width,
            vent_y + vent_height
        ], radius=2, fill=(*accent_color[:3], 200))
    
    # Holographic targeting nodes (small glowing dots)
    node_positions = [
        (cx - size * 0.3, cy - size * 0.2),
        (cx + size * 0.3, cy - size * 0.2),
        (cx, cy + size * 0.3),
    ]
    for nx, ny in node_positions:
        draw.ellipse([
            nx - 4,
            ny - 4,
            nx + 4,
            ny + 4
        ], fill=(*COLORS['cyan_neon'][:3], 220))
    
    # Energy conduits (thin glowing lines)
    conduit_length = size * 0.4
    draw.line([
        (cx - conduit_length/2, cy),
        (cx + conduit_length/2, cy)
    ], fill=(*accent_color[:3], 150), width=2)

def generate_sprite(index, sprite_type):
    """Generate a single sprite based on type."""
    img = create_transparent_base()
    draw = ImageDraw.Draw(img)
    
    cx, cy = SPRITE_WIDTH // 2, SPRITE_HEIGHT // 2
    base_size = min(SPRITE_WIDTH, SPRITE_HEIGHT) * 0.35
    
    # Define color schemes based on enemy type
    color_schemes = [
        {'dark': COLORS['dark_metal'], 'medium': COLORS['medium_metal'], 'light': COLORS['light_metal'], 'accent': COLORS['cyan_neon']},
        {'dark': (30, 25, 35, 255), 'medium': (60, 50, 70, 255), 'light': (90, 80, 100, 255), 'accent': COLORS['purple_neon']},
        {'dark': (35, 30, 25, 255), 'medium': (70, 60, 50, 255), 'light': (100, 90, 80, 255), 'accent': COLORS['orange_neon']},
        {'dark': (25, 35, 30, 255), 'medium': (50, 70, 60, 255), 'light': (80, 100, 90, 255), 'accent': COLORS['green_neon']},
        {'dark': (35, 25, 30, 255), 'medium': (70, 50, 60, 255), 'light': (100, 80, 90, 255), 'accent': COLORS['red_neon']},
    ]
    
    scheme = color_schemes[index % len(color_schemes)]
    
    # Regular tanks (indices 0-9)
    if index == 0:  # Standard cannon tank
        draw_tank_tracks(draw, cx, cy, base_size * 1.4, base_size, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.2, base_size * 0.8, scheme, 'standard')
        draw_turret(draw, cx, cy - base_size * 0.1, base_size * 0.5, scheme, 'cannon')
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 1:  # Dual cannon tank
        draw_tank_tracks(draw, cx, cy, base_size * 1.5, base_size, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.3, base_size * 0.85, scheme, 'heavy')
        draw_turret(draw, cx, cy - base_size * 0.1, base_size * 0.55, scheme, 'dual_cannon')
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 2:  # Missile tank
        draw_tank_tracks(draw, cx, cy, base_size * 1.4, base_size, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.2, base_size * 0.9, scheme, 'missile')
        draw_turret(draw, cx, cy - base_size * 0.15, base_size * 0.5, scheme, 'missile')
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 3:  # Energy turret tank
        draw_tank_tracks(draw, cx, cy, base_size * 1.3, base_size, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.1, base_size * 0.75, scheme, 'energy')
        draw_turret(draw, cx, cy - base_size * 0.05, base_size * 0.5, scheme, 'energy')
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 4:  # Hover tank (fast, light)
        draw_turret(draw, cx, cy - base_size * 0.1, base_size * 0.45, scheme, 'hover')
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 5:  # Heavy assault tank
        draw_tank_tracks(draw, cx, cy, base_size * 1.7, base_size * 1.1, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.5, base_size * 1.0, scheme, 'heavy_assault')
        draw_turret(draw, cx, cy - base_size * 0.15, base_size * 0.65, scheme, 'dual_cannon')
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 6:  # Sniper tank (long range)
        draw_tank_tracks(draw, cx, cy, base_size * 1.3, base_size, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.1, base_size * 0.7, scheme, 'sniper')
        # Extra long cannon
        turret_cx, turret_cy = cx, cy - base_size * 0.1
        barrel_length = base_size * 1.8
        barrel_width = base_size * 0.15
        draw.polygon([
            (turret_cx - barrel_width/2, turret_cy),
            (turret_cx + barrel_width/2, turret_cy),
            (turret_cx + barrel_width/2 + barrel_length, turret_cy + barrel_width/4),
            (turret_cx - barrel_width/2, turret_cy + barrel_width/4),
        ], fill=scheme['medium'])
        draw.ellipse([
            turret_cx - base_size * 0.3,
            turret_cy - base_size * 0.3,
            turret_cx + base_size * 0.3,
            turret_cy + base_size * 0.3
        ], fill=scheme['light'])
        draw.ellipse([
            turret_cx + barrel_length - 10,
            turret_cy - 8,
            turret_cx + barrel_length + 10,
            turret_cy + 12
        ], fill=COLORS['glow_orange'])
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 7:  # Anti-air tank (rotating multi-barrel)
        draw_tank_tracks(draw, cx, cy, base_size * 1.35, base_size, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.15, base_size * 0.75, scheme, 'aa')
        # Multi-barrel AA turret
        turret_radius = base_size * 0.4
        draw.ellipse([
            cx - turret_radius,
            cy - turret_radius - 10,
            cx + turret_radius,
            cy + turret_radius - 10
        ], fill=scheme['medium'])
        # Four barrels pointing up
        for angle in [45, 135, 225, 315]:
            rad = math.radians(angle)
            barrel_end_x = cx + math.cos(rad) * base_size * 0.7
            barrel_end_y = cy - turret_radius - 10 + math.sin(rad) * base_size * 0.7
            draw.line([
                (cx + math.cos(rad) * turret_radius * 0.5, cy - turret_radius/2 - 10),
                (barrel_end_x, barrel_end_y)
            ], fill=scheme['light'], width=12)
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 8:  # Flamethrower tank
        draw_tank_tracks(draw, cx, cy, base_size * 1.4, base_size, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.2, base_size * 0.85, scheme, 'flame')
        # Flamethrower nozzle
        nozzle_cx, nozzle_cy = cx, cy - base_size * 0.1
        draw.polygon([
            (nozzle_cx - 30, nozzle_cy - 20),
            (nozzle_cx + 30, nozzle_cy - 20),
            (nozzle_cx + 50, nozzle_cy + 10),
            (nozzle_cx - 50, nozzle_cy + 10),
        ], fill=scheme['dark'], outline=COLORS['orange_neon'], width=2)
        # Flame effect (semi-transparent)
        flame_img = Image.new('RGBA', (100, 80), (0, 0, 0, 0))
        flame_draw = ImageDraw.Draw(flame_img)
        flame_draw.polygon([
            (50, 40),
            (70, 10),
            (90, 40),
            (70, 70)
        ], fill=(*COLORS['orange_neon'][:3], 180))
        img.alpha_composite(flame_img, (int(nozzle_cx + 40), int(nozzle_cy - 40)))
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    elif index == 9:  # Shield tank (defensive)
        draw_tank_tracks(draw, cx, cy, base_size * 1.5, base_size, scheme)
        draw_tank_chassis(draw, cx, cy, base_size * 1.3, base_size * 0.9, scheme, 'shield')
        # Small turret
        draw_turret(draw, cx, cy - base_size * 0.1, base_size * 0.4, scheme, 'cannon')
        # Energy shield generator
        shield_radius = base_size * 0.8
        shield_arc = [(cx - shield_radius, cy - shield_radius/2), 
                      (cx + shield_radius, cy + shield_radius)]
        draw.arc(shield_arc, 0, 180, fill=(*COLORS['cyan_neon'][:3], 100), width=4)
        add_cyberpunk_details(draw, cx, cy, base_size, scheme['accent'])
        
    # Boss mechs (indices 10-11)
    elif index == 10:  # Heavy Mech Boss
        draw_mech_boss(draw, cx, cy, base_size * 1.3, scheme, 'heavy_mech')
        add_cyberpunk_details(draw, cx, cy, base_size * 1.2, COLORS['red_neon'])
        
    elif index == 11:  # Spider Mech Boss
        draw_mech_boss(draw, cx, cy, base_size * 1.2, scheme, 'spider_mech')
        add_cyberpunk_details(draw, cx, cy, base_size * 1.1, COLORS['purple_neon'])
    
    return img

def create_spritesheet():
    """Create the complete 3x4 spritesheet."""
    spritesheet = Image.new('RGBA', OUTPUT_SIZE, (0, 0, 0, 0))
    
    # Define sprite types
    sprite_types = [
        'standard_cannon', 'dual_cannon', 'missile', 'energy',
        'hover', 'heavy_assault', 'sniper', 'anti_air',
        'flamethrower', 'shield', 'heavy_mech_boss', 'spider_mech_boss'
    ]
    
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            index = row * GRID_COLS + col
            if index < len(sprite_types):
                sprite = generate_sprite(index, sprite_types[index])
                x_offset = col * SPRITE_WIDTH
                y_offset = row * SPRITE_HEIGHT
                spritesheet.paste(sprite, (x_offset, y_offset), sprite)
    
    return spritesheet

def main():
    print("Generating cyberpunk tank spritesheet...")
    spritesheet = create_spritesheet()
    
    output_path = '/workspace/tanks_improved.png'
    spritesheet.save(output_path, 'PNG')
    print(f"Spritesheet saved to: {output_path}")
    print(f"Dimensions: {spritesheet.size[0]}x{spritesheet.size[1]} pixels")
    print(f"Grid: {GRID_COLS}x{GRID_ROWS} (12 sprites)")
    
    # Also create individual sprite files for reference
    output_dir = '/workspace/sprites_individual'
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    sprite_names = [
        'standard_cannon', 'dual_cannon', 'missile', 'energy',
        'hover', 'heavy_assault', 'sniper', 'anti_air',
        'flamethrower', 'shield', 'heavy_mech_boss', 'spider_mech_boss'
    ]
    
    for i, name in enumerate(sprite_names):
        row = i // GRID_COLS
        col = i % GRID_COLS
        x = col * SPRITE_WIDTH
        y = row * SPRITE_HEIGHT
        individual = spritesheet.crop((x, y, x + SPRITE_WIDTH, y + SPRITE_HEIGHT))
        individual.save(f'{output_dir}/{name}.png', 'PNG')
    
    print(f"Individual sprites saved to: {output_dir}/")

if __name__ == '__main__':
    main()
