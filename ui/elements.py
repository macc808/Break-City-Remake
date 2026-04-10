import pygame
from config import WIDTH, HEIGHT


class HealthBar:
    """Відображення здоров'я гравця у вигляді зеленого прямокутника з числом"""
    
    def __init__(self, max_health, x=10, y=10, width=300, height=30):
        """
        Args:
            max_health: Максимальне здоров'я
            x, y: Позиція на екрані
            width, height: Розмір прямокутника здоров'я
        """
        self.max_health = max_health
        self.current_health = max_health  # Ініціалізовано на повне здоров'я
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 24)
    
    def update(self, current_health):
        """Оновити поточне здоров'я"""
        self.current_health = max(0, current_health)
    
    def draw(self, screen):
        """Відобразити прямокутник здоров'я на екрані"""
        # Фоновий темний прямокутник
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        
        # Зелений прямокутник здоров'я (скорочується при пошкодженні)
        health_width = (self.current_health / self.max_health) * self.width
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, health_width, self.height))
        
        # Межа
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)
        
        # Текст здоров'я
        health_text = f"HP: {int(self.current_health)}/{int(self.max_health)}"
        text_surface = self.font.render(health_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.x + 10, self.y + 3))


class PauseButton:
    """Кнопка паузи у правому верхньому кутку"""
    
    def __init__(self, x=None, y=10, width=80, height=40):
        """
        Args:
            x: X позиція (за замовчуванням WIDTH - 100)
            y: Y позиція
            width: Ширина кнопки
            height: Висота кнопки
        """
        self.x = x if x is not None else WIDTH - 100
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(None, 20)
        self.is_hovered = False
    
    def update(self, mouse_pos):
        """Перевірити наведення миші"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, event):
        """Перевірити, чи кнопка була натиснута"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False
    
    def draw(self, screen):
        """Відобразити кнопку на екрані"""
        # Колір залежить від наведення
        button_color = (100, 150, 255) if self.is_hovered else (70, 130, 230)
        
        pygame.draw.rect(screen, button_color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # Текст кнопки
        button_text = "PAUSE"
        text_surface = self.font.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class PauseMenu:
    """Меню паузи з кнопками Продовжити/Вийти"""
    
    def __init__(self, width=WIDTH, height=HEIGHT):
        """
        Args:
            width: Ширина екрану
            height: Висота екрану
        """
        self.width = width
        self.height = height
        self.menu_width = 300
        self.menu_height = 260
        self.menu_x = (width - self.menu_width) // 2
        self.menu_y = (height - self.menu_height) // 2
        
        self.font_title = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 32)
        
        # Кнопки
        self.continue_button = pygame.Rect(self.menu_x + 50, self.menu_y + 80, 200, 40)
        self.menu_button = pygame.Rect(self.menu_x + 50, self.menu_y + 140, 200, 40)
        self.quit_button = pygame.Rect(self.menu_x + 50, self.menu_y + 200, 200, 40)
        
        self.continue_hovered = False
        self.menu_hovered = False
        self.quit_hovered = False
    
    def update(self, mouse_pos):
        """Перевірити наведення на кнопки"""
        self.continue_hovered = self.continue_button.collidepoint(mouse_pos)
        self.menu_hovered = self.menu_button.collidepoint(mouse_pos)
        self.quit_hovered = self.quit_button.collidepoint(mouse_pos)
    
    def handle_click(self, event):
        """Повернути дію при кліку на кнопку"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.continue_hovered:
                return "continue"
            elif self.menu_hovered:
                return "menu"
            elif self.quit_hovered:
                return "quit"
        return None
    
    def draw(self, screen):
        """Відобразити меню паузи на екрані"""
        # Напівпрозорий фон
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Панель меню
        pygame.draw.rect(screen, (50, 50, 50), 
                        (self.menu_x, self.menu_y, self.menu_width, self.menu_height))
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 3)
        
        # Заголовок
        title = self.font_title.render("PAUSE", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.menu_x + self.menu_width // 2, self.menu_y + 25))
        screen.blit(title, title_rect)
        
        # Кнопка Продовжити
        continue_color = (100, 200, 100) if self.continue_hovered else (70, 150, 70)
        pygame.draw.rect(screen, continue_color, self.continue_button)
        pygame.draw.rect(screen, (255, 255, 255), self.continue_button, 2)
        continue_text = self.font_button.render("Continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=self.continue_button.center)
        screen.blit(continue_text, continue_rect)
        
        # Кнопка Меню
        menu_color = (100, 150, 200) if self.menu_hovered else (70, 120, 170)
        pygame.draw.rect(screen, menu_color, self.menu_button)
        pygame.draw.rect(screen, (255, 255, 255), self.menu_button, 2)
        menu_text = self.font_button.render("Menu", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        screen.blit(menu_text, menu_rect)
        
        # Кнопка Вийти
        quit_color = (200, 100, 100) if self.quit_hovered else (150, 70, 70)
        pygame.draw.rect(screen, quit_color, self.quit_button)
        pygame.draw.rect(screen, (255, 255, 255), self.quit_button, 2)
        quit_text = self.font_button.render("Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=self.quit_button.center)
        screen.blit(quit_text, quit_rect)
