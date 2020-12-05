import random
from typing import List, Dict

from logic.data import file_parser


def process_load_data(data: str or Union[int, float]) -> str or Union[int, float]:
    def str_is_number(test_str: str) -> bool:
        try:
            f = float(test_str)
            return True
        except ValueError:
            return False

    data = str(data)  # 字符串化
    s_list = data.split('/,')  # 分开所有并列的
    s_range = random.choice(s_list).split('/_')
    # 任选一个，然后解析范围
    a = s_range[0]
    b = s_range[-1]
    if str_is_number(a) and str_is_number(b):
        if s_range[0].count('.') == 1:
            # 此时为浮点数
            return random.uniform(float(a), float(b))
        else:
            # 此时为整数
            return random.randint(int(float(a)), int(float(b)))
    else:
        return s_range[0]


def pop_duplicate_from_array(s_list: List) -> List[any]:
    return list(set(s_list))


def translate_string(speak: str) -> str:
    t_data: Dict[str, str or List[str]] = file_parser.open_file('描述配置')
    if speak in t_data:
        a = t_data[speak]
        if type(a) == str:
            return a
        else:
            return random.choice(a)
    # 功能暂时不做
    return speak
