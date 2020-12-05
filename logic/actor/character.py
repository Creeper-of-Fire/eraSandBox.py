import copy
from typing import Dict, List, Optional

from logic.act import act_admin, environment
from logic.actor import organ, modifier, experience, equipment
from logic.data import file_parser, data_process


class NumData(object):
    data: Dict[str, int]
    modifiers: modifier.ModifierAdmin  # 修正管理

    class Data(object):
        # <editor-fold desc="Data类">
        def __init__(self):
            self.max_physical_power = 0
            self.physical_power = 0
            self.max_spirit_power = 0
            self.spirit_power = 0
            self.action_bar = 0
            self.action_speed = 0

            self.height = 0
            self.weight = 0

            self._data = {'最大体力': self.max_physical_power,
                          '体力': self.physical_power,
                          '最大精力': self.max_spirit_power,
                          '精力': self.spirit_power,
                          '行动条': self.action_bar,
                          '行动速度': self.action_speed,

                          '身高': self.height,
                          '体重': self.weight}

        def __getitem__(self, item: str):
            return self._data[item]

        def __setitem__(self, key: str, value: int):
            self._data[key] = value

        def __iter__(self):
            return self._data.__iter__()

        def __add__(self, other):
            a: Dict = self._data
            # noinspection PyProtectedMember
            b: Dict = other._data
            c = NumData.Data()
            for i in self._data:
                c[i] = a[i] + b[i]
            return c

        def __sub__(self, other):
            a: Dict = self._data
            # noinspection PyProtectedMember
            b: Dict = other._data
            c = NumData.Data()
            for i in self._data:
                c[i] = a[i] - b[i]
            return c

        def copy(self):
            def copy_dict_num(x: Dict[str, int or float]):
                y = {}
                for key, value in x.items():
                    y[key] = copy.copy(value)
                return y

            c = NumData.Data()
            c._data = copy_dict_num(self._data)
            return c
        # </editor-fold>

    def __init__(self):
        self.modifiers = modifier.ModifierAdmin()
        self._shown_data = NumData.Data()
        self._add_data = NumData.Data()
        self._base_data = NumData.Data()

    def settle_num(self):
        """
        回合结束时的数据总结
        """
        if '时间冻结' not in self.modifiers.names():
            return
        shown = self._shown_data
        base = self._base_data
        add = self._add_data
        m = self.modifiers
        for key in shown:
            base[key] += m.addition_when_alt_by_act(key, add[key])
            shown[key] = m.addition_when_alt_by_act(key, base[key])
            add[key] = 0

    def __getitem__(self, item: str):
        return self._base_data[item]

    def __setitem__(self, key: str, value: int):
        self._base_data[key] = value

    def __iter__(self):
        return self._base_data.__iter__()

    def copy(self):
        c = NumData()
        c.modifiers = self.modifiers
        c._base_data = self._base_data.copy()
        return c

    # <editor-fold desc="# ---------setter和getter--------- #">
    @property
    def max_physical_power(self):
        """最大体力"""
        return self._shown_data.max_physical_power

    @max_physical_power.setter
    def max_physical_power(self, val):
        """最大体力"""
        self._add_data.max_physical_power = val

    @property
    def physical_power(self):
        """体力"""
        return self._shown_data.physical_power

    @physical_power.setter
    def physical_power(self, val):
        """体力"""
        self._add_data.physical_power = val

    @property
    def max_spirit_power(self):
        """最大精力"""
        return self._shown_data.max_spirit_power

    @max_spirit_power.setter
    def max_spirit_power(self, val):
        """最大精力"""
        self._add_data.max_spirit_power = val

    @property
    def spirit_power(self):
        """精力"""
        return self._shown_data.spirit_power

    @spirit_power.setter
    def spirit_power(self, val):
        """精力"""
        self._add_data.spirit_power = val

    @property
    def action_bar(self):
        """行动条"""
        return self._shown_data.action_bar

    @action_bar.setter
    def action_bar(self, val):
        """行动条"""
        self._add_data.action_bar = val

    @property
    def action_speed(self):
        """行动速度"""
        return self._shown_data.action_speed

    @action_speed.setter
    def action_speed(self, val):
        """行动速度"""
        self._add_data.action_speed = val

    @property
    def height(self):
        """身高"""
        return self._shown_data.height

    @height.setter
    def height(self, val):
        """身高"""
        self._add_data.height = val

    @property
    def weight(self):
        """体重"""
        return self._shown_data.weight

    @weight.setter
    def weight(self, val):
        """体重"""
        self._add_data.weight = val

    # </editor-fold>


