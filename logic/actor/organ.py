import copy
from typing import List, Dict, Optional, Union

from logic.actor import character, modifier
from logic.data import file_parser, data_process


class OrganAdmin(object):
    model: str  # 角色的器官模板，比如human
    all_organs: Dict[str, Optional['Organ']] = {}
    master: Optional['character.Character']

    def __init__(self):
        self.model = 'human'
        self.all_organs = {}

    def set_default(self, master: Optional['character.Character'], model: str):
        self.model = model
        self.master = master
        struct_data = file_parser.open_file('器官结构', model)
        # 种族默认器官结构
        '''insert_data = file_parser.open_file('插入结构', model)'''
        self.all_organs['全身'] = Organ()
        self.all_organs['全身'].set_default('全身', self, struct_data)
        '''self._set_default_insert_structure(insert_data)'''

    def data_default(self, organ_data):
        """
        :type organ_data: Dict[str, Dict[str, Union[Dict[str,
        Union[str, int, float], Dict[str, Dict[str, Union[str, int, float]]]]]]]
        """
        for i in self.all_organs:
            if i in organ_data:
                self.all_organs[i].data_default(organ_data[i])

    def settle_when_turn_end(self):
        self.all_organs['全身'].settle_when_turn_end()
        # 递归汇总全部的器官（但是可能有时间停止）

    def settle_when_turn_check(self):
        self.all_organs['全身'].settle_when_turn_check()

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

    # <editor-fold desc="insert相关的代码，暂时不使用">
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
    # </editor-fold>


