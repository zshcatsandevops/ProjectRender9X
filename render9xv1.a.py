from ursina import *
from ursina.prefabs.primitives import *

def create_peach_castle():
    # Base structure
    base = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(255, 200, 200),
        scale=(20, 4, 20),
        position=(0, 2, 0)
    )
    
    # Main tower base
    tower_base = Entity(
        model='cylinder',
        texture='white_cube',
        color=color.rgb(255, 180, 180),
        scale=(6, 4, 6),
        position=(0, 6, 0)
    )
    
    # Main tower
    tower = Entity(
        model='cylinder',
        texture='white_cube',
        color=color.rgb(255, 150, 150),
        scale=(4, 12, 4),
        position=(0, 10, 0)
    )
    
    # Tower top section
    tower_top = Entity(
        model='cylinder',
        texture='white_cube',
        color=color.rgb(255, 200, 200),
        scale=(4.5, 2, 4.5),
        position=(0, 18, 0)
    )
    
    # Tower roof (cone)
    roof = Entity(
        model='cone',
        texture='white_cube',
        color=color.rgb(255, 100, 100),
        scale=(5, 6, 5),
        position=(0, 22, 0)
    )
    
    # Gold star on top (iconic element)
    star = Entity(
        model='sphere',
        color=color.yellow,
        scale=(1.5, 0.3, 1.5),
        position=(0, 25.5, 0)
    )
    
    # Side towers (4 corners)
    for x in [-8, 8]:
        for z in [-8, 8]:
            # Tower base
            side_base = Entity(
                model='cube',
                texture='white_cube',
                color=color.rgb(255, 180, 180),
                scale=(3, 2, 3),
                position=(x, 3, z)
            )
            
            # Side tower
            side_tower = Entity(
                model='cylinder',
                texture='white_cube',
                color=color.rgb(255, 150, 150),
                scale=(2, 8, 2),
                position=(x, 7, z)
            )
            
            # Side tower top
            side_top = Entity(
                model='cylinder',
                texture='white_cube',
                color=color.rgb(255, 200, 200),
                scale=(2.2, 1, 2.2),
                position=(x, 11, z)
            )
            
            # Side roof
            side_roof = Entity(
                model='cone',
                texture='white_cube',
                color=color.rgb(255, 100, 100),
                scale=(2.5, 3, 2.5),
                position=(x, 13, z)
            )
    
    # Main entrance
    entrance = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(255, 180, 180),
        scale=(6, 5, 4),
        position=(0, 2.5, -10)
    )
    
    # Entrance arch
    entrance_arch = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(255, 150, 150),
        scale=(4, 3, 2),
        position=(0, 3.5, -10.5)
    )
    
    # Remove the center of the arch to create an opening
    entrance_hole = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(0, 0, 0),
        scale=(2.5, 2, 1.1),
        position=(0, 3.5, -10.8)
    )
    
    # Bridge to entrance
    bridge = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(200, 150, 100),
        scale=(6, 0.5, 10),
        position=(0, 0.25, -5)
    )
    
    # Moat (using a flat cylinder)
    moat = Entity(
        model='cylinder',
        texture='white_cube',
        color=color.blue,
        scale=(25, 0.1, 25),
        position=(0, -0.5, 0)
    )
    
    # Windows on main tower
    for y in [8, 12, 16]:
        window = Entity(
            model='circle',
            color=color.blue,
            scale=(0.8, 0.8, 0.8),
            position=(0, y, -4.1),
            rotation_x=90
        )
    
    # Decorative elements on base
    for i in range(8):
        angle = i * 45
        x = 10 * math.cos(math.radians(angle))
        z = 10 * math.sin(math.radians(angle))
        decoration = Entity(
            model='cube',
            texture='white_cube',
            color=color.rgb(255, 180, 180),
            scale=(1, 2, 1),
            position=(x, 3, z)
        )

def create_surroundings():
    # Create some trees around the castle
    for i in range(12):
        angle = i * 30
        distance = 30
        x = distance * math.cos(math.radians(angle))
        z = distance * math.sin(math.radians(angle))
        
        # Tree trunk
        trunk = Entity(
            model='cylinder',
            color=color.rgb(101, 67, 33),
            scale=(1, 3, 1),
            position=(x, 1.5, z)
        )
        
        # Tree foliage
        foliage = Entity(
            model='sphere',
            color=color.green,
            scale=(3, 3, 3),
            position=(x, 4, z)
        )
    
    # Path from bridge
    path = Entity(
        model='cube',
        texture='white_cube',
        color=color.rgb(200, 180, 140),
        scale=(6, 0.2, 30),
        position=(0, 0.1, -20)
    )

def main():
    app = Ursina()
    
    # Set up camera
    camera.position = (30, 20, -30)
    camera.rotation_y = 30
    camera.rotation_x = 20
    
    # Create ground
    ground = Entity(
        model='plane',
        texture='white_cube',
        color=color.green,
        scale=(100, 1, 100),
        position=(0, -1, 0)
    )
    
    # Create castle
    create_peach_castle()
    
    # Create surroundings
    create_surroundings()
    
    # Add sky
    Sky()
    
    # Add light
    sun = DirectionalLight()
    sun.look_at(Vec3(1, -1, -1))
    
    # Add first-person controls for exploration
    EditorCamera()
    
    app.run()

if __name__ == '__main__':
    main()
