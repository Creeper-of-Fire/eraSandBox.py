from typing import List, Dict, Optional

import copy

from logic.actor import character, modifier
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


def copy_dict_num(x: Dict[str, int or float]):
    y = {}
    for key, value in x.items():
        y[key] = copy.copy(value)
    return y


class NumData:
    modifiers: modifier.ModifierAdmin
    # 每个organ会有属于自己的修正
    low_list: List[Optional['Organ']]

    # 每个organ有它下属organ的指针

    def __init__(self):
        self.modifiers = modifier.ModifierAdmin()
        self.low_list: List[Organ] = []

        self.level = 0
        self.exp = 0
        self.skill = 0
        self.sensibility = 0
        self.pain = 0
        self.expand = 0
        self.delight = 0
        self.destruction = 0
        self.lust = 0

        self._shown_data = {'等级': self.level,  # 似乎等级应该单独出来
                            '经验': self.exp,
                            '技巧': self.skill,
                            '敏感': self.sensibility,
                            '痛苦': self.pain,
                            '扩张': self.expand,  # 扩张值，只影响扩张
                            '快感': self.delight,
                            '破坏': self.destruction,
                            '欲望': self.lust,
                            }
        self._temp_data = copy_dict_num(self._shown_data)
        self._base_data = copy_dict_num(self._shown_data)

    def __getitem__(self, item: str):
        return self._shown_data[item]

    def __setitem__(self, key: str, value: int):
        self._shown_data[key] = value

    def __iter__(self):
        return self._shown_data.__iter__()

    def __add__(self, other) -> Optional['NumData']:
        a: Dict = self._shown_data
        # noinspection PyProtectedMember
        b: Dict = other._shown_data
        c = NumData()
        for i in self._shown_data:
            c[i] = a[i] + b[i]
        return c

    def __sub__(self, other):
        a: Dict = self._shown_data
        # noinspection PyProtectedMember
        b: Dict = other._shown_data
        c = NumData()
        for i in self._shown_data:
            c[i] = a[i] - b[i]
        return c

    def copy(self):
        c = NumData()
        c._shown_data = self._shown_data.copy()
        return c

    def settle_num(self):  # 回合结束时的数据总结
        if '时间冻结' not in self.modifiers.names():
            return
        s = self._shown_data
        b = self._base_data
        m = self.modifiers
        for key, value in s.items():
            value -= b[key]  # 获得本回合的原始加值（这里定义了运算符）
            # noinspection PyUnusedLocal
            value = m.add_alt(key, value)
            # 通过修正计算实际加值（为了效率而在总结时进行）
        self._temp_data = copy_dict_num(s)  # self._num_temp用于获得口上
        for key, value in b.items():
            b += s[key]
            s[key] += m.add_get(key, value)
            # 通过修正获得显示值的加值


class StrData:
    _data: Dict[str, str]

    def __init__(self):
        self.name = ''

        self._data = {
            '名字': self.name,
        }
        # 希望只在初始化时使用self._shown_data

    def __getitem__(self, item: str):
        return self._data[item]

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __iter__(self):
        return self._data.__iter__()


