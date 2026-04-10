import math


def calculate_distance(x1, y1, x2, y2):
    """Обчислити евклідову відстань між двома точками"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_direction_to_target(from_x, from_y, to_x, to_y):
    """
    Визначити напрямок до цілі.
    
    Args:
        from_x, from_y: Поточна позиція
        to_x, to_y: Позиція цілі
    
    Returns:
        str: Напрямок ("up", "down", "left", "right")
    """
    dx = to_x - from_x
    dy = to_y - from_y
    
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    
    # Якщо напрямок горизонтальний важливіший
    if abs_dx > abs_dy:
        return "right" if dx > 0 else "left"
    else:
        return "down" if dy > 0 else "up"


def calculate_angle(from_x, from_y, to_x, to_y):
    """
    Обчислити кут між двома точками в градусах (0-360).
    
    Args:
        from_x, from_y: Поточна позиція
        to_x, to_y: Позиція цілі
    
    Returns:
        float: Кут в градусах
    """
    dx = to_x - from_x
    dy = to_y - from_y
    
    # atan2 повертає радіани, конвертуємо в градуси
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    
    # Нормалізуємо до 0-360 діапазону
    return (angle_deg + 360) % 360


def get_perpendicular_direction(primary_direction):
    """
    Отримати перпендикулярний напрямок.
    Використовується для кружління біля цілі.
    
    Args:
        primary_direction: Основний напрямок ("up", "down", "left", "right")
    
    Returns:
        str: Перпендикулярний напрямок
    """
    perpendicular_map = {
        "up": "right",
        "down": "left",
        "left": "up",
        "right": "down"
    }
    return perpendicular_map.get(primary_direction, "right")
