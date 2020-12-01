from typing import Dict, List
from logic.character import organ, modifier, experience, equipment
from logic.act import act_admin, environment
from logic.data import file_parser, data_process


class Character:
    id: int
    type: str
    ctrl_able: bool
    acts: act_admin  # 动作控制
    modifiers: modifier.ModifierAdmin  # 修正管理
    organs: organ.OrganAdmin  # 器官管理（主要的数据）
    equipments: equipment.EquipmentAdmin  # 装备管理
    experiences: experience.ExperienceAdmin  # 经验管理（不知道有什么用
    environment: environment  # 所在环境
    num_data: Dict[str, int or float]
    str_data: Dict[str, str]
    add_val_temp: Dict[str, int or float]

    def __init__(self):
        self.id = 0
        self.type = 'NULL'  # 角色的类型，比如“玩家”
        self.ctrl_able = True

        self.acts = act_admin.ActAdmin()
        self.modifiers = modifier.ModifierAdmin()
        self.organs = organ.OrganAdmin()
        self.equipments = equipment.EquipmentAdmin()
        self.experiences = experience.ExperienceAdmin()
        self.environment = environment.Environment()
        self.num_data = {
            '最大体力': 0,
            '体力': 0,
            '最大精力': 0,
            '精力': 0,
            '行动条': 0,
            '速度': 100,

            '高潮次数': 0,

            '身高': 0,
            '体重': 0,
            '胸围': 0,
            '腰围': 0,
            '臀围': 0,
        }
        # 以后这些数据会变成用函数获取的，方便锯掉腿之类的

        self.add_val_temp = {}
        for i in self.num_data:
            self.add_val_temp[i] = 0

        self.str_data = {
            '名字': '',
            '种族': '',
        }

        # 要展示的数据放在这上面
        # console.log(this)

    def set_default(self, id: int, s_type: str):
        self.id = id
        self.type = s_type
        # self.器官模板 = 器官模板
        data = file_parser.open_file('角色配置', s_type)
        self.__data_default(data['基础'])

        if '修正' in data:
            self.modifiers.set_default(
                data['修正']
            )

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
                self.__data_default(c[i]['基础'])
                if not '器官' in c[i]:
                    continue
                if c[i]['器官'] is None:
                    continue
                self.organs.data_default(c[i]['器官'])

    def __data_default(self, data: Dict[str, str or int or float]):
        if data is None:
            return
        for key in self.num_data:
            if key in data:
                a = data_process.process_load_data(data[key])
                self.num_data[key] = self.num_data[key] + a
            # 注意这里是加号，这是为了进行多次配置而进行的改动

        for key in self.str_data:
            if key in data:
                self.str_data[key] = data_process.process_load_data(data[key])
            # 对于字符串，后面的配置信息会直接覆盖前面的，所以还请注意

    def get(self, key: str) -> str or int or float or None:
        # 希望少用
        if key in self.num_data:
            return self.get_num(key)
        elif key in self.str_data:
            return self.get_str(key)
        else:
            return None

    def set(self, key: str, val: str or int or float) -> None:
        # 只有设置时才使用
        if key in self.num_data:
            self.num_data[key] = val
        elif key in self.str_data:
            self.str_data[key] = val
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
    def get_num(self, key: str) -> int or float:
        if key in self.num_data:
            g = self.modifiers.add_get(key, self.num_data[key])
            return g
        else:
            return 0

    def add_temp(self, key: str, val: int or float):
        a = self.modifiers.add_alt(key, val)
        self.add_val_temp[key] = self.add_val_temp[key] + a

    # character的add_num_temp只加自己的
    def settle(self):
        self.__settle_this()
        self.organs.settle()

    def __settle_this(self):
        self.modifiers.time_pass()
        if '时间冻结' in self.modifiers.names:
            return

        a = self.num_data
        b = self.add_val_temp
        for i in a:
            if b[i] == 0:
                continue

            a[i] = a[i] + b[i]

    # character的settle_num只会总结自己的
    def __speak(self) -> List[str]:
        pass

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

    def search_object(self, name: str):  # -> equipment.Equipment or Character
        a = self.organs.get_organ(name)
        return a
