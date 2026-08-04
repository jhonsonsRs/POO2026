import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class InstructionsView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            'Instruções',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 80,
            arcade.color.WHITE,
            font_size=36,
            anchor_x='center',
            bold=True
        )

        linhas = [
            'Objetivo: colete todas as moedas para vencer!',
            '',
            'Movimentação:',
            '  A / ← : Mover para a esquerda',
            '  D / → : Mover para a direita',
            '  SPACE  : Pular',
            '',
            'Inimigos:',
            '  Inimigo comum  — patrulha o mapa. Cada colisão remove 1 ponto.',
            '  Inimigo especial — te persegue. Teleporta ao colidir e remove 1 ponto.',
            '',
            'Moeda especial — quica nas bordas e vale 5 pontos.',
            'Moeda comum    — vale 1 ponto.',
            '',
            '[ESC] ou [M] — Voltar ao Menu',
        ]

        for i, linha in enumerate(linhas):
            arcade.draw_text(
                linha,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT - 160 - i * 30,
                arcade.color.LIGHT_GRAY,
                font_size=16,
                anchor_x='center',
            )

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            from menu_view import MenuView
            self.window.show_view(MenuView())