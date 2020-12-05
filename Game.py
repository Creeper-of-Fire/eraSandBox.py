#!/usr/bin/python3
from typing import List, Optional

import erajs.api as era

from logic.act import environment
from logic.actor import character


class CharacterAdmin(object):
    charalist: List[Optional['character.Character']]
    master: Optional['character.Character']
    assist: Optional['character.Character']
    target: Optional['character.Character']
    player: Optional['character.Character']
    choose: Optional['character.Character']

    def __init__(self) -> None:
        self.charalist = []
        null_chara = character.Character()
        self.add_chara(null_chara)
        null_chara.set_default(0, 'NULL')
        # 添加空角色
        self.master = self.charalist[0]
        self.assist = self.charalist[0]
        self.target = self.charalist[0]
        self.player = self.charalist[0]
        self.choose = self.charalist[0]

    def num(self) -> int:
        # 注意，去掉了一个空角色
        num: int = len(self.charalist) - 1
        return num

    def add_chara(self, temp_chara: Optional['character.Character']) -> None:
        temp_chara.id = self.num() + 1
        self.charalist.append(temp_chara)
        self._re_list()
        self.error_fix()

    def del_chara(self, id: int) -> None:
        self.charalist.pop(id)
        self._re_list()

    def get_chara(self):
        return

    def _re_list(self) -> None:
        for i in range(0, self.num() + 1):
            self.charalist[i].id = i

    def error_fix(self) -> None:
        if self.num() != 0:
            if self.master.id == 0:
                self.master = self.charalist[1]

            if self.target.id == 0:
                self.target = self.charalist[1]

            if self.player.id == 0:
                self.player = self.charalist[1]

    def names(self, start: int, end: int = None):
        if end is None:
            end = len(self.charalist) - 1
        a = []
        for i in range(start, end):
            a.append(self.charalist[i].str_data.name)
        return a


# 以后会移除

version = 'Beta 0.0.2'

'''class MainData:
    def __init__(self):
        try:
            self.characters = era.data['chara']
            self.environment_focus = era.data['environment_focus']
        except:
            
            self.characters = era.data['chara']
            self.environment_focus = era.data['environment_focus']'''


def ui_title():
    era.page()
    era.h('eraEQC RE:dream v' + version)
    era.t('with Era.js v' + era.version)
    era.t()
    era.t()
    era.b('华灯初上', era.goto, ui_start_game, popup='开始游戏')
    era.t()
    era.t()
    era.b('晨光熹微', era.exit, popup='退出游戏')


def ui_start_game():
    era.page()
    era.h('夜幕降临')
    era.t()
    era.t('有些倦意了呢')
    era.t()
    era.t('今天会梦见些什么呢？')
    era.t()
    era.t()
    era.b('一枕槐安', era.goto, ui_start_new_game, popup='不同于往前的梦')
    era.t()
    era.b('前尘旧梦', era.goto, ui_start_old_game, popup='以往梦境的延续')
    era.t()
    era.b('事了无痕', era.back, popup='什么都没有记住')


def ui_start_new_game():
    def set_new_game_difficulty(num: int):
        # setup.game_difficulty(num)
        era.goto(ui_start_new_game_set)

    era.page()
    era.h('不同于往前的梦境')
    era.t()
    era.t('会是些什么呢？')
    era.t()
    era.b('桃红色的春梦', set_new_game_difficulty, 1,
          popup='简单地开始游戏',
          color='pink',
          )
    era.t()
    era.b('雪青色的寤梦', set_new_game_difficulty, 2,
          popup='普通的游戏体验',
          color='violet',
          disabled=True,
          )
    era.t()
    era.b('刈安色的迷梦', set_new_game_difficulty, 3,
          popup='也许会有些困难',
          color='yellow',
          disabled=True,
          )
    era.t()
    era.b('月白色的狂梦', set_new_game_difficulty, 4,
          popup='极具挑战的模式',
          disabled=True,
          )
    era.t()
    era.b('苍蓝的捕梦网', era.back,
          popup='什么都没有记得',
          color='blue',
          )