# 一个角色的organ参与组成以下几种数据结构：
# 解剖学树——有序树，是最主要的树，用处：创建成员，进行数据关联，显示给玩家
# 通道网——一个图，用处：构成让人插入的结构
class Organ:
    name: str
    _num_data: NumData
    _num_shown: NumData
    _num_temp: NumData
    _str_data: StrData
    # 直接显示给玩家的数据
    o_admin: OrganAdmin
    # 本质上，一个角色的所有的organ都是存储在一个一层的dict里面的，以方便外部直接调用彼此

    '''object_insert: act.object_insert
    #一个镜像器官，掌管插入类'''

    def __init__(self):
        self.name = ''
        self._num_data = NumData()
        self._str_data = StrData()
        # 初始化相关的数据，即使在战斗中它们也会起作用
        self.o_admin = OrganAdmin()

        '''self.object_insert = A.i.object_insert()'''

    @property
    def num_data(self) -> NumData:
        return self._num_data  # 每个回合，将self._num_shown用于展示和加算

    def _settle_num(self):  # 回合结束时的数据总结
        self.num_data.settle_num()
        '''if '时间冻结' not in self.modifiers.names():
            return
        num_data_add = self._num_shown - self._num_data  # 获得本回合的原始加值（这里定义了运算符）
        for key in num_data_add:
            num_data_add[key] = self.modifiers.add_alt(key, num_data_add[key])
            # 通过修正计算实际加值（为了效率而在总结时进行）
        self._num_temp = num_data_add.copy()  # self._num_temp用于获得口上
        for key in num_data_add:
            num_data_add[key] = self.modifiers.add_get(key, self._num_data[key])
            # 通过修正获得显示值的加值
        self._num_shown += num_data_add'''

        # 字符串处理

    @property
    def str_data(self):
        return

    '''def get_str(self, key: str) -> str:
        if key in self._str_data:
            return self._str_data[key]
        else:
            return ''

    def set_str(self, key: str, val: str):
        self._str_data[key] = val'''

    @property
    def modifiers(self):
        return self._num_data.modifiers

    @property
    def low_list(self):
        return self._num_data.low_list

    def set_default(self, name: str, o_admin: OrganAdmin, struct_data: Dict[str, any]):
        self.name = name  # 读取来自外部的名字
        self.o_admin = o_admin  # 传递自己所在的dict
        self._struct_default(struct_data[name])  # 进行器官结构的默认配置

    def data_default(self, organ_data):
        """
        :type organ_data: Dict[ str, Dict[str, str or int or float or Dict[str, Dict[str, str or int or float]]]]
        """
        # 为上级结构增加的属性会流到如果存在该属性的下级结构中
        if organ_data is None:
            return

        if not (self.name in organ_data):
            return

        data = organ_data[self.name]
        for key in self._num_data:
            self._num_data[key] = self._num_data[key] + data_process.process_load_data(data[key])

        for key in self._str_data:
            self._str_data[key] = data_process.process_load_data(data[key])

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
    '''def get(self, key: str):
        if key in self._num_data:
            return self.get_num(key)
        elif key in self._str_data:
            return self.get_str(key)
        else:
            return None'''

    def set(self, key: str, val):
        # 只有设置时才使用
        if key in self._num_data:
            self._num_data[key] = val
        elif key in self._str_data:
            self._str_data[key] = val
        else:
            return

    # 数字处理部分，num_data相关
    def _sum_all(self):
        for i in self._num_data:
            self._sum_num(i)

    def _sum_num(self, key: str):
        # 汇总
        if len(self.low_list) != 0:
            for i_low in self.low_list:
                i_low._sum_num(key)

            for i_low in self.low_list:
                self._num_data[key] = self._num_data[key] + i_low.get_num(key)
            # 不经过modifier加成地加，但是get_num还是被加成了

    def get_num(self, key: str) -> int or float:
        if key in self._num_data:
            self._sum_num(key)
            g = self.modifiers.add_get(key, self._num_data[key])
            return g
        else:
            return 0

    def add_num_temp(self, key: str, val: int or float):
        # self._sum_num(key)
        a = self.modifiers.add_alt(key, val)  # 获得加成
        self._num_temp[key] = self._num_temp[key] + a

    def settle(self):
        self.modifiers.time_pass()
        if '时间冻结' in self.modifiers.names():
            return
        self._settle_num()

    '''def _settle_num(self):
        for key in self._num_data:
            b = self._num_temp
            if b[key] == 0:
                return
    
            a = self._num_data
            a[key] = a[key] + b[key]
            self._sum_num(key)
            add_val = self._num_temp[key]
            self._add_num(key, add_val)'''

    def _add_num(self, key: str, val: int or float):
        part = len(self.low_list)
        if part == 0:
            self._num_data[key] = self._num_data[key] + val
        else:
            for i_part in self.low_list:  # type
                add_val = val / part  # 未经过加权，直接分配
                i_part._add_num(key, add_val)

    def destruction(self) -> float:
        # 破坏度，最大100，会查找自己的下级器官，得到破坏度上限
        part = 0
        val = 0
        self._sum_num('破坏 ')
        if len(self.low_list) == 0:
            part = 1
        else:
            for i in self.low_list:
                part = part + 1
                val = val + i.destruction()
        dt = self._num_data['破坏'] / part
        return dt
