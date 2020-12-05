import A = require('../Act/__init__')
import C = require('../Character/__init__')

export  item_admin, item, item_part 

class item_admin 
    constructor() 
    set_default(类型) 

class item 
    name: string
    modifiers: C.m.modifier_admin
    parts: Array<item_part>
    constructor() 
        self.name = ''
        self.modifiers = C.m.modifier_admin()
        self.parts = []
    

class item_part 
    name: string
    modifiers: C.m.modifier_admin
    object_insert: A.i.object_insert
    private num_data: Record<string, number>
    private str_data: Record<string, string>
    constructor() 
        self.name = ''
        self.modifiers = C.m.modifier_admin()
        self.object_insert = A.i.object_insert()
        self.num_data = 
        self.str_data = 
    
    #希望少用
    get(key: string) 
        if (key in self.num_data) 
            return self.get_num(key)
         else if (key in self.str_data) 
            return self.get_str(key)
         else 
            return null
        
    
    alt(key: string, val: string | number) 
        if (key in self.num_data) 
            self.alt_num(key, val as number)
         else if (key in self.str_data) 
            self.alt_str(key, val as string)
         else 
            null
        
    
    get_str(key: string): string 
        if (key in self.str_data) 
            return self.str_data[key]
         else 
            return ''
        
    
    alt_str(key: string, val: string) 
        self.str_data[key] = val
    

    get_num(key: string): number 
        if (key in self.num_data) 
            g = self.modifiers.addition_when_get_value(key, self.num_data[key])
            return g
         else 
            return 0
        
    
    alt_num(key: string, val: number):  
        add_val = val - self.num_data[key]
        self._add_num(key, add_val)
    
    private _add_num(key: string, val: number):  
        a = self.modifiers.addition_when_alt_by_act(key, val) #获得加成
        part = 0
        self.num_data[key] = self.num_data[key] + a
    

