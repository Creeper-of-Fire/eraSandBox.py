from typing import List, Dict

import erajs.api as era
import erajs.engine as engine

import xlrd
import xlwt
import random
import yaml
import re
import json


def open_file(a_type, b_type=''):
    # 请输入以游戏主程序为根目录的目录
    if a_type == '角色配置':
        file_data = load_auto('data/配置表/角色初始/{}.yml'.format(b_type))
    elif a_type == '经历配置':
        file_data = load_auto('data/配置表/经历/经历.yml')
    elif a_type == '口上描述':
        file_data = load_auto('data/配置表/口上预设/描述配置.yml')
    elif a_type == '口上配置':
        file_data = load_auto('data/配置表/口上预设/口上配置.yml')
    elif a_type == '器官结构':
        file_data = load_auto('data/配置表/器官注册/{}.yml'.format(b_type))
    elif a_type == '插入结构':
        file_data = load_auto('data/配置表/器官注册/{}.yml'.format(b_type))
    elif a_type == '修正配置':
        file_data = load_auto('data/配置表/修正/{}.yml'.format(b_type))
    elif a_type == '修正配置':
        file_data = load_auto('data/配置表/动作配置.csv')
    else:
        return None
    return file_data


'''class FileExcl:

    # 读取第一列得到行的索引
    def list_row_index(self):
        row_max = self.sheet.nrows
        row_list = self.sheet.col_values(0, 1, row_max)
        return row_list

    # 读取第一行得到列的索引
    def list_col_index(self):
        col_max = self.sheet.ncols
        col_list = self.sheet.row_values(0, 1, col_max)
        return col_list

    # 读取角色的默认属性(没有报错修复，请把空格填满)
    def get_default_key_value(self, str_row, str_col):
        row_index_list = self.list_row_index()  # 读取第一列得到行的索引
        row_index = row_index_list.index(str_row) + 1
        col_index_list = self.list_col_index()  # 读取第一行得到列的索引
        col_index = col_index_list.index(str_col) + 1
        chara_key_val = self.sheet.row(row_index)[col_index].value
        return chara_key_val

    def __init__(self, book_path, sheet_name):
        self.book = xlrd.open_workbook(book_path)
        self.sheet = self.book.sheet_by_name(sheet_name)


class FileYaml:

    def __init__(self, path):
        # 打开yaml
        file = open(path, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()
        # 将字符串转化为字典或列表
        self.data = yaml.load(file_data)'''


def load_file(path: str, encoding="utf8") -> str:
    file = open(path, 'r', encoding=encoding)
    file_data = file.read()
    return file_data


def load_csv(path: str, encoding="utf8") -> List[List[str]]:
    text = load_file(path, encoding)
    data = []
    for row in re.split('\r?\n', text):
        data.append(row.split(','))
    return data


def load_yaml(path: str, encoding="utf8") -> Dict:
    text = load_file(path, encoding)
    return yaml.load(text)


def load_json(path: str, encoding="utf8") -> Dict:
    text = load_file(path, encoding)
    return json.loads(text)


def load_auto(path: str, encoding="utf8"):
    suffix = re.search('\.(.+)$', path).group()
    if suffix == ".csv":
        return load_csv(path, encoding)
    elif suffix == ".yml":
        return load_yaml(path, encoding)
    elif suffix == ".json":
        return load_json(path, encoding)
    else:
        return load_file(path, encoding)
