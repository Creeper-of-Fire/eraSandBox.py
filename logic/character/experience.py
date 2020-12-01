from typing import Dict, Any
from logic.data import file_parser, data_process


class ExperienceAdmin:
    data_list: Dict[str, Any]

    def __init__(self):
        self.data_list = {}
        self.experiences: Dict[str, Experience] = {}

    def set_default(self, s_list: Dict[str, str or int or float]):
        data = file_parser.open_file('经历配置')
        data_list = {}
        for i in s_list:
            a = data_process.process_load_data(s_list[i])
            if a != 0:
                self.experiences[i] = Experience()
                b = data[i]
                self.experiences[i].set_default(i, b)
                data_list[i] = b

        self.data_list = data_list  # 然后character调用这个玩意


class Experience:
    name: str
    describe: str

    def __init__(self):
        self.name = ''
        self.describe = ''

    def set_default(self, name, data):
        self.name = name
        self.describe = data['描述']
