from typing import List, Dict, Optional
import erajs.api as era

from logic.character import character


# environment是一个数据和界面交互的层
class Environment:
    characters: List[Optional['character.Character']]
    start: List[int or float]
    action_values: Dict[str, int or float]

    # items: List[I.ia.item]
    def __init__(self):
        self.characters = []
        self.start = []
        self.action_values = {}
        # self.items = []

    def add_chara(self, temp_chara: Optional['character.Character']):
        temp_chara.id = len(self.characters)
        self.characters.append(temp_chara)

    def turn_run(self):
        # 不知道这样合不合理，但是我就打算把显示也做在这里了
        self.__time_pass()
        to_do_list: List[character.Character] = self.__search_turn()
        for i in to_do_list:
            i.acts.set_default(i, self.characters)
            i.acts.check_acts()  # 判断所有可用动作
            if i.ctrl_able:
                # 对可控制角色，提供选择
                for a in i.acts.able_acts:
                    era.b(a.name, i.acts.manual_plan_acts, a)
            else:
                i.acts.auto_plan_acts()
            i.acts.work()

        # 找不到时，本次回合结束
        # 持续运行函数写在game.ts里面，这里只能一次一回合

    def __search_turn(self) -> List[Optional['character.Character']]:
        def pare_num(a: character.Character):
            return a.get_num('行动条')

        to_do_list: List[character.Character] = []
        for i in self.characters:
            if i.get_num('行动条') >= 100:
                to_do_list.append(i)
        to_do_list.sort(key=pare_num, reverse=True)  # 由大到小排列
        return to_do_list
        # 选择大于100的而且最大的执行（如果需要输入指令就输入指令），然后执行了的减去100

    def __time_pass(self):
        for i in self.characters:
            i.set('行动条', i.get_num('速度') + i.get_num('行动条'))


'''/*
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
        
    

*/'''


class Site(Environment):
    def __init__(self):
        super(Site, self).__init__()

    '''/* _check_acts():  
        typical = A.aa.act_admin()
        typical.set_default(self.characters)
        self.acts.append(typical)
        #insert = A.i.insert_admin()
        #insert.set_default(self.characters)
        #self.acts.append(insert)
    
    prepare():  */'''


class Map(Environment):
    sites: List[Site]

    def __init__(self):
        super(Map, self).__init__()
