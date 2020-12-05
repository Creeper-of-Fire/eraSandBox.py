import copy
from typing import Dict, List, Optional, Union

from logic.act import act_admin, environment
from logic.actor import organ, modifier, experience, equipment
from logic.data import file_parser, data_process


class NumData(object):
    """存储数字数据的类。
    在这个游戏中，运算量的大头在角色AI部分涉及的大量数据处理。

    Attributes:
        _shown_data: 对外Read-only的数据，在内部通过settle_when_turn_check来从_base_data结算
        _base_data: 理论上private的数据，但是能通过__setitem__来修改，通过__getitem__来读取（约定只在初始化时这样做）
        _add_data: 对外Write-only的数据，在内部通过settle_when_turn_end来修改_base_data的数据
        modifiers: 自身的修正，在回合开始结束时都会影响数据
        action_bar: 行动条
    """
    modifiers: modifier.ModifierAdmin  # 修正管理

    class Data(object):
        # <editor-fold desc="Data类">
        def __init__(self):
            """由于这里的数据是基础类，data没有进行引用"""
            self.max_physical_power: int = 0
            self.physical_power: int = 0
            self.max_spirit_power: int = 0
            self.spirit_power: int = 0

            self.action_speed: float = 0

            self.height: float = 0
            self.weight: float = 0

        def _dict_to_data(self, _data: Dict[str, Union[int, float]]):
            """解压dict到数据，通常在进行设置时和回合结束时"""

            if '最大体力' in _data:
                self.max_physical_power = _data['最大体力']
            if '体力' in _data:
                self.physical_power = _data['体力']
            if '最大精力' in _data:
                self.max_spirit_power = _data['最大精力']
            if '精力' in _data:
                self.spirit_power = _data['精力']
            if '行动速度' in _data:
                self.action_speed = _data['行动速度']

            if '身高' in _data:
                self.height = _data['身高']
            if '体重' in _data:
                self.weight = _data['体重']

        def _data_to_dict(self) -> Dict[str, Union[int, float]]:
            """压缩数据到dict"""
            _data = {'最大体力': self.max_physical_power,
                     '体力': self.physical_power,
                     '最大精力': self.max_spirit_power,
                     '精力': self.spirit_power,
                     '行动速度': self.action_speed,

                     '身高': self.height,
                     '体重': self.weight}
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
        self.action_bar = 0
        self._shown_data = NumData.Data()
        self._add_data = NumData.Data()
        self._base_data = NumData.Data()

    def settle_when_turn_end(self):
        """回合结束时的数据总结，主要是计算加值并加上去"""
        m = self.modifiers
        base = self._base_data
        add = self._add_data
        if '时间冻结' not in m.names():
            return
        for key in base:
            base[key] = base[key] + m.addition_when_alt_by_act(key, add[key])
            add[key] = 0

    def settle_when_turn_check(self):
        """回合开始时的加值，主要是计算“临时加值”，从base_data生成shown_data"""
        m = self.modifiers
        shown = self._shown_data
        base = self._base_data
        for key in shown:
            shown[key] = m.addition_when_alt_by_act(key, base[key])

    def __getitem__(self, key: str):
        """可能会降低运行效率"""
        return self._base_data.__getitem__(key)

    def __setitem__(self, key: str, value: Union[int, float]):
        """可能会降低运行效率"""
        self._base_data.__setitem__(key, value)

    def __iter__(self):
        """可能会降低运行效率"""
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

        self._num_data['行动速度'] = 100

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

    def _data_default(self, data: Dict[str, str or Union[int, float]]):
        if data is None:
            return
        for key in self._num_data:
            if key in data:
                a = data_process.process_load_data(data[key])
                self._num_data[key] = a + self._num_data[key]
            # 注意这里是加号，这是为了进行多次配置而进行的改动

        for key in self._str_data:
            if key in data:
                self._str_data[key] = data_process.process_load_data(data[key])
            # 对于字符串，后面的配置信息会直接覆盖前面的，所以还请注意

    def set(self, key: str, val: str or Union[int, float]) -> None:
        """只有设置时才使用，平时请勿使用，以后会进行更换"""
        # TODO 角色设置系统
        if key in self._num_data:
            self._num_data[key] = val
        elif key in self._str_data:
            self._str_data[key] = val
        else:
            return

    def settle_when_turn_end(self):
        """自身行动结束时或者特殊情况触发时，把临时属性变为永久属性、进行口上演出等"""
        self.modifiers.time_pass()
        self._num_data.settle_when_turn_end()
        self.organs.settle_when_turn_end()

    def settle_when_turn_check(self):
        """从base_data生成shown_data，可以随时检测，但是为了效率不应该那样做"""
        self._num_data.settle_when_turn_check()
        self.organs.settle_when_turn_check()

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
    '''def direct_set_num(self, key: str, val: Union[int, float]):
            self._num_data[key] = val
        def add_temp(self, key: str, val: Union[int, float]):
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
    '''def get(self, key: str) -> str or Union[int, float] or None:
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
