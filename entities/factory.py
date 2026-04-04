from entities.enemy import Enemy
from config import img_enemy, TILE_SIZE, SPAWN_POSITIONS, WAVES_CONFIG
from logger import Logger


class WaveManager:
    """Управляет спавнением ворогов по волнам"""
    
    def __init__(self, level=1):
        self.level = level
        self.current_wave = 0
        self.waves = WAVES_CONFIG.get(level, [])
        self.spawn_positions = SPAWN_POSITIONS.get(level, [])
        self.current_wave_enemies = []  # Враги текущей волны
        self.wave_spawned = False
        self.all_waves_completed = False
        
        if self.waves:
            self.should_spawn_next = True  # Первая волна готова к спавну сразу
        else:
            self.should_spawn_next = False
    
    def update(self, dt):
        """Обновить менеджер волн и вернуть список новых врагов для спавна"""
        new_enemies = []
        
        if self.all_waves_completed:
            return new_enemies
        
        # Если нужно спавнить следующую волну
        if self.should_spawn_next and not self.wave_spawned:
            if self.current_wave >= len(self.waves):
                self.all_waves_completed = True
                Logger().logger.info("All waves completed!")
                return new_enemies
            
            # Спавнить всех врагов текущей волны
            wave_config = self.waves[self.current_wave]
            self.current_wave_enemies = []
            
            for enemy_config in wave_config.get("enemies", []):
                spawn_index = enemy_config["spawn_index"]
                ai_type_id = enemy_config["ai_type"]
                
                if spawn_index < len(self.spawn_positions):
                    x, y = self.spawn_positions[spawn_index]
                    # Центрировать врага на позиции
                    enemy_x = x + TILE_SIZE // 2 - 25
                    enemy_y = y + TILE_SIZE // 2 - 15
                    
                    enemy = Enemy(img_enemy, enemy_x, enemy_y, 50, 30, 2, ai_type_id)
                    new_enemies.append(enemy)
                    self.current_wave_enemies.append(enemy)
                    Logger().logger.info(f"Spawned enemy wave {self.current_wave + 1} with AI type {ai_type_id} at ({enemy_x}, {enemy_y})")
            
            self.wave_spawned = True
            self.should_spawn_next = False
            self.current_wave += 1
            
            Logger().logger.info(f"Wave {self.current_wave}/{len(self.waves)} spawned. Waiting for all enemies to be defeated...")
        
        return new_enemies
    
    def update_wave_status(self, alive_enemies):
        """Обновить статус волны на основе живых врагов в игре
        
        Args:
            alive_enemies: Список всех живых врагов на карте
        """
        if not self.wave_spawned or self.all_waves_completed:
            return
        
        # Проверить, живы ли враги текущей волны
        all_dead = True
        for wave_enemy in self.current_wave_enemies:
            if wave_enemy in alive_enemies:
                all_dead = False
                break
        
        # Если все враги волны мертвы, можно спавнить следующую
        if all_dead:
            self.wave_spawned = False
            self.should_spawn_next = True
            Logger().logger.info(f"Wave {self.current_wave} completed! All enemies defeated.")
    
    def get_current_wave(self):
        """Получить номер текущей волны"""
        return self.current_wave
    
    def get_total_waves(self):
        """Получить всего волн"""
        return len(self.waves)
    
    def is_finished(self):
        """Проверить, завершены ли все волны"""
        return self.all_waves_completed


class EnemyFactory:
    """Фабрика для создания врагов"""
    
    @staticmethod
    def create_enemy(ai_type, x, y, width=50, height=30, speed=2):
        """Создать врага с указанным типом ИИ"""
        return Enemy(img_enemy, x, y, width, height, speed, ai_type)
