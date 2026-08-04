import arcade
import random
from entity import Entity
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Enemy(Entity):
    SPRITE_SIZE = 32

    def __init__(self, scale: float = 2.0, speed: float = 2.0, max_health: int = 999):
        super().__init__('../sprites/Ninja/ninja_idle.png', scale, speed, max_health)

        self.facing_right = True
        self.current_frame = 0
        self.frame_timer = 0.0
        self.frame_speed = 0.08

        self.idle_textures = self._load_atlas('../sprites/Ninja/ninja_idle.png', 11)
        self.run_textures  = self._load_atlas('../sprites/Ninja/ninja_run.png',  12)
        self.jump_textures = self._load_atlas('../sprites/Ninja/ninja_jump.png',  1)
        self.fall_textures = self._load_atlas('../sprites/Ninja/ninja_fall.png',  1)
        self.current_textures = self.idle_textures

        self.damage = 1
        self.hit_cooldown = 0.0
        self.is_on_ground = False
        self.jump_speed = 12.0
        self.jumps_remaining = 1

        self._edge_sensor = arcade.SpriteSolidColor(4, 8, arcade.color.RED)

        self.center_x = random.randint(100, SCREEN_WIDTH - 100)
        self.center_y = 400

    def _load_atlas(self, path: str, frame_count: int):
        sheet = arcade.texture.spritesheet.SpriteSheet(path)
        textures = []
        s = self.SPRITE_SIZE
        for i in range(frame_count):
            rect = arcade.LRBT(i * s, i * s + s, 0, s)
            tex_r = sheet.get_texture(rect)
            sheet.flip_left_right()
            tex_l = sheet.get_texture(rect)
            sheet.flip_left_right()
            textures.append((tex_r, tex_l))
        return textures

    def _update_edge_sensor(self):
        offset = (self.width / 2 + 4) * (1 if self.facing_right else -1)
        self._edge_sensor.center_x = self.center_x + offset
        self._edge_sensor.center_y = self.bottom - 4

    def _should_jump(self, walls):
        self._update_edge_sensor()
        hits = arcade.check_for_collision_with_list(self._edge_sensor, walls)
        return len(hits) == 0

    def _chase(self, player):
        if player.center_x > self.center_x:
            self.change_x = self.speed
            self.facing_right = True
        elif player.center_x < self.center_x:
            self.change_x = -self.speed
            self.facing_right = False
        else:
            self.change_x = 0

    def jump(self):
        if self.is_on_ground and self.jumps_remaining > 0:
            self.change_y = self.jump_speed
            self.is_on_ground = False
            self.jumps_remaining -= 1

    def update(self, delta_time: float = 1/60, player=None, walls=None):
        if self.hit_cooldown > 0:
            self.hit_cooldown -= delta_time

        if player:
            self._chase(player)

            if walls and self.is_on_ground and self._should_jump(walls):
                self.jump()

            if self.is_on_ground and player.center_y > self.center_y + 80:
                self.jump()

        self._animate(delta_time)

    def _animate(self, delta_time):
        if self.change_y > 0:
            new_tex = self.jump_textures
        elif self.change_y < 0:
            new_tex = self.fall_textures
        elif self.change_x != 0:
            new_tex = self.run_textures
        else:
            new_tex = self.idle_textures

        if new_tex is not self.current_textures:
            self.current_textures = new_tex
            self.current_frame = 0

        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_textures)

        direction = 0 if self.facing_right else 1
        self.texture = self.current_textures[self.current_frame][direction]

    def on_hit_player(self, player) -> bool:
        if self.hit_cooldown <= 0:
            player.score -= self.damage
            self.hit_cooldown = 1.0
            return True
        return False


class PinkMan(Enemy):
    def __init__(self, scale: float = 2.0, speed: float = 1.2, max_health: int = 999):
        super().__init__(scale, speed, max_health)

        self.idle_textures = self._load_atlas('../sprites/PinkMan/pinkman_idle.png', 11)
        self.run_textures  = self._load_atlas('../sprites/PinkMan/pinkman_run.png',  12)
        self.jump_textures = self._load_atlas('../sprites/PinkMan/pinkman_jump.png',  1)
        self.fall_textures = self._load_atlas('../sprites/PinkMan/pinkman_fall.png',  1)
        self.current_textures = self.idle_textures
        self.texture = self.idle_textures[0][0]

    def _teleport(self):
        self.center_x = random.randint(100, SCREEN_WIDTH - 100)
        self.center_y = 400
        self.change_x = 0
        self.change_y = 0

    def on_hit_player(self, player) -> bool:
        if self.hit_cooldown <= 0:
            player.score -= self.damage
            self._teleport()
            self.hit_cooldown = 0.5
            return True
        return False