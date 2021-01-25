# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

# Имортируем модули стандартной библиотеки.
import os, sys
# Импортируем модули XBMC.
import xbmcgui, xbmcaddon

# Создаем экземпляр класса Addon для доступа к параметрам плагина.
# Если имя плагина в xbmcaddon.Addon() явно не указано,
# мы получаем параметры текущего плагина.
_addon = xbmcaddon.Addon()
# Получаем путь к плагину.
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())

# Коды клавиатурных комманд.
ACTION_PREVIOUS_MENU = 10 # Esc
ACTION_NAV_BACK = 92 # Backspace

# Параметр выравнивания текста.
ALIGN_CENTER = 6

# Указываем пути к картинкам и текстурам:
# фон;
background_img = os.path.join(_addon_path, 'images', 'SKINDEFAULT.jpg')
# текстура кнопки без фокуса;
button_nf_img = os.path.join(_addon_path, 'images', 'KeyboardKeyNF.png')
# текстура кнопки в фокусе;
button_fo_img = os.path.join(_addon_path, 'images', 'KeyboardKey.png')
# танцующий банан чисто для прикола :-).
banana_img = os.path.join(_addon_path, 'images', 'banana.gif')

class MyAddon(xbmcgui.Window):

    def __init__(self):
        # Создаем экземпляр класса Dialog для доступа к диалогам.
        self.dialog = xbmcgui.Dialog()
        # Устанавливаем фоновую картинку.
        background = xbmcgui.ControlImage(1, 1, 1280, 720, background_img)
        self.addControl(background)
        # Размещаем картинку с бананом.
        banana_picture = xbmcgui.ControlImage(500, 200, 256, 256, banana_img)
        self.addControl(banana_picture)
        # Создаем интерактивные контролы (кнопки).
        self.set_controls()
        # Настраиваем навигацию между контролами.
        self.set_navigation()

    def set_controls(self):
        # Кнопка "Привет".
        self.privet_btn = xbmcgui.ControlButton(500, 500, 110, 40, u'Привет…', focusTexture=button_fo_img,
                                                        noFocusTexture=button_nf_img, alignment=ALIGN_CENTER)
        self.addControl(self.privet_btn)
        # Кнопка "Выход".
        self.exit_btn = xbmcgui.ControlButton(650, 500, 110, 40, u'Выход', focusTexture=button_fo_img,
                                                        noFocusTexture=button_nf_img, alignment=ALIGN_CENTER)
        self.addControl(self.exit_btn)

    def set_navigation(self):
        # Назначаем соседние контролы для кнопки "Привет".
        self.privet_btn.controlRight(self.exit_btn)
        self.privet_btn.controlLeft(self.exit_btn)
        # Назначаем соседние контролы для кнопки "Выход".
        self.exit_btn.controlRight(self.privet_btn)
        self.exit_btn.controlLeft(self.privet_btn)
        # Устанавливаем первоначальный фокус на кнопку "Привет".
        self.setFocus(self.privet_btn)

    def onAction(self, action):
        # Обрабатываем нажатия кнопок для выхода из плагина.
        if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
            self.close()

    def onControl(self, control):
        # Обрабатываем активированные контролы.
        # Если активирована кнопка "Привет"...
        if control == self.privet_btn:
            # ...выводим диалоговое окно с надписью и кнопкой ОК.
            self.dialog.ok(u'Привет, мир!', u'Я рад тебя видеть :-)')
        # Если активирована кнопка "Выход", выходим из плагина.
        elif control == self.exit_btn:
            self.close()

if __name__ == '__main__':
    addon = MyAddon()
    addon.doModal()
    del addon