def ui_start_old_game():
    era.page()
    era.show_save_to_load(ui_main)
    era.t()
    era.t()
    era.b('苍蓝的捕梦网', era.back,
          popup='什么都没有记得',
          color='blue',
          )


def ui_start_new_game_set():
    era.page()

    def start_new_game():
        ui_make_chara('玩家')

    era.data['chara'] = CharacterAdmin()

    era.b('梦境的开端', era.goto, start_new_game, popup='进行玩家属性设置')


def ui_make_chara(character_type='玩家'):
    def set_temp(key_value):
        temp.str_data[key_name] = key_value

    def make_input(k_str: str):
        # noinspection PyShadowingNames
        key_name = k_str
        era.t(str(k_str) + ':  ')
        era.input(set_temp, str(temp.str_data[key_name]))
        era.t()

    def go_next():
        temp.ctrl_able = True
        era.data['chara'].add_chara(temp)
        era.goto(ui_main)
        # 页面

    def ui_make_chara_1():
        # 显示属性
        era.page()
        make_input('名字')
        era.b('确定', go_next)

    key_name = ''
    temp = character.Character()
    temp.set_default(1, character_type)
    era.goto(ui_make_chara_1)


def ui_main():
    def target_choose(target: str):
        c.target = c.charalist[int(target[1])]
        era.goto(ui_main)

    def main_save_game():
        era.page()
        era.h('保存游戏')
        # data.save()
        era.show_save_to_save()
        era.b('返回', era.back)

    def main_load_game():
        era.page()
        era.h('读取游戏')
        era.show_save_to_load(load_goto)
        era.b('返回', era.back)

    def load_goto():
        era.data['chara'] = character.Character()
        # data.load()
        era.goto(ui_main)

    def target_info(id) -> str:
        info = '[' + str(id) + ']' + str(c.charalist[id].str_data.name)
        return info

    def charalist_infos() -> List[str]:
        infos: List[str] = []
        for i in c.charalist:
            infos.append(target_info(i.id))

        return infos

    c: CharacterAdmin = era.data['chara']  # 一个常驻的对象，类的全称是character_admin
    era.page()
    c.error_fix()
    era.t('主人' + c.master.str_data.name)
    era.t()
    era.t('助手' + c.assist.str_data.name)
    era.t()
    era.t('目标' + c.target.str_data.name)
    # era.t()
    # era.t('查看角色：')
    # era.dropdown(chara_list_infos(), target_choose, target_info(c.target.id))
    era.t()
    era.b('召唤角色', era.goto, ui_make_chara)
    if c.target.id == 1:
        era.b('自慰', era.goto, ui_make_love)
    else:
        era.b('调教角色', era.goto, ui_make_love)

    era.b('保存进度', era.goto, main_save_game)
    era.b('读取进度', era.goto, main_load_game)
    era.b('返回标题', era.goto, ui_title)


def ui_make_love():
    def train_start():
        era.clear()
        era.page()
        era.data['environment_focus'].time_pass()
        era.goto(ui_turn_focus)

    c = era.data['chara'].charalist
    era.page()
    train = environment.Site()
    era.data['environment_focus'] = train

    i: character.Character
    for i in c:
        if i.id != 0:
            train.add_chara(i)
            i.environment = train
    era.t('xxx了xxx，然后xxx')
    era.t()
    era.b('开始', era.goto, train_start)


def ui_turn_focus():
    def turn_prepare():
        era.page()
        era.goto(ui_turn_focus)

    a = era.data
    era.clear_gui()
    era.data['environment_focus'].turn()
    era.b('下一回合', era.goto, turn_prepare)
    era.b('结束', era.goto, ui_main)


if __name__ == "__main__":  # 程序入口
    try:
        era.init()  # 初始化引擎
        era.goto(ui_start_new_game_set)  # 进入游戏封面
    except Exception:
        pass
