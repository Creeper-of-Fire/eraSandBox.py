import copy
from typing import Dict, List, Optional
from logic.actor import organ, modifier, experience, equipment
from logic.act import act_admin, environment
from logic.data import file_parser, data_process


def copy_dict_num(x: Dict[str, int or float]):
    y = {}
    for key, value in x.items():
        y[key] = copy.copy(value)
    return y


class NumData:
    data: Dict[str, int]
    modifiers: modifier.ModifierAdmin  # 修正管理

    def __init__(self):
        self.modifiers = modifier.ModifierAdmin()

        self.max_physical_power = 0
        self.physical_power = 0
        self.max_spirit_power = 0
        self.spirit_power = 0
        self.action_bar = 0
        self.action_speed = 0

        self.height = 0
        self.weight = 0

        self._shown_data = {'最大体力': self.max_physical_power,
                            '体力': self.physical_power,
                            '最大精力': self.max_spirit_power,
                            '精力': self.spirit_power,
                            '行动条': self.action_bar,
                            '行动速度': self.action_speed,
                            '身高': self.height,
                            '体重': self.weight}
        # 希望只在初始化时使用self._base_data
        self._temp_data = copy_dict_num(self._shown_data)
        self._base_data = copy_dict_num(self._shown_data)

    def __getitem__(self, item: str):
        return self._base_data[item]

    def __setitem__(self, key: str, value: int):
        self._base_data[key] = value

    def __iter__(self):
        return self._base_data.__iter__()

    def __add__(self, other) -> Optional['NumData']:
        a: Dict = self._base_data
        # noinspection PyProtectedMember
        b: Dict = other._base_data
        c = NumData()
        for i in self._base_data:
            c[i] = a[i] + b[i]
        return c

    def __sub__(self, other):
        a: Dict = self._base_data
        # noinspection PyProtectedMember
        b: Dict = other._base_data
        c = NumData()
        for i in self._base_data:
            c[i] = a[i] - b[i]
        return c

    def copy(self):
        c = NumData()
        c.modifiers = self.modifiers
        c._base_data = self._base_data.copy()
        return c

    def settle_num(self):  # 回合结束时的数据总结
        if '时间冻结' not in self.modifiers.names():
            return
        s = self._shown_data
        b = self._base_data
        m = self.modifiers
        for key, value in s.items():
            value -= b[key]  # 获得本回合的原始加值（这里定义了运算符）
            value = m.add_alt(key, value)
            # 通过修正计算实际加值（为了效率而在总结时进行）
        self._temp_data = copy_dict_num(s)  # self._num_temp用于获得口上
        for key, value in b.items():
            b += s[key]
            s[key] += m.add_get(key, value)
            # 通过修正获得显示值的加值


'''
    @property
    def max_physical_power(self):
        return

    @max_physical_power.setter
    def max_physical_power(self, val):
        pass

    @property
    def physical_power(self):
        return

    @property
    def max_spirit_power(self):
        return

    @property
    def spirit_power(self):
        return

    @property
    def action_bar(self):
        return

    @property
    def action_speed(self):
        return

    @property
    def height(self):
        return

    @property
    def weight(self):
        return
'''


class StrData:
    _data: Dict[str, str]

    def __init__(self):
        self.name = ''
        self.race = ''

        self._data = {
            '名字': self.name,
            '种族': self.race,
        }
        # 希望只在初始化时使用self._base_data

    def __getitem__(self, item: str):
        return self._data[item]

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __iter__(self):
        return self._data.__iter__()


