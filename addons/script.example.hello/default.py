# -*- coding: utf-8 -*-

import xbmcgui

# Коды клавиатурных действий
ACTION_PREVIOUS_MENU = 10 # По умолчанию - ESC
ACTION_NAV_BACK = 92 # По умолчанию - Backspace


# Главный класс-контейнер
class MyAddon(xbmcgui.Window):

    def __init__(self):
        # Создаем текстовую подпись.
        label = xbmcgui.ControlLabel(550, 300, 200, 50, u'Привет, мир!')
        # Добавляем подпись в контейнер
        self.addControl(label)

    def onAction(self, action):
        # Если нажали ESC или Backspace...
        if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
            # ...закрываем плагин.
            self.close()


if __name__ == '__main__':
    # Создаем экземпляр класса-контейнера.
    addon = MyAddon()
    # Выводим контейнер на экран.
    addon.doModal()
    # По завершении удаляем экземпляр.
    del addon
