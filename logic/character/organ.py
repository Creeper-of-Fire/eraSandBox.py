from typing import List, Dict, Optional

from logic.character import character, modifier
from logic.data import file_parser, data_process


class OrganAdmin:
    model: str  # 角色的器官模板，比如human

    master: Optional['character.Character']

    def __init__(self):
        self.model = 'human'
        self.all_organs: Dict[str, Organ] = {}

    def set_default(self, master: Optional['character.Character'], model: str):
        self.model = model
        self.master = master
        struct_data = file_parser.open_file('器官结构', model)
        # 种族默认器官结构
        '''insert_data = file_parser.open_file('插入结构', model)'''
        self.all_organs['全身'] = Organ()
        self.all_organs['全身'].set_default('全身', self, struct_data)
        '''self._set_default_insert_structure(insert_data)'''

    def data_default(self, organ_data: Dict[
        str,
        Dict[str, Dict[str, str or int or float or Dict[str, Dict[str, str or int or float]]]]
    ]):
        for i in self.all_organs:
            if i in organ_data:
                self.all_organs[i].data_default(organ_data[i])

    def settle(self):
        a = self.all_organs
        for i in a:
            a[i].settle()

    def append_organ(self, key, val):
        """
        :type key: str
        :type val: Organ
        """
        self.all_organs[key] = val

    def get_organ(self, key):
        if key in self.all_organs:
            return self.all_organs[key]
        else:
            return self.null_organ()

    @staticmethod
    def null_organ():
        a = Organ()
        return a

    '''def _set_default_insert_structure(self,insert_data):
        object_inserts: Dict[str, A.i.object_insert] = {}
        for i in self.all_organs:
            self.all_organs[i].object_insert = A.i.object_insert()
            self.all_organs[i].object_insert.set_default(self.master, self.all_organs[i])
            object_inserts[i] = self.all_organs[i].object_insert
            #提取的是引用
        
        A.i.load_map(insert_data['位点连接'], object_inserts)
        #初始化，然后连接
    
    def insert_able_organ_list(self)-> List[A.i.object_insert]:
        organ_list: List[A.i.object_insert] = []
        for i in self.all_organs['外界'].object_insert.points:
            for j in i.toward:
                organ_list.append(j.object_at)
        return organ_list
    
    def insert_able_point_list(self) -> List[A.i.object_insert_point]:
        list: List[A.i.object_insert_point] = []
        for i in self.all_organs['外界'].object_insert.points:
            for j in i.toward:
                list.append(j)
        return list'''


