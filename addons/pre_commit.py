#!/usr/bin/python
''' Модуль для формирования репозитория дополнений

    Формирует структуру репозитория
    Копирует необходимые файлы дополнений в репозиторий
    Создает в репозитории zip архив дополнения
    Генерирует необходимые для репозитория хэш суммы файлов
'''

__author__ = 'AlexFdlv@bk.ru (Alex Fdlv)'

import hashlib
import os
import shutil
import sys
import xml.dom.minidom
import zipfile

def read_file(file: str) -> str:
    ''' Чтение текста из файла

        Файл читается в двоичном формате.
        (При чтении в текстовом формате, 
        конец строки автоматически преобразуется 
        в используемый в ОС, т.е., например, LF (\\n)
        при работе модуля в Windows преобразуется
        в CRLF (\\r\\n), что может в дальнейшем
        спровоцировать некоторые проблемы)
        
        Далее данные декодируются в текст.

        Возврат: текст 
    '''
    with open(file, 'rb') as fr:
        return fr.read().decode('utf-8')

def write_file(file: str, data: str):
    ''' Запись текста в файл

        Принятый текст, кодируется в двоичные данные.
        Файл пишется в двоичном формате.
        (При записи в текстовом формате, 
        конец строки автоматически преобразуется 
        в используемый в ОС, т.е., например, LF (\\n)
        при работе модуля в Windows преобразуется
        в CRLF (\\r\\n), что может в дальнейшем
        спровоцировать некоторые проблемы) 
    '''
    with open(file, 'wb') as fw:
        fw.write(data.encode('utf-8'))

def get_hash_md5(file: str) -> str:
    ''' Получение хэш суммы файла

        Файл читается в двоичном формате
        блоками по 8192кб, при каждой итерации
        производится обновление(подсчет)
        хэш суммы методом md5

        Возврат: строка с хэш суммой   
    '''
    with open(file, 'rb') as fr:
        m = hashlib.md5()
        while True:
            data = fr.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def get_addons_list(path: str) -> list:
    ''' Получение списка дополнений в папке

        Список формируется из имен папок, 
        в которых содержится файл addon.xml
        
        Возврат: список имен дополнений (папок с дополнениями)
    '''
    dir_elements = sorted(os.listdir(path))
    addons_list = []
    for item in dir_elements:
        if os.path.isdir(os.path.join(path, item)) and os.path.exists(os.path.join(path, item, 'addon.xml')):
            addons_list.append(item)
    return addons_list

def get_files_for_zip(path: str) -> list :
    ''' Получение списка всех файлов и папок дополнения

        Список формируется из относительных путей
        всех файлов и папок (в т.ч. пустых) содержащихся
        в папке дополнения

        Возврат: список относительных путей всех
        элементов в папке
    '''
    files_for_zip = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if len(os.listdir(os.path.join(root,dir))) == 0:
                files_for_zip.append(os.path.join(root,dir))
        for file in files:
            # if file.startswith(path) or file.endswith(".zip.md5"): continue
            files_for_zip.append(os.path.join(root,file))
    return files_for_zip
    
def get_data_for_addons_xml(path: str) -> str:
    ''' Получение данных для файла addons.xml 
        из файла addon.xml в дополнении

        Из всех данных исключается строка объявления
        xml файла (первая строка).

        Возврат: текст
    '''
    xml_path = os.path.join(path, 'addon.xml')
    addon_xml_lines = read_file(xml_path).splitlines()
    addon_xml_data = ''
    for line in addon_xml_lines:
        if (line.find('<?xml') >= 0 ): continue
        addon_xml_data += line.rstrip() + '\n'
    return addon_xml_data
  
def create_md5_file(filename: str):
    ''' Создание файла md5

        Создается файл .md5 с хэш суммой файла.
        Если хэш сумма подсчитывается для файла zip
        то в md5 записывается хэш сумма и имя файла.   
    '''
    md5_data = get_hash_md5(filename)
    if filename.endswith(".zip"):
        md5_data += '  ' + os.path.basename(filename)
    md5_data += u'\n'
    write_file(filename + '.md5', md5_data)

def create_zip_file(files: list, zip_filename: str):
    ''' Создание архива zip

        Принимает список относительных путей
        файлов для помещения в архив и путь к файлу архива
    '''
    z = zipfile.ZipFile(zip_filename, 'w')
    for file in files:
        z.write(file)  
    z.close()
    create_md5_file(zip_filename)
  
