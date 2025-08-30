"""
indoor_mario.py — Ursina indoor test level with SM64-inspired dressing.

- Castle-like room dressing (checkered floor, red carpet, paintings, doors)
- Simple third-person camera (Lakitu-style OFF: direct follow)
- Character physics with robust ground snap and kill plane
- Optional use of external Mario 3D model if found in assets
"""

from ursina import *
import os
import math

# Global toggle: external model files OFF (always use builtin cube)
FILES_OFF = True


# =============================
# Helpers
# =============================

def resolve_mario_model():
    """Try to find an external Mario 3D model in common asset paths.
    Returns (model_path_or_builtin, texture_path_or_None).
    Place your model under an `assets/` folder next to this script, e.g.:
      assets/mario.glb, assets/mario.gltf, assets/mario.obj, assets/mario.ursinamesh
      optional texture: assets/mario.png
    """
    if FILES_OFF:
        return 'cube', None
    here = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(here, 'assets')
    candidates = [
        'mario.glb', 'mario.gltf', 'mario.obj', 'mario.ursinamesh',
        'Mario.glb', 'Mario.gltf', 'Mario.obj', 'Mario.ursinamesh'
    ]
    texture_candidates = ['mario.png', 'Mario.png']

    model_path = None
    texture_path = None

    if os.path.isdir(assets):
        for name in candidates:
            p = os.path.join(assets, name)
            if os.path.isfile(p):
                model_path = p
                break
        if model_path:
            for tname in texture_candidates:
                tp = os.path.join(assets, tname)
                if os.path.isfile(tp):
                    texture_path = tp
                    break

    # Fallback to cube if no model found
    if not model_path:
        model_path = 'cube'
    return model_path, texture_path


# =============================
# ENVIRONMENT
# =============================
def create_indoor_environment():
    """Creates a closed indoor room (floor, walls, ceiling) and decorates it
    loosely in the style of Princess Peach's Castle main hall.
    """
    room_size = 30
    wall_height = 10
    wall_thickness = 1

    # Primary floor slab with collider. Top surface sits at y=0
    floor = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(150, 120, 90),  # base under the tiles
        scale=(room_size, 1, room_size),
        position=(0, -0.5, 0),   # top sits exactly at y=0
        collider='box'
    )

    # Ceiling
    ceiling = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(160, 140, 120),
        scale=(room_size, wall_thickness, room_size),
        position=(0, wall_height, 0),
        collider='box'
    )

    # Walls (light warm tone)
    walls = []
    # North
    walls.append(Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(200, 180, 165),
        scale=(room_size, wall_height, wall_thickness),
        position=(0, wall_height/2, room_size/2),
        collider='box'
    ))
    # South
    walls.append(Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(200, 180, 165),
        scale=(room_size, wall_height, wall_thickness),
        position=(0, wall_height/2, -room_size/2),
        collider='box'
    ))
    # East
    walls.append(Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(200, 180, 165),
        scale=(wall_thickness, wall_height, room_size),
        position=(room_size/2, wall_height/2, 0),
        collider='box'
    ))
    # West
    walls.append(Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(200, 180, 165),
        scale=(wall_thickness, wall_height, room_size),
        position=(-room_size/2, wall_height/2, 0),
        collider='box'
    ))

    # Checkered floor tiles (black/white) on top of the slab
    # Keep this light: 12x12 grid over 30x30 area
    tiles = []
    grid = 12
    tile_size = room_size / grid
    start = -room_size / 2 + tile_size / 2
    for gx in range(grid):
        for gz in range(grid):
            is_black = (gx + gz) % 2 == 0
            tiles.append(Entity(
                model='quad',
                color=color.rgb(240, 240, 240) if not is_black else color.rgb(30, 30, 30),
                scale=(tile_size, tile_size),
                rotation_x=90,
                position=(start + gx * tile_size, 0.01, start + gz * tile_size),
                collider=None
            ))

    # Red carpet down the middle
    carpet = Entity(
        model='cube',
        color=color.rgb(170, 20, 20),
        scale=(4, 0.02, room_size * 0.8),
        position=(0, 0.02, 0),
        collider=None
    )

    # Decorative pillars (use cubes for compatibility if 'cylinder' model is missing)
    pillars = []
    for sx in (-1, 1):
        for sz in (-1, 1):
            pillars.append(Entity(
                model='cube',
                color=color.rgb(210, 190, 175),
                scale=(1.2, wall_height, 1.2),  # slender columns
                position=(sx * (room_size/2 - 3), wall_height/2, sz * (room_size/2 - 3)),
                collider='box'
            ))

    # Castle-style doors on the north wall: one star door center, two side doors
    door_z = room_size/2 - 0.51
    # Center door
    center_door = Entity(model='cube', color=color.rgb(180, 120, 60),
                         scale=(3, 4.5, 0.3), position=(0, 2.25, door_z), collider='box')
    # Star emblem
    star = Entity(parent=center_door, model='quad', color=color.yellow,
                  scale=(1, 1), position=(0, 0.5, -0.18), rotation_x=0)
    # Side doors
    left_door = Entity(model='cube', color=color.rgb(150, 90, 50),
                       scale=(2.4, 4, 0.3), position=(-6, 2, door_z), collider='box')
    right_door = Entity(model='cube', color=color.rgb(150, 90, 50),
                        scale=(2.4, 4, 0.3), position=(6, 2, door_z), collider='box')

    # Paintings along the north wall
    paintings = []
    for i, x in enumerate((-10, 0, 10)):
        paintings.append(Entity(
            model='quad',
            color=color.rgb(230, 200, 170),
            scale=(3, 2.5),
            position=(x, 3.0, door_z + 0.02),
            rotation_y=180,
            collider=None
        ))

    return [floor, ceiling] + walls + tiles + [carpet] + pillars + [center_door, left_door, right_door] + paintings


