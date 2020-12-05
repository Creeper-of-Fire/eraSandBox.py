from typing import List, Dict, Optional

import erajs.api as era

from logic.actor import character


# environment是一个数据和界面交互的层
class Environment(object):
    characters: List[Optional['character.Character']]
    start: List[Union[int, float]]
    action_values: Dict[str, Union[int, float]]
    to_do_chara: List[Optional['character.Character']]

    # items: List[I.ia.item]
    def __init__(self):
        self.characters = []
        self.start = []
        self.action_values = {}
        self.to_do_chara = []
        # self.items = []

    def add_chara(self, temp_chara: Optional['character.Character']):
        # temp_chara.id = len(self.characters)
        self.characters.append(temp_chara)

    def turn(self):
        from Game import ui_turn_focus

        def _search_turn():
            def pare_num(a: character.Character):
                return a.num_data.action_bar

            self.to_do_chara = []
            for i in self.characters:
                if i.num_data.action_bar >= 100:
                    self.to_do_chara.append(i)
            self.to_do_chara.sort(key=pare_num, reverse=True)  # 由大到小排列
            # 选择大于100的而且最大的执行（如果需要输入指令就输入指令），然后执行了的减去100

        def _running():
            def _ctrl_button(*args):
                era.page()
                act = args[0][0]
                chara = args[0][1]
                chara.acts.manual_plan_acts(act)
                chara.acts.work()
                chara.settle()
                era.t(wait=True)
                era.goto(ui_turn_focus)

            _search_turn()
            if len(self.to_do_chara) == 0:
                self.time_pass()
                era.goto(ui_turn_focus)
            for i in self.to_do_chara:
                if i.num_data.action_bar < 100:
                    continue
                i.num_data.action_bar -= 100
                i.acts.set_default(i, self.characters)
                i.acts.check_acts()  # 判断所有可用动作
                if i.ctrl_able:
                    # 对可控制角色，提供选择
                    if i.acts.able_acts != 0:
                        era.page()
                        for a in i.acts.able_acts:
                            era.b(a.name, _ctrl_button, (a, i))
                        era.t()
                else:
                    era.page()
                    i.acts.auto_plan_acts()
                    i.acts.work()
                    i.settle()
                    era.t(wait=True)
                    _running()

        # 不知道这样合不合理，但是我就打算把显示也做在这里了
        _running()

        # 找不到时，本次回合结束
        # 一回合相当于一帧

    def time_pass(self):
        for i in self.characters:
            a = i.num_data
            a.settle_when_turn_check()
            a.action_bar += a.action_speed
            # 在一个回合中，所有操作都是对临时的数据的


'''
class environment 
    #基类
     acts: List[A.aa.act_admin]
     characters: Dict[str, C.character.character ]
     items: List[I.ia.item]
    constructor() 
        self.acts = []
        self.characters = 
        self.items = []
    
    add_chara(character: C.character.character):
        if (!(str(character.id) in self.characters)) 
            self.characters[str(character.id)] = character
            self.characters[str(character.id)].environment = this
        
    
    add_item(item: I.ia.item):  
        self.items.append(item)
    
    set_default():  
        self.acts = [A.aa.act_admin()]
        for (a of self.acts) 
            a.set_default(self.characters)
        
    
    turn_prepare(command?):  
        self._check_acts()
    
    turn_start():  
        #执行瞬间动作，挂载长期动作 
        #长期动作挂载在环境中
    
    turn_process():  
        self._work()
        #长期动作运行
    
    turn_end():  
        #所有时间不停止的角色和器官不进行数据结算
        #流程：
        #数据结算
        #口上处理
        #液体分泌处理
        #特性获得处理
    
    private _work():  
        for (i of self.acts) 
            i.work()
        
    
    _check_acts():  
        for (a of self.acts) 
            a.check_acts()
'''


class Site(Environment):
    def __init__(self):
        super(Site, self).__init__()

    ''' _check_acts():  
        typical = A.aa.act_admin()
        typical.set_default(self.characters)
        self.acts.append(typical)
        #insert = A.i.insert_admin()
        #insert.set_default(self.characters)
        #self.acts.append(insert)
    
    prepare():  '''


class Map(Environment):
    sites: List[Site]

    def __init__(self):
        super(Map, self).__init__()
