#!/usr/bin/python
''' Модуль для копирования дополнения

    Копирует дополнение в папку дополнений
    Kodi на данном компьютере
'''

__author__ = 'AlexFdlv@bk.ru (Alex Fdlv)'

import os
import shutil
import sys

if ( __name__ == "__main__" ):
    # !!! После первого копирования, дополнение в коди находится в отключенном состоянии, нужно включить
    # !!! Далее папку можно модифицировать, изменения принимаются без перезагрузки KODI
    
    os.chdir(os.path.realpath(os.path.dirname(sys.argv[0]))) # сменить текущую папку на ту, в которой находится файл этого модуля
    addons_develop_path = os.path.abspath('.')
    addons_local_kodi_path = r'C:\Users\Alex\AppData\Roaming\Kodi\addons'
    remote_path = r'\\PC-INWIN\zeroq\.kodi\addons'

    addons_list = ['script.test']

    for addon_name in addons_list:
        src = os.path.join(addons_develop_path, addon_name)
        dst = os.path.join(addons_local_kodi_path, addon_name)
        shutil.rmtree(dst)
        shutil.copytree(src, dst)

        dst2 = os.path.join(remote_path, addon_name)
        # shutil.rmtree(dst2)
        shutil.copytree(src, dst2)