def create_furniture():
    """Adds simple props inside the room."""
    table = Entity(
        model='cube',
        color=color.rgb(101, 67, 33),
        scale=(4, 1, 4),
        position=(0, 0.5, 0),
        collider='box'
    )

    # Four green columns (decor) — use cubes for broad compatibility
    for i in range(4):
        Entity(
            model='cube',
            color=color.green,
            scale=(1, 3, 1),
            position=(8 * math.cos(i * math.pi/2), 1.5, 8 * math.sin(i * math.pi/2)),
            collider='box'
        )


# =============================
# PLAYER CONTROLLER
# =============================
class Mario(Entity):
    def __init__(self, **kwargs):
        model_path, texture_path = resolve_mario_model()
        super().__init__(
            model=model_path,
            texture=texture_path,
            color=color.white if texture_path else color.blue,
            scale=(1, 2, 1),   # 2 units tall
            origin_y=-1,       # pivot at feet
            collider='box',
            **kwargs
        )

        # Movement
        self.speed = 6
        self.jump_speed = 10
        self.gravity = -25
        self.velocity_y = 0
        self.terminal = -20
        self.on_ground = False
        self.ground_snap = 0.25   # max snap distance to ground
        self.skin = 0.05          # small cast tolerance

        # Respawn logic
        self.kill_y = -20
        self.spawn_point = Vec3(self.position)

        # Camera setup (Lakitu off: simple follow)
        self.camera_pivot = Entity(parent=self, y=1.5)
        camera.parent = self.camera_pivot
        camera.position = (0, 3, -7)
        camera.rotation = (15, 0, 0)
        camera.fov = 85

    def update(self):
        # Camera-relative input (WASD relative to camera yaw)
        input_x = held_keys['d'] - held_keys['a']
        input_z = held_keys['w'] - held_keys['s']
        move_dir = (camera.forward * input_z + camera.right * input_x)
        move_dir.y = 0
        if move_dir.length() > 0:
            move_dir = move_dir.normalized()
            self.look_at(self.position + move_dir)
            self.position += move_dir * self.speed * time.dt

        # Gravity
        self.velocity_y += self.gravity * time.dt
        if self.velocity_y < self.terminal:
            self.velocity_y = self.terminal

        # Pre-move downward sweep to prevent tunneling
        dy = self.velocity_y * time.dt
        if dy < 0:
            ray_origin = self.world_position + Vec3(0, self.skin, 0)
            sweep = abs(dy) + self.ground_snap
            hit = raycast(ray_origin, direction=self.down, distance=sweep, ignore=[self])
            if hit.hit:
                # Land on ground
                self.y = hit.world_point.y
                self.velocity_y = 0
                self.on_ground = True
            else:
                # No ground within sweep; apply full move
                self.y += dy
                self.on_ground = False
        else:
            # Moving up or stationary: apply move
            self.y += dy
            # Gentle ground snap if very close and not ascending fast
            ray_origin = self.world_position + Vec3(0, self.skin, 0)
            hit = raycast(ray_origin, direction=self.down, distance=self.ground_snap, ignore=[self])
            if hit.hit and self.velocity_y <= 0.1:
                self.y = hit.world_point.y
                self.on_ground = True
            else:
                self.on_ground = False

        # Jump
        if held_keys['space'] and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False

        # Kill plane
        if self.y < self.kill_y:
            self.position = Vec3(self.spawn_point)
            self.velocity_y = 0


# =============================
# MAIN
# =============================
def main():
    app = Ursina()

    window.title = "Indoor Mario Test"
    window.color = color.rgb(120, 160, 200)

    # Environment
    create_indoor_environment()
    create_furniture()

    # Lighting
    PointLight(position=(0, 6, -2), color=color.white)
    AmbientLight(color=color.rgba(200, 200, 200, 0.5))

    # Player
    Mario(position=(0, 2, 0))

    Sky(color=color.rgb(200, 200, 200))  # soft indoor light

    app.run()


if __name__ == '__main__':
    main()
