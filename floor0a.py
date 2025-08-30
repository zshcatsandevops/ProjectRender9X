# indoor_mario.py — Ursina indoor test level with working Mario controller

from ursina import *
import math


# =============================
# ENVIRONMENT
# =============================
def create_indoor_environment():
    """Creates a closed indoor room (floor, walls, ceiling)."""
    room_size = 30
    wall_height = 10
    wall_thickness = 1

    # Floor at y=0 (top surface)
    floor = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(150, 120, 90),
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

    # Walls
    walls = []
    # North
    walls.append(Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(180, 150, 130),
        scale=(room_size, wall_height, wall_thickness),
        position=(0, wall_height/2, room_size/2),
        collider='box'
    ))
    # South
    walls.append(Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(180, 150, 130),
        scale=(room_size, wall_height, wall_thickness),
        position=(0, wall_height/2, -room_size/2),
        collider='box'
    ))
    # East
    walls.append(Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(180, 150, 130),
        scale=(wall_thickness, wall_height, room_size),
        position=(room_size/2, wall_height/2, 0),
        collider='box'
    ))
    # West
    walls.append(Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(180, 150, 130),
        scale=(wall_thickness, wall_height, room_size),
        position=(-room_size/2, wall_height/2, 0),
        collider='box'
    ))

    return [floor, ceiling] + walls


def create_furniture():
    """Adds simple props inside the room."""
    table = Entity(
        model='cube',
        color=color.rgb(101, 67, 33),
        scale=(4, 1, 4),
        position=(0, 0.5, 0),
        collider='box'
    )

    # Four green columns (decor)
    for i in range(4):
        Entity(
            model='cylinder',
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
        super().__init__(
            model='cube',
            color=color.blue,
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

        # Respawn logic
        self.kill_y = -20
        self.spawn_point = Vec3(self.position)

        # Camera setup
        self.camera_pivot = Entity(parent=self, y=1.5)  # camera follow point
        camera.parent = self.camera_pivot
        camera.position = (0, 3, -8)
        camera.rotation = (15, 0, 0)
        camera.fov = 90

    def update(self):
        # Input direction
        move_dir = Vec3(
            held_keys['d'] - held_keys['a'],
            0,
            held_keys['w'] - held_keys['s']
        )

        if move_dir.length() > 0:
            move_dir = move_dir.normalized()
            self.look_at(self.position + move_dir)
            self.position += self.forward * self.speed * time.dt

        # Gravity
        self.velocity_y += self.gravity * time.dt
        if self.velocity_y < self.terminal:
            self.velocity_y = self.terminal

        # Apply vertical move
        self.y += self.velocity_y * time.dt

        # Ground detection
        ray_origin = self.world_position + Vec3(0, 0.1, 0)
        hit = raycast(ray_origin, direction=self.down, distance=0.2, ignore=[self])

        if hit.hit:
            self.y = hit.world_point.y
            self.velocity_y = 0
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
