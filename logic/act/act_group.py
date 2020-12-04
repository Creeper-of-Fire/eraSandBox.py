from typing import List,Optional

import erajs.api as era
from logic.act import act
from logic.actor import character


class ActGroup:
    name: str
    describe: str
    active_character: Optional['character.Character']
    passive_character: Optional['character.Character']
    act_list: List[act.Act]

    def __init__(self):
        self.name = ''
        self.describe = ''
        self.active_character = character.Character()
        self.passive_character = character.Character()
        self.act_list = []

    def able(self) -> bool:
        for i_act in self.act_list:
            if i_act.able() is False:
                return False
        return True

    def will(self):
        willing = 0
        for i_act in self.act_list:
            if i_act.will() == 0:
                return 0
            else:
                willing = willing + i_act.will()
        return willing

    def _speak(self):
        era.t(self.describe)
        era.t()

    def work(self):
        self._speak()
        for i_act in self.act_list:
            i_act.work()

    def set_default(self, active_character, passive_character):
        self.active_character = active_character
        self.passive_character = passive_character
        self._list_act()

    def _list_act(self):
        pass


class Kiss(ActGroup):
    def __init__(self):
        super(Kiss, self).__init__()
        self.name = '接吻'
        self.describe = 'describe_kiss'

    def _list_act(self):
        a = act.Touch()
        a.set_default(self.active_character, self.active_character, '嘴唇', '嘴唇')
        self.act_list = [a, ]
