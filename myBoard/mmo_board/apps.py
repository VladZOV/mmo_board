from django.apps import AppConfig


class BoardConfig(AppConfig):
    name = 'mmo_board'

    def ready(self):
        import mmo_board.signals