# 一个角色的organ参与组成以下几种数据结构：
# 解剖学树——有序树，是最主要的树，用处：创建成员，进行数据关联，显示给玩家
# 通道网——一个图，用处：构成让人插入的结构
class Organ:
    name: str
    num_data: Dict[str, int or float]
    add_val_temp: Dict[str, int or float]
    str_data: Dict[str, str]
    # 直接显示给玩家的数据
    o_admin: OrganAdmin
    # 本质上，一个角色的所有的organ都是存储在一个一层的dict里面的，以方便外部直接调用彼此
    modifiers: modifier.ModifierAdmin
    # 每个organ会有属于自己的修正
    # low_list: List[Organ]
    # 每个organ有它下属organ的指针
    '''object_insert: act.object_insert
    #一个镜像器官，掌管插入类'''

    def __init__(self):
        self.name = ''
        self.num_data = {
            # '等级': 0,#似乎等级应该单独出来
            '经验': 0,
            '技巧': 0,
            '敏感': 0,
            '痛苦': 0,
            '扩张': 0,  # 扩张值，只影响扩张
            '快感': 0,
            '破坏': 0,
            '欲望': 0,
        }
        self.add_val_temp = {}
        for i in self.num_data:
            self.add_val_temp[i] = self.num_data[i] + 0
        self.str_data = {}
        # 初始化相关的数据，即使在战斗中它们也会起作用
        self.o_admin = OrganAdmin()
        self.modifiers = modifier.ModifierAdmin()
        self.low_list: List[Organ] = []
        '''self.object_insert = A.i.object_insert()'''

    def set_default(self, name: str, o_admin: OrganAdmin, struct_data: Dict[str, any]):
        self.name = name  # 读取来自外部的名字
        self.o_admin = o_admin  # 传递自己所在的dict
        self._struct_default(struct_data[name])  # 进行器官结构的默认配置

    def data_default(self,
                     organ_data: Dict[
                         str,
                         Dict[str, str or int or float or Dict[str, Dict[str, str or int or float]]]
                     ]
                     ):
        # 为上级结构增加的属性会流到如果存在该属性的下级结构中
        if organ_data is None:
            return

        if not (self.name in organ_data):
            return

        data = organ_data[self.name]
        for key in self.num_data:
            self.num_data[key] = self.num_data[key] + data_process.process_load_data(data[key])

        for key in self.str_data:
            self.str_data[key] = data_process.process_load_data(data[key])

        if '修正' in data:
            self.modifiers.set_default(data['修正'])

    def _struct_default(self, struct_data):
        if struct_data is None:
            return
        # 结构树的默认值
        for key in struct_data:
            og = Organ()
            # 创建下属organ
            og.set_default(key, self.o_admin, struct_data)
            # 初始化下级organ
            self.o_admin.append_organ(key, og)
            # 向admin添加
            self.low_list.append(og)
            # 向自己的下级添加

    # 希望少用
    def get(self, key: str):
        if key in self.num_data:
            return self.get_num(key)
        elif key in self.str_data:
            return self.get_str(key)
        else:
            return None

    def set(self, key: str, val):
        # 只有设置时才使用
        if key in self.num_data:
            self.num_data[key] = int or float(val)
        elif key in self.str_data:
            self.str_data[key] = str(val)
        else:
            return

    # 字符串处理
    def get_str(self, key: str) -> str:
        if key in self.str_data:
            return self.str_data[key]
        else:
            return ''

    def set_str(self, key: str, val: str):
        self.str_data[key] = val

    # 数字处理部分，num_data相关
    def _sum_all(self):
        for i in self.num_data:
            self.__sum_num(i)

    def __sum_num(self, key: str):
        # 汇总
        if len(self.low_list) != 0:
            for i_low in self.low_list:
                i_low.__sum_num(key)

            for i_low in self.low_list:
                self.num_data[key] = self.num_data[key] + i_low.get_num(key)
            # 不经过modifier加成地加，但是get_num还是被加成了

    def get_num(self, key: str) -> int or float:
        if key in self.num_data:
            self.__sum_num(key)
            g = self.modifiers.add_get(key, self.num_data[key])
            return g
        else:
            return 0

    def add_num_temp(self, key: str, val: int or float):
        # self.__sum_num(key)
        a = self.modifiers.add_alt(key, val)  # 获得加成
        self.add_val_temp[key] = self.add_val_temp[key] + a

    def settle(self):
        self.modifiers.time_pass()
        if '时间冻结' in self.modifiers.names:
            return

        for i in self.num_data:
            self._settle_key(i)

    def _settle_key(self, key: str):
        b = self.add_val_temp
        if b[key] == 0:
            return

        a = self.num_data
        a[key] = a[key] + b[key]
        self.__sum_num(key)
        add_val = self.add_val_temp[key]
        self.__add_num(key, add_val)

    def __add_num(self, key: str, val: int or float):
        part = len(self.low_list)
        if part == 0:
            self.num_data[key] = self.num_data[key] + val
        else:
            for i_part in self.low_list:  # type
                add_val = val / part  # 未经过加权，直接分配
                i_part.__add_num(key, add_val)

    def destruction(self) -> float:
        # 破坏度，最大100，会查找自己的下级器官，得到破坏度上限
        part = 0
        val = 0
        self.__sum_num('破坏 ')
        if len(self.low_list) == 0:
            part = 1
        else:
            for i in self.low_list:
                part = part + 1
                val = val + i.destruction()
        dt = self.num_data['破坏'] / part
        return dt