class Character:
    id: int
    type: str
    ctrl_able: bool
    acts: act_admin.ActAdmin  # 动作控制
    organs: organ.OrganAdmin  # 器官管理（主要的数据）
    equipments: equipment.EquipmentAdmin  # 装备管理
    experiences: experience.ExperienceAdmin  # 经验管理（不知道有什么用
    environment: environment  # 所在环境
    _num_data: NumData
    _num_temp: NumData
    _str_data: StrData

    def __init__(self):
        self.id = 0
        self.type = 'NULL'  # 角色的类型，比如“玩家”
        self.ctrl_able = False

        self.acts = act_admin.ActAdmin()
        self.organs = organ.OrganAdmin()
        self.equipments = equipment.EquipmentAdmin()
        self.experiences = experience.ExperienceAdmin()
        self.environment = environment.Environment()

        self._num_data = NumData()
        '''self._num_shown = NumData()
        self._num_temp = NumData()'''
        self._str_data = StrData()

        self._num_data.action_speed = 100

    # 数字处理部分，num_data相关

    @property
    def modifiers(self):
        return self.num_data.modifiers

    @property
    def num_data(self) -> NumData:
        return self._num_data  # 每个回合，将self._num_shown用于展示和加算

    def _settle_num(self):  # 回合结束时的数据总结
        self._num_data.settle_num()
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

    @property
    def str_data(self):
        return self._str_data  # 字符串处理

    def set_default(self, id: int, s_type: str):
        self.id = id
        self.type = s_type
        # self.器官模板 = 器官模板
        data = file_parser.open_file('角色配置', s_type)
        self._data_default(data['基础'])

        if '修正' in data:
            self.modifiers.set_default(data['修正'])

        self.organs.set_default(self, data['器官模板'])
        if not (data['器官'] is None):
            self.organs.data_default(data['器官'])

        self.equipments.set_default(s_type)
        if '经历' in data:
            # 利用经历，再进行一次加载
            self.experiences.set_default(data['经历'])
            c = self.experiences.data_list
            for i in c:
                self.modifiers.set_default(
                    c[i]['修正']
                )  # 添加修正的时候，是利用了字典的特性来覆盖了之前的修正
                self._data_default(c[i]['基础'])
                if not ('器官' in c[i]):
                    continue
                if c[i]['器官'] is None:
                    continue
                self.organs.data_default(c[i]['器官'])

    def _data_default(self, data: Dict[str, str or int or float]):
        if data is None:
            return
        for key in self._num_data:
            if key in data:
                a = data_process.process_load_data(data[key])
                self._num_data[key] = self._num_data[key] + a
            # 注意这里是加号，这是为了进行多次配置而进行的改动

        for key in self._str_data:
            if key in data:
                self._str_data[key] = data_process.process_load_data(data[key])
            # 对于字符串，后面的配置信息会直接覆盖前面的，所以还请注意

    def set(self, key: str, val: str or int or float) -> None:
        # 只有设置时才使用
        if key in self._num_data:
            self._num_data[key] = val
        elif key in self._str_data:
            self._str_data[key] = val
        else:
            return

    # 回合结束时，把临时属性变为永久属性
    def settle(self):
        self.modifiers.time_pass()
        self._settle_num()
        self.organs.settle()

    def _speak(self) -> List[str]:
        pass

    def search_object(self, name: str):  # -> equipment.Equipment or Character
        a = self.organs.get_organ(name)
        return a

    '''def _settle_num(self):
            if '时间冻结' in self.modifiers.names():
                return
            a = self._num_data
            b = self._num_temp
            for i in a:
                if b[i] == 0:
                    continue
                a[i] = a[i] + b[i]'''
    '''def insert_able_object_list(self) -> List[A.i.object_insert]:
        list_a = self.organs.insert_able_organ_list()
        list_b = self.equipments.insert_able_part_list()
        list = list_a.concat(list_b)
        return list
    def insert_able_point_list(self) -> List[A.i.object_insert_point]:
        list_a = self.organs.insert_able_point_list()
        list_b = self.equipments.insert_able_point_list()
        list = list_a.concat(list_b)
        return list'''
    '''def direct_set_num(self, key: str, val: int or float):
            self._num_data[key] = val
        def add_temp(self, key: str, val: int or float):
            a = self.modifiers.add_alt(key, val)
            self._num_temp[key] = self._num_temp[key] + a
        @property
        def num_data(self):
            temp_num_data = NumData()
            for key in temp_num_data:
                temp_num_data[key] = self.modifiers.add_get(key, self._num_data[key])
            return temp_num_data
        @num_data.setter
        def num_data(self, val):
            pass        '''
    '''def get(self, key: str) -> str or int or float or None:
            # 希望少用
            if key in self._num_data:
                return self.get_num(key)
            elif key in self._str_data:
                return self.get_str(key)
            else:
                return None'''
    '''def get_str(self, key: str) -> str:
            if key in self._str_data:
                return self._str_data[key]
            else:
                return ''

        def set_str(self, key: str, val: str):
            self._str_data[key] = val'''
