from typing import List, Optional

from logic.act import act_group
from logic.actor import character


class ActAdmin:
    owner: Optional['character.Character']
    to_do_list: List[act_group.ActGroup]  # 可用的动作组
    able_acts: List[act_group.ActGroup]
    characters: List[Optional['character.Character']]

    def __init__(self):
        self.characters = []
        self.to_do_list = []

    def set_default(self, owner: Optional['character.Character'], characters: List[Optional['character.Character']]):
        self.owner = owner
        self.characters = characters

    def auto_plan_acts(self):
        def willing_to_do(ag: act_group.ActGroup):
            return ag.will()

        self.able_acts.sort(key=willing_to_do, reverse=True)
        self.to_do_list.append(self.able_acts[0])  # 最大的

    def manual_plan_acts(self, ag: act_group.ActGroup):
        self.to_do_list.append(ag)

    def check_acts(self):
        # 寻找“可用”的，并且给出权重(权重这里还没有写)
        able_acts: List[act_group.ActGroup] = []
        for i in self.characters:
            for ag in self.act_group_list():
                # 这里是动作组而不是动作
                ag.set_default(self.owner, i)
                if ag.able():
                    # 也许应该做一个显示不可用动作组的功能，不过再说吧
                    able_acts.append(ag)
        self.able_acts = able_acts

    @staticmethod
    def act_group_list():
        return [act_group.Kiss(), ]

    def work(self):
        for i in self.to_do_list:
            i.work()
        self.to_do_list = []
