import pygame
import os
from logger import Logger


class SoundManager:
    """Менеджер для управління звуками та музикою в грі"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.sounds = {}
        self.music_playing = False
        self.bg_music_volume = 0.3
        self.sfx_volume = 0.7
        
        # Ініціалізуємо mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Виділяємо окремі канали для вистрілів
        pygame.mixer.set_num_channels(8)  # 8 каналів
        self.player_shoot_channel = pygame.mixer.Channel(0)  # Канал 0 для вистрілів гравця
        self.enemy_shoot_channel = pygame.mixer.Channel(1)   # Канал 1 для вистрілів ворогів
        
        # Завантажуємо звуки
        self._load_sounds()
        
        Logger().log_message(self.__init__, "SoundManager initialized")
    
    def _load_sounds(self):
        """Завантажити всі звукові файли"""
        sound_files = {
            'shoot': 'assets/sounds/shot.mp3',
            'win': 'assets/sounds/win.mp3',
            'lose': 'assets/sounds/lose.mp3',
            'bg_music': 'assets/music/mus.mp3',
        }
        
        for sound_name, file_path in sound_files.items():
            try:
                if sound_name == 'bg_music':
                    # Для музики просто зберігаємо шлях
                    self.sounds[sound_name] = file_path
                    Logger().log_message(self._load_sounds, f"Music loaded: {sound_name}")
                else:
                    # Для звукових ефектів завантажуємо їх
                    if os.path.exists(file_path):
                        self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                        Logger().log_message(self._load_sounds, f"Sound loaded: {sound_name}")
                    else:
                        Logger().log_message(self._load_sounds, f"Sound file not found: {file_path}")
            except Exception as e:
                Logger().log_message(self._load_sounds, f"Error loading {sound_name}: {e}")
    
    def play_sound(self, sound_name, volume=None):
        """Грати звуковий ефект"""
        if sound_name not in self.sounds:
            Logger().log_message(self.play_sound, f"Sound not found: {sound_name}")
            return
        
        try:
            sound = self.sounds[sound_name]
            if isinstance(sound, pygame.mixer.Sound):
                if volume is None:
                    volume = self.sfx_volume
                sound.set_volume(volume)
                sound.play()
                Logger().log_message(self.play_sound, f"Playing sound: {sound_name}")
        except Exception as e:
            Logger().log_message(self.play_sound, f"Error playing sound {sound_name}: {e}")
    
    def play_shoot_sound(self, volume=0.5):
        """Грати звук вистрілу гравця з автоматичним зупиненням попередніх звуків"""
        if 'shoot' not in self.sounds:
            Logger().log_message(self.play_shoot_sound, "Sound 'shoot' not found")
            return
        
        try:
            sound = self.sounds['shoot']
            if isinstance(sound, pygame.mixer.Sound):
                # Зупиняємо попередній звук вистрілу на каналі гравця
                self.player_shoot_channel.stop()
                # Встановлюємо гучність та грають звук на виділеному каналі
                sound.set_volume(volume)
                self.player_shoot_channel.play(sound)
                Logger().log_message(self.play_shoot_sound, "Playing player shoot sound on dedicated channel")
        except Exception as e:
            Logger().log_message(self.play_shoot_sound, f"Error playing shoot sound: {e}")
    
    def play_enemy_shoot_sound(self, volume=0.4):
        """Грати звук вистрілу ворога з автоматичним зупиненням попередніх звуків"""
        if 'shoot' not in self.sounds:
            Logger().log_message(self.play_enemy_shoot_sound, "Sound 'shoot' not found")
            return
        
        try:
            sound = self.sounds['shoot']
            if isinstance(sound, pygame.mixer.Sound):
                # Зупиняємо попередній звук вистрілу на каналі врага
                self.enemy_shoot_channel.stop()
                # Встановлюємо гучність та грають звук на виділеному каналі
                sound.set_volume(volume)
                self.enemy_shoot_channel.play(sound)
                Logger().log_message(self.play_enemy_shoot_sound, "Playing enemy shoot sound on dedicated channel")
        except Exception as e:
            Logger().log_message(self.play_enemy_shoot_sound, f"Error playing enemy shoot sound: {e}")
    
    def play_music(self, music_name='bg_music', loops=-1):
        """Грати музику (циклічно за замовчуванням)"""
        if music_name not in self.sounds:
            Logger().log_message(self.play_music, f"Music not found: {music_name}")
            return
        
        try:
            music_path = self.sounds[music_name]
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.bg_music_volume)
                pygame.mixer.music.play(loops)
                self.music_playing = True
                Logger().log_message(self.play_music, f"Playing music: {music_name}")
        except Exception as e:
            Logger().log_message(self.play_music, f"Error playing music {music_name}: {e}")
    
    def stop_music(self):
        """Зупинити музику"""
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
            Logger().log_message(self.stop_music, "Music stopped")
        except Exception as e:
            Logger().log_message(self.stop_music, f"Error stopping music: {e}")
    
    def set_music_volume(self, volume):
        """Встановити гучність музики (0.0 - 1.0)"""
        self.bg_music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.bg_music_volume)
        except Exception as e:
            Logger().log_message(self.set_music_volume, f"Error setting music volume: {e}")
    
    def set_sfx_volume(self, volume):
        """Встановити гучність звукових ефектів (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def cleanup(self):
        """Очистити ресурси звуків"""
        try:
            self.stop_music()
            pygame.mixer.stop()
            Logger().log_message(self.cleanup, "SoundManager cleaned up")
        except Exception as e:
            Logger().log_message(self.cleanup, f"Error cleaning up sounds: {e}")
    
    def stop_all_sounds(self):
        """Зупинити ВСІ звукові ефекти (але не музику)"""
        try:
            self.player_shoot_channel.stop()
            self.enemy_shoot_channel.stop()
            # Зупиняємо видимі канали 2-7
            for i in range(2, 8):
                pygame.mixer.Channel(i).stop()
            Logger().log_message(self.stop_all_sounds, "All sound effects stopped")
        except Exception as e:
            Logger().log_message(self.stop_all_sounds, f"Error stopping all sounds: {e}")
    
    def play_victory_sound(self, volume=0.7):
        """Грати звук перемоги з попередньою очисткою всіх інших звуків"""
        try:
            # Очищуємо все перед запуском звуку перемоги
            self.stop_all_sounds()
            self.stop_music()
            
            if 'win' not in self.sounds:
                Logger().log_message(self.play_victory_sound, "Sound 'win' not found")
                return
            
            sound = self.sounds['win']
            if isinstance(sound, pygame.mixer.Sound):
                sound.set_volume(volume)
                sound.play()
                Logger().log_message(self.play_victory_sound, "Playing victory sound")
        except Exception as e:
            Logger().log_message(self.play_victory_sound, f"Error playing victory sound: {e}")
    
    def play_defeat_sound(self, volume=0.7):
        """Грати звук поразки з попередньою очисткою всіх інших звуків"""
        try:
            # Очищуємо все перед запуском звуку поразки
            self.stop_all_sounds()
            self.stop_music()
            
            if 'lose' not in self.sounds:
                Logger().log_message(self.play_defeat_sound, "Sound 'lose' not found")
                return
            
            sound = self.sounds['lose']
            if isinstance(sound, pygame.mixer.Sound):
                sound.set_volume(volume)
                sound.play()
                Logger().log_message(self.play_defeat_sound, "Playing defeat sound")
        except Exception as e:
            Logger().log_message(self.play_defeat_sound, f"Error playing defeat sound: {e}")
