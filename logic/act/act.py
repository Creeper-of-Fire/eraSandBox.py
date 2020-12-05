from typing import List, Optional

from logic.actor import equipment, organ
import logic.actor.character as character


class Act(object):
    name: str
    describe: str
    passive_character: Optional['character.Character']
    active_character: Optional['character.Character']
    passive_object: Optional['equipment.Equipment'] or Optional['character.Character']
    active_object: Optional['equipment.Equipment'] or Optional['character.Character']
    feature: List[str]

    def __init__(self):
        self.passive_character = character.Character()
        self.active_character = character.Character()
        self.active_object = organ.Organ()
        self.passive_object = organ.Organ()
        self.feature = []

    def will(self) -> int:
        # 通过条件判断来判断是否可行，当大于0则可行
        # 在以后加入“自动调教”时会很有用
        return 0

    def able(self) -> bool:
        # 通过设置来直接禁止的动作
        return False

    '''
    spek(): List [ str ]
        def _speak_func(self, speak: str)->str:
            # 处理口上中类似于{balabala}的数据
            return speak

        list_for_rand: Array < Array < string >> = []
        s_data = D.fp.load_yaml(D.fp.ActDefaultIndex.口上配置()) as Record <
            string,
            Array < Record < string, Record < string, Array < string >> | string>>
        >
        active = self.active_character
        passive = self.passive_character
        a_feature = active.modifiers.names
        p_feature = passive.modifiers.names
        for i_feature in self.feature):
            if i_feature in s_data
             else
                continue

            for (dict1 of s_data[i_feature])
                # s_data[i_feature]是个列表，dict是个字典
                able=dict1['ABLE'] as Record < string, Array < string >>
                is_true=1
                if ('A' in able)
                    for (a_key in able['A'])
                        if (a_key in a_feature)
                         else
                            is_true=0



                if ('P' in able)
                    for (p_key in able['P'])
                        if (p_key in p_feature)
                         else
                            is_true=0



                if (is_true == 1)
                    t_list=[]
                    for (i_key in dict1)
                        if (i_key != 'ABLE')
                            t_list.append(dict1[i_key])


                    list_for_rand.append(t_list)



        speak_list: Array < string >= []
        if (list_for_rand.length != 0)
            speak_list=D.dp.getRandomFromArray(list_for_rand)
            speak_list.append(D.dp.translateString(self.describe))

        for (i in speak_list)
            i=_speak_func(this, i)

        return speak_list
    '''

    def work(self):
        pass

    def set_default(self, active_character: Optional['character.Character'],
                    passive_character: Optional['character.Character'],
                    active_object_name: str, passive_object_name: str):
        self.active_character = active_character
        self.passive_character = passive_character
        self.active_object = active_character.search_object(active_object_name)
        self.passive_object = passive_character.search_object(passive_object_name)


class Touch(Act):
    def __init__(self):
        super(Touch, self).__init__()
        self.name = 'name_touch'
        self.describe = 'describe_touch'
        self.timer = 0

    def will(self) -> int:
        return 1

    def able(self) -> bool:
        return True

    def work(self):
        super(Touch, self).work()
        self.active_character.num_data.max_physical_power -= 1900


class Hit(Act):
    def __init__(self):
        super(Hit, self).__init__()
        self.name = 'name_hit'
        self.describe = 'describe_hit'
        self.timer = 0

    def will(self) -> int:
        return 1

    def able(self) -> bool:
        return True

    def work(self):
        super(Hit, self).work()