class StrData(object):
    """简单的字符串数据存储，内部定义了一些枚举方法什么的"""
    _data: Dict[str, str]

    def __init__(self):
        self.name = ''
        self.race = ''

        self._data = {
            '名字': self.name,
            '种族': self.race,
        }
        '''希望只在初始化时使用self._base_data，平时请直接获取'''

    def __getitem__(self, item: str):
        return self._data[item]

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __iter__(self):
        return self._data.__iter__()


class Character(object):
    """Character是负责人物的类.
    它含有一个角色的器官、基础数据、装备、人生经历、AI（对动作的管理和抉择）

    Attributes:
        id: int，对于所有角色的统一编码，主要是玩家收集的角色
        _formwork: str，该角色初始化时使用的模板，例如”玩家“，目前只在初始化时使用
        ctrl_able: bool，该角色是否可以控制
        acts: ActAdmin，动作控制，具有简单的AI
        organs: OrganAdmin，器官管理，最主要的数据
        equipments: EquipmentAdmin，角色身上的装备，没有完工
        experiences: ExperienceAdmin，经验管理，不知道有什么用
        #environment: Environment，应该是用于标记的，目前没啥用
        _num_data: NumData，用于管理角色的所有数字型数据
        _str_data: StrData，用于管理字符串类型的数据
    """

    def __init__(self):
        """这个项目的大部分初始化函数都只是单纯地初始化出了一些容器，
        然后通过set_default函数设置默认值\n
        """
        self.id = 0
        '''对于所有角色的统一编码，主要是玩家收集的角色'''
        self._formwork = 'NULL'
        '''该角色初始化时使用的模板，例如”玩家“，目前只在初始化时使用'''
        self.ctrl_able = False
        '''该角色是否可以控制'''
        self.acts = act_admin.ActAdmin()
        '''动作控制，具有简单的AI'''
        self.organs = organ.OrganAdmin()
        '''器官管理，最主要的数据'''
        self.equipments = equipment.EquipmentAdmin()
        '''角色身上的装备，没有完工'''
        # TODO 装备系统
        self.experiences = experience.ExperienceAdmin()
        # TODO 经历系统
        self.environment = environment.Environment()
        # TODO 这里的environment有点问题

        self._num_data = NumData()
        self._str_data = StrData()

        self._num_data.action_speed = 100

    # ---------setter和getter--------- #
    @property
    def modifiers(self):
        return self.num_data.modifiers

    @property
    def num_data(self) -> NumData:
        return self._num_data  # 每个回合，将self._num_shown用于展示和加算

    @property
    def str_data(self):
        return self._str_data  # 字符串处理

    # ---------setter和getter--------- #

    def set_default(self, id: int, formwork: str):
        """通过外部文件设置默认值，因为经历系统的存在，会进行多次设置.\n
        Args：
            id: 角色的id \n
            formwork: 角色创建依据的模板
        """
        self.id = id
        self._formwork = formwork
        data = file_parser.open_file('角色配置', formwork)
        # 读取文件

        self._data_default(data['基础'])
        # 基础数据的默认值

        if '修正' in data:
            self.modifiers.set_default(data['修正'])
        # 修正的默认值

        self.organs.set_default(self, data['器官模板'])
        if '器官' in data:
            self.organs.data_default(data['器官'])
        # 器官的默认值

        self.equipments.set_default(formwork)
        # 装备的默认值

        if '经历' in data:
            # 利用经历，再进行一次加载
            self.experiences.set_default(data['经历'])  # 经历的默认值
            for i_exp in self.experiences.data_list.values():
                self.modifiers.set_default(i_exp['修正'])  # 添加修正的时候，是利用了字典的特性来覆盖了之前的修正
                self._data_default(i_exp['基础'])
                if not ('器官' in i_exp):
                    continue
                if i_exp['器官'] is None:
                    continue
                self.organs.data_default(i_exp['器官'])

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
        """只有设置时才使用，平时请勿使用，以后会进行更换"""
        # TODO 角色设置系统
        if key in self._num_data:
            self._num_data[key] = val
        elif key in self._str_data:
            self._str_data[key] = val
        else:
            return

    def settle(self):
        """自身行动结束时或者特殊情况触发时，把临时属性变为永久属性、进行口上演出等"""
        self.modifiers.time_pass()
        self._num_data.settle_num()
        self.organs.settle()

    def _speak(self) -> List[str]:
        """输出口上"""
        pass

    def search_object(self, name: str) -> equipment.Equipment or Optional['Character']:
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
            a = self.modifiers.addition_when_alt_by_act(key, val)
            self._num_temp[key] = self._num_temp[key] + a
        @property
        def num_data(self):
            temp_num_data = NumData()
            for key in temp_num_data:
                temp_num_data[key] = self.modifiers.addition_when_get_value(key, self._num_data[key])
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