def create_addons_xml_file(path:str, data: str):
    ''' Создание файла addons.xml

        Формирует данные для файла и записывает в файл.    
    '''
    xml_data = u'<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n'
    xml_data += data
    xml_data = xml_data.strip() + u'\n</addons>\n'
    write_file(os.path.join(path, 'addons.xml'), xml_data)
    create_md5_file(os.path.join(path, 'addons.xml'))

def correction_xml_file(path: str):
    ''' Исправление xml файла.

        Удаляет пустые строки,
        удаляет пробелы перед тэгами <?xml  <addon  </addon>
    '''
    
    xml_lines = read_file(os.path.join(path,'addon.xml')).splitlines()
    correct_xml_data = ''
    for line in xml_lines:
        if len(line) == 0: continue
        if (line.find('<?xml') + line.find('<addon') + line.find('</addon>') >= 0): 
            line = line.lstrip()
        correct_xml_data += line.rstrip() + '\n'
    write_file(os.path.join(path,'addon.xml'), correct_xml_data)
    return correct_xml_data

def get_latest_version_zip(path: str) -> str:
    ''' Получение последней версии zip файла в папке

        Извлекает версию из имен файлов всех архивов в папке
        и возвращает максимальную.
        Если версии не найдены, возвращает 0.0.0
    '''
    dir_elements = sorted(os.listdir(path))
    ver_list = ['0.0.0']
    for item in dir_elements:
        if zipfile.is_zipfile(os.path.join(path,item)) and item.startswith(path):
            ver = item.replace(path + '-','')
            ver = ver.replace('.zip','')
            ver_list.append(ver)
    return max(ver_list)

def get_addon_version_from_xml(path: str) -> str:
    ''' Получение версии дополнения из файла addon.xml

        Производится парсинг addon.xml, берется содержимое 
        первого аттрибута version в первом тэге addon

        Возврат: строка с версией
    '''
    dom = xml.dom.minidom.parse(os.path.join(path, 'addon.xml')) 
    dom.normalize()
    tag_addon = dom.getElementsByTagName('addon')[0]
    attr_id = tag_addon.getAttribute('id')
    if attr_id == path:
        attr_version = tag_addon.getAttribute('version')
    return attr_version

def copy_file(src: str, dst: str):
    ''' Копирование файла

        Файл копируется в двух случаях, 
        1. Если файла назначения не существует
        2. Если хэш суммы файла источника и 
           и файла назначения не равны.
    '''
    if os.path.exists(src):
        src_exist = True
    else:
        src_exist = False
    if os.path.exists(dst):
        dst_exist = True
    else:
        dst_exist = False
    if src_exist:
        md5_src = get_hash_md5(src)
    if dst_exist:
        md5_dst = get_hash_md5(dst)
    
    if src_exist:
        if not dst_exist or (src_exist and md5_src !=  md5_dst):
            shutil.copy2(src, dst)


if ( __name__ == "__main__" ):
    os.chdir(os.path.realpath(os.path.dirname(sys.argv[0]))) # сменить текущую папку на ту, в которой находится файл этого модуля
    addons_develop_path = os.path.abspath('.')
    repository_path = os.path.abspath(r'..\repository')
    exclude_addons_list = ['script.develop']
    addons_list = sorted(list(set(get_addons_list(addons_develop_path)) - set(exclude_addons_list)))
    addons_list_in_repo_for_del = list(set(get_addons_list(repository_path)) - set(addons_list))
    for addon_dir in addons_list_in_repo_for_del:
        shutil.rmtree(os.path.join(repository_path, addon_dir))
    copy_files_list = ['addon.xml', 'icon.png', 'fanart.jpg']
    data_for_addons_xml = ''
    for addon_name in addons_list:
        addon_dir_in_repo = os.path.join(repository_path, addon_name)
        if not os.path.exists(addon_dir_in_repo):
            os.makedirs(addon_dir_in_repo)
        for file in copy_files_list:
            file_in_develop = os.path.join(addons_develop_path, addon_name, file)
            file_in_repo = os.path.join(repository_path, addon_name, file)
            copy_file(file_in_develop, file_in_repo)
        addon_version_from_xml = get_addon_version_from_xml(addon_name)
        zip_file = os.path.join(repository_path, addon_name, addon_name + '-' + addon_version_from_xml + '.zip')
        if not os.path.exists(zip_file):
            create_zip_file(get_files_for_zip(addon_name), zip_file)

        data_for_addons_xml += get_data_for_addons_xml(addon_name) + '\n'
    create_addons_xml_file(repository_path, data_for_addons_xml)
