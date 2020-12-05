from typing import Dict, List

from logic.data import file_parser, data_process


class ModifierAdmin(object):
    def __init__(self):
        self.modifiers: Dict[str, Modifier] = {}

    def set_default(self, data: Dict[str, Dict[str, str or Union[int, float]]]):
        if data is None:
            return
        for i in data:
            for j in data[i]:
                a = data_process.process_load_data(data[i][j])
                if a != 0:
                    self.add_modifier(j, i)

    def add_modifier(self, name: str, s_type: str):
        b = self.type(s_type)
        self.modifiers[name] = b()
        self.modifiers[name].set_default(name)

    def time_pass(self, past_time=1):
        a = self.modifiers
        if '时间冻结' in a:
            a['时间冻结'].time_pass(past_time)
            if a['时间冻结'].timer == 0:
                del a['时间冻结']
        for i in list(a.keys()):
            b = a[i]
            b.time_pass(past_time)
            if b.timer == 0:
                del a[i]

    def remove_modifier(self, name):
        a = self.modifiers
        a.pop(name)

    def addition_when_get_value(self, key: str, val: Union[int, float]):
        """
        相当于自带的数据，在回合末会计算并加到临时数据中
        """

        def __g_add(chara, _key: str):
            add = 0
            for i in chara.modifiers:
                if _key in chara.modifiers[i].get_add:
                    add = add + chara.modifiers[i].get_add[_key]
            return add

        def __g_mlt(chara, _key: str):
            mlt = 1
            for i in chara.modifiers:
                if _key in chara.modifiers[i].get_mlt:
                    mlt = mlt * chara.modifiers[i].get_mlt[_key]
            return mlt

        if len(dir(self.modifiers)) == 0:  # 如果修正是空，不知道这样对不对
            return val
        # add_get是在get时提供修正，不影响原值
        a = (val + __g_add(self, key)) * __g_mlt(self, key)
        return a

    def addition_when_alt_by_act(self, key: str, val: Union[int, float]) -> Union[int, float]:
        """每个回合加上去的数据会成为临时数据，在回合结束时转变为加值"""

        def __a_add(chara, _key: str) -> Union[int, float]:
            add = 0
            for i in chara.modifiers:
                if _key in chara.modifiers[i].alt_add:
                    add = add + chara.modifiers[i].alt_add[_key]
            return add

        def __a_mlt(chara, _key: str) -> Union[int, float]:
            mlt = 1
            for i in chara.modifiers:
                if _key in chara.modifiers[i].alt_mlt:
                    mlt = mlt * chara.modifiers[i].alt_mlt[_key]
            return mlt

        # add_alt是在每回合结束时提供修正,对于加上去的值，会得到加成
        if len(dir(self.modifiers)) == 0:  # 如果修正是空，不知道这样对不对
            return val
        a = (val + __a_add(self, key)) * __a_mlt(self, key)
        return a

    def add_end(self, key: str, val: Union[int, float]):
        def __e_add(chara, _key: str):
            add = 0
            for i in chara.modifiers:
                if _key in chara.modifiers[i].end_add:
                    add = add + chara.modifiers[i].end_add[_key]
            return add

        def __e_mlt(chara, _key: str):
            mlt = 1
            for i in chara.modifiers:
                if _key in chara.modifiers[i].end_mlt:
                    mlt = mlt * chara.modifiers[i].end_mlt[_key]
            return mlt

        # add_alt是在每回合结束时提供修正,对于加上去的值，会得到加成
        if len(dir(self.modifiers)) == 0:  # 如果修正是空，不知道这样对不对
            return val
        a = (val + __e_add(self, key)) * __e_mlt(self, key)
        return a

    def names(self) -> List[str]:
        a: List[str] = []
        for i in self.modifiers:
            a.append(i)
        return a

    @staticmethod
    def type(val: str):
        a = {
            'modifier': Modifier,
            'attach': Attach,
            'destruction': Destruction,
            'insert': Insert,
            'experience': Experience,
        }
        if val in a:
            return a[val]
        else:
            # console.log('modifier_type_error when auto_set')
            return Modifier


class Modifier(object):
    name: str
    describe: str
    get_add: Dict[str, Union[int, float]]
    get_mlt: Dict[str, Union[int, float]]
    alt_add: Dict[str, Union[int, float]]
    alt_mlt: Dict[str, Union[int, float]]
    timer: int

    def __init__(self):
        self.name = ''
        self.describe = ''
        self.get_add = {}
        self.get_mlt = {}
        self.alt_add = {}
        self.alt_mlt = {}
        self.end_add = {}
        self.end_mlt = {}
        self.timer = -1  # 为负一则是永久的

    def set_default(self, name, timer: int = -1):
        self.name = name
        data = file_parser.open_file('修正配置', self.__class__.__name__)
        if data is None:
            return
        if name in data:
            a = data[name]
            # 傻逼代码
            if 'describe' in a:
                self.describe = a['describe']
            if 'get_add' in a:
                self.get_add = a['g_add']
            if 'get_mlt' in a:
                self.get_mlt = a['g_mlt']
            if 'alt_add' in a:
                self.alt_add = a['a_add']
            if 'alt_mlt' in a:
                self.alt_mlt = a['a_mlt']
            if 'end_add' in a:
                self.end_add = a['e_add']
            if 'end_mlt' in a:
                self.end_mlt = a['e_mlt']

    def time_pass(self, past_time):
        a = self.timer
        if a == -1:
            return
        # 为负一则是永久的
        if past_time >= a:
            self.timer = 0
            return
        self.timer -= past_time

    def work(self):
        pass


class Attach(Modifier):
    def __init__(self):
        super(Attach, self).__init__()

    def contaminate(self):  # 液体沾染
        pass


class Destruction(Modifier):
    def __init__(self):
        super(Destruction, self).__init__()


class Insert(Modifier):
    def __init__(self):
        super(Insert, self).__init__()


class Experience(Modifier):
    def __init__(self):
        super(Experience, self).__init__()
