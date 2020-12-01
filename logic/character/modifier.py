from typing import Dict, List

from logic.data import file_parser, data_process


class ModifierAdmin:
    def __init__(self):
        self.modifiers: Dict[str, Modifier] = {}

    def set_default(self, data: Dict[str, Dict[str, str or int or float]]):
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
                '''delete a['时间冻结']'''
                pass
        for i in a:
            b = a[i]
            b.time_pass(past_time)
            if b.timer == 0:
                '''delete a[i] #这种删除不知道对不对'''
                pass

    def remove_modifier(self, name):
        a = self.modifiers
        a.pop(name)

    def add_get(self, key: str, val: int or float):
        if len(dir(self.modifiers)) == 0:  # 如果修正是空，不知道这样对不对
            return val

        # add_get是在get时提供修正，不影响原值
        a = (val + self.__g_add(key)) * self.__g_mlt(key)
        return a

    def __g_add(self, key: str):
        add = 0
        for i in self.modifiers:
            if key in self.modifiers[i].get_add:
                add = add + self.modifiers[i].get_add[key]
        return add

    def __g_mlt(self, key: str):
        mlt = 1
        for i in self.modifiers:
            if key in self.modifiers[i].get_mlt:
                mlt = mlt * self.modifiers[i].get_mlt[key]

        return mlt

    def add_alt(self, key: str, val: int or float):
        # add_alt是在add时提供修正，会影响“加上去的值”
        if len(dir(self.modifiers)) == 0:  # 如果修正是空，不知道这样对不对
            return val

        a = (val + self.__a_add(key)) * self.__a_mlt(key)
        return a

    def __a_add(self, key: str):
        add = 0
        for i in self.modifiers:
            if key in self.modifiers[i].alt_add:
                add = add + self.modifiers[i].alt_add[key]
        return add

    def __a_mlt(self, key: str):
        mlt = 1
        for i in self.modifiers:
            if key in self.modifiers[i].alt_mlt:
                mlt = mlt * self.modifiers[i].alt_mlt[key]
        return mlt

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


class Modifier:
    name: str
    describe: str
    get_add: Dict[str, int or float]
    get_mlt: Dict[str, int or float]
    alt_add: Dict[str, int or float]
    alt_mlt: Dict[str, int or float]
    timer: int

    def __init__(self):
        self.name = ''
        self.describe = ''
        self.get_add = {}
        self.get_mlt = {}
        self.alt_add = {}
        self.alt_mlt = {}
        self.timer = 0  # 为负一则是永久的

    def set_default(self, name, timer: int = -1):
        self.name = name
        data = file_parser.open_file('修正配置', self.__class__.__name__)
        if data is None:
            return
        if self.name in data:
            self.describe = data[self.name]['describe']
            self.get_add = data[self.name]['g_add']
            self.get_mlt = data[self.name]['g_mlt']
            self.alt_add = data[self.name]['a_add']
            self.alt_mlt = data[self.name]['a_mlt']

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