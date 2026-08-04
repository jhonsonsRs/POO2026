import arcade
from PIL import Image, ImageDraw, ImageOps
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


def make_circular_texture(path, size=300):
    img = Image.open(path).convert('RGBA')
    img = ImageOps.fit(img, (size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)
    return arcade.Texture(img)


class AboutView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.avatar = arcade.Sprite(scale=0.4)
        self.avatar.texture = make_circular_texture('../sprites/profile.jpeg')
        self.avatar.center_x = SCREEN_WIDTH / 2
        self.avatar.center_y = SCREEN_HEIGHT / 2 + 20

        self.avatar_list = arcade.SpriteList()
        self.avatar_list.append(self.avatar)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            'Sobre o Jogo',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80,
            arcade.color.WHITE, font_size=36,
            anchor_x='center', bold=True
        )

        arcade.draw_text(
            'Desenvolvido por:',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 140,
            arcade.color.LIGHT_GRAY, font_size=20,
            anchor_x='center',
        )

        self.avatar_list.draw()

        arcade.draw_text(
            'João Emanuel Vieira Orlando',
            SCREEN_WIDTH / 2, self.avatar.bottom - 30,
            arcade.color.WHITE, font_size=20,
            anchor_x='center', bold=True
        )

        arcade.draw_text(
            '[ESC] ou [M] — Voltar ao Menu',
            SCREEN_WIDTH / 2, 60,
            arcade.color.LIGHT_GRAY, font_size=16,
            anchor_x='center',
        )

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            from menu_view import MenuView
            self.window.show_view(MenuView())