class NumData(object):
    """存储数字数据的类。
    在这个游戏中，运算量的大头在角色AI部分涉及的大量数据处理。

    Attributes:
        _shown_data: 对外Read-only的数据，在内部通过settle_when_turn_check来从_base_data结算
        _base_data: 理论上private的数据，但是能通过__setitem__来修改，通过__getitem__来读取（约定只在初始化时这样做）
        _add_data: 对外Write-only的数据，在内部通过settle_when_turn_end来修改_base_data的数据
        low_list: 下级器官们
        modifiers: 自身的修正，在回合开始结束时都会影响数据
    """
    modifiers: modifier.ModifierAdmin
    # 每个organ会有属于自己的修正
    low_list: List[Optional['Organ']]

    # 每个organ有它下属organ的指针

    class Data(object):
        # <editor-fold desc="Data类">
        def __init__(self):
            self.level: int = 0
            self.exp: int = 0
            self.skill: int = 0
            self.sensibility: float = 0
            self.pain: float = 0
            self.expand: float = 0
            self.delight: float = 0
            self.destruction: float = 0
            self.lust: float = 0

        def _dict_to_data(self, _data: Dict[str, Union[int, float]]):
            """解压dict到数据，通常在进行设置时和回合结束时"""
            if '等级' in _data:
                self.level = _data['等级']
            if '经验' in _data:
                self.exp = _data['经验']
            if '技巧' in _data:
                self.skill = _data['技巧']
            if '敏感' in _data:
                self.sensibility = _data['敏感']
            if '痛苦' in _data:
                self.pain = _data['痛苦']
            if '扩张' in _data:
                self.expand = _data['扩张']
            if '快感' in _data:
                self.delight = _data['快感']
            if '破坏' in _data:
                self.destruction = _data['破坏']
            if '欲望' in _data:
                self.lust = _data['欲望']

        def _data_to_dict(self) -> Dict[str, Union[int, float]]:
            """压缩数据到dict"""
            _data = {'等级': self.level,
                     '经验': self.exp,
                     '技巧': self.skill,
                     '敏感': self.sensibility,
                     '痛苦': self.pain,
                     '扩张': self.expand,
                     '快感': self.delight,
                     '破坏': self.destruction,
                     '欲望': self.lust,
                     }
            return _data

        def __getitem__(self, key: str):
            _data = self._data_to_dict()
            return _data[key]

        def __setitem__(self, key: str, value: Union[int, float]):
            _data = {key: value}
            self._dict_to_data(_data)

        def __iter__(self):
            _data = self._data_to_dict()
            # 改成tuple的性能提高也许并比不上方便性
            return _data.__iter__()

        def copy(self):
            def copy_dict_num(x: Dict[str, Union[int, float]]):
                y = {}
                for key, value in x.items():
                    y[key] = copy.copy(value)
                return y

            c = NumData.Data()
            c._dict_to_data(copy_dict_num(self._data_to_dict()))
            return c
        # </editor-fold>

    def __init__(self):
        self.modifiers = modifier.ModifierAdmin()
        self.low_list = []

        self._add_data = NumData.Data()
        self._shown_data = NumData.Data()
        self._base_data = NumData.Data()

    # <editor-fold desc="# ---------setter和getter--------- #">
    '''@property
    def destruction(self) -> float:
        # 破坏度，最大100，会查找自己的下级器官，得到破坏度上限
        # destruction不应该手动修改，而是应该通过修正来增加
        part = 0
        val = self.modifiers.addition_when_get_value('破坏', 0)
        if len(self.low_list) == 0:
            part = 1
        else:
            for i in self.low_list:
                part = part + 1
                val = val + i.num_data.destruction
        dt = self._base_data.destruction / part
        if self._base_data.destruction > 100:
            self._base_data.destruction = 100
        return dt'''

    @property
    def level(self):
        """等级"""
        return self._shown_data.level

    '''@level.setter
    def level(self, val):
        """等级"""
        self._add_data.level = val'''

    @property
    def exp(self):
        """经验"""
        return self._shown_data.exp

    @exp.setter
    def exp(self, val):
        """经验"""
        self._add_data.exp = val

    @property
    def skill(self):
        """技巧"""
        return self._shown_data.skill

    @skill.setter
    def skill(self, val):
        """技巧"""
        self._add_data.skill = val

    @property
    def sensibility(self):
        """敏感"""
        return self._shown_data.sensibility

    @sensibility.setter
    def sensibility(self, val):
        """敏感"""
        self._add_data.sensibility = val

    @property
    def pain(self):
        """痛苦"""
        return self._shown_data.pain

    @pain.setter
    def pain(self, val):
        """痛苦"""
        self._add_data.pain = val

    @property
    def expand(self):
        """扩张"""
        return self._shown_data.expand

    @expand.setter
    def expand(self, val):
        """扩张"""
        self._add_data.expand = val

    @property
    def delight(self):
        """快感"""
        return self._shown_data.delight

    @delight.setter
    def delight(self, val):
        """快感"""
        self._add_data.delight = val

    @property
    def destruction(self):
        """破坏"""
        return self._shown_data.destruction

    '''@destruction.setter
    def destruction(self, val):
        """破坏"""
        self._add_data.destruction = val'''

    @property
    def lust(self):
        """欲望"""
        return self._shown_data.lust

    @lust.setter
    def lust(self, val):
        """欲望"""
        self._add_data.lust = val

    # </editor-fold>

    def settle_when_turn_end(self):
        """回合结束时的数据总结，主要是计算加值并加上去"""
        m = self.modifiers
        add = self._add_data
        base = self._base_data
        if len(self.low_list) != 0:
            # 先汇总下级器官
            for i_part in self.low_list:
                i_part.settle_when_turn_end()
                for key in add:
                    # noinspection PyProtectedMember
                    add[key] = add[key] + i_part.num_data._add_data[key]
        if '时间冻结' not in m.names():
            return
        for key in base:
            base[key] += m.addition_when_alt_by_act(key, add[key])
            add[key] = 0

    def settle_when_turn_check(self):
        """回合开始时的加值，主要是计算“临时加值”，从base_data生成shown_data"""
        m = self.modifiers
        base = self._base_data
        shown = self._shown_data
        if len(self.low_list) != 0:
            # 先汇总下级器官
            for i_part in self.low_list:
                i_part.settle_when_turn_check()
                for key in shown:
                    shown[key] = shown[key] + i_part.num_data._shown_data[key]
        for key in shown:
            shown[key] = m.addition_when_alt_by_act(key, base[key])

    def _add_num(self, key: str, val: Union[int, float]):
        part = len(self.low_list)
        if part == 0:
            self._shown_data[key] += val
        else:
            for i_part in self.low_list:  # type
                add_val = val / part  # 未经过加权，直接分配
                i_part.num_data._add_num(key, add_val)

    def __getitem__(self, item: str):
        """可能会降低运行效率"""
        return self._shown_data[item]

    def __setitem__(self, key: str, value: int):
        """可能会降低运行效率"""
        self._shown_data[key] = value

    def __iter__(self):
        """可能会降低运行效率"""
        return self._shown_data.__iter__()

    def copy(self):
        c = NumData()
        c._shown_data = self._shown_data.copy()
        return c


class StrData(object):
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
class Organ(object):
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
        # self.object_insert = A.i.object_insert()
        # TODO 插入的完善

    @property
    def num_data(self) -> NumData:
        return self._num_data

    @property
    def str_data(self):
        return

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
        # 未使用
        """
        :type organ_data: Dict[ str, Union[Dict[str,
        Union[str, int, float], Dict[str, Dict[str, Union[str, int, float]]]]]]
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

    # <editor-fold desc="以前的获取代码，现在不用了">
    # 希望少用
    '''def get(self, key: str):
        if key in self._num_data:
            return self.get_num(key)
        elif key in self._str_data:
            return self.get_str(key)
        else:
            return None'''

    # </editor-fold>

    def set(self, key: str, val):
        # 只有设置时才使用
        if key in self._num_data:
            self._num_data[key] = val
        elif key in self._str_data:
            self._str_data[key] = val
        else:
            return

    def settle_when_turn_end(self):
        self.modifiers.time_pass()
        self.num_data.settle_when_turn_end()
        # 在num_data里面进行递归

    def settle_when_turn_check(self):
        self._num_data.settle_when_turn_check()
