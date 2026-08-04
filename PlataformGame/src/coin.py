import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Coin(arcade.Sprite):
    def __init__(self, sprite: str, scale: float, value: int):
        super().__init__()
        self.scale = scale
        self.value = value
        self.current_frame = 0
        self.frame_timer = 0
        self.FRAME_SPEED = 0.1
        self.textures_list = self._load_atlas('../sprites/Coin_tiles.png', frame_count=6)
        self.texture = self.textures_list[0]

    def _load_atlas(self, path, frame_count):
        sheet = arcade.texture.spritesheet.SpriteSheet(path)
        textures = []
        for i in range(frame_count):
            rect = arcade.LRBT(i * 16, i * 16 + 16, 0, 16)
            textures.append(sheet.get_texture(rect))
        return textures

    def update(self, delta_time: float = 1/60):
        self.frame_timer += delta_time
        if self.frame_timer >= self.FRAME_SPEED:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures_list)
            self.texture = self.textures_list[self.current_frame]


class SpecialCoin(Coin):
    def __init__(self, scale: float):
        super().__init__('../sprites/Coin_tiles.png', scale, value=5)
        import random
        self.change_x = random.choice([-3, 3])
        self.change_y = random.choice([-3, 3])

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left <= 0 or self.right >= SCREEN_WIDTH:
            self.change_x *= -1
        if self.bottom <= 0 or self.top >= SCREEN_HEIGHT:
            self.change_y *= -1

        self.frame_timer += delta_time
        if self.frame_timer >= self.FRAME_SPEED:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures_list)
            self.texture = self.textures_list[self.current_frame]