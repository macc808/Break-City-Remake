import os
from config import TILE_SIZE, TILE_IMAGES
from map.wall import FloorTile, Wall, floor_group, wall_group


def load_level_from_txt(path):
    floor_group.empty()
    wall_group.empty()

    if not os.path.exists(path):
        raise FileNotFoundError(f"Level file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        for row_index, raw_line in enumerate(f):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if "," in line:
                tiles = [t.strip() for t in line.split(",") if t.strip() != ""]
            else:
                tiles = [c for c in line if c.strip() != ""]

            for col_index, tile_code in enumerate(tiles):
                try:
                    tile_id = int(tile_code)
                except ValueError:
                    continue

                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if tile_id == 1:
                    image_path = TILE_IMAGES.get(1)
                    if image_path:
                        floor_group.add(FloorTile(image_path, x, y, TILE_SIZE))

                if tile_id == 2:
                    image_path = TILE_IMAGES.get(2)
                    if image_path:
                        floor_group.add(FloorTile(image_path, x, y, TILE_SIZE))

                if tile_id == 3:
                    image_path = TILE_IMAGES.get(3)
                    if image_path:
                        wall_group.add(Wall(image_path, x, y, TILE_SIZE))

                if tile_id == 4:
                    image_path = TILE_IMAGES.get(4)
                    if image_path:
                        floor_group.add(FloorTile(image_path, x, y, TILE_SIZE))
    
                if tile_id == 5:
                    image_path = TILE_IMAGES.get(5)
                    if image_path:
                        floor_group.add(FloorTile(image_path, x, y, TILE_SIZE))
    
    return floor_group, wall_group
