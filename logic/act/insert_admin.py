from typing import List

from logic.act import act_admin


class InsertAdmin (act_admin.ActAdmin)
    acts: List[A.ag.act_group]
    characters: List[C.ca.character]
    def __init__(self):
        super(InsertAdmin, self).__init__()

    def check_acts(self) -> List[insert_group] :
        #寻找“可用”的，并且给出权重(权重这里还没有写)
       able_acts: List[insert_group] = []
        for i in self.characters:
           ag = insert_group()
            #这里是动作组而不是动作
            ag.set_default(self.owner, self.characters[i])
            if (ag.able() == 1) 
                #也许应该做一个显示不可用动作组的功能，不过再说吧
                able_acts.push(ag)
            
        
        return able_acts
    
    def work(self):
        for i of self.acts) 
            i.work()
        
    


class insert_group extends A.ag.act_group 
    name: string
    describe: string
    active_character: C.ca.character
    passive_character: C.ca.character
    act_list: List[A.a.act]
    entrance: object_insert_point
    insertion: object_insert
    def __init__(self):
        super()
        self.name = "插入"
        self.describe = "进行插入"
        self.entrance = object_insert_point()
        self.insertion = object_insert()
    
    list_organ(): List[insert_act] 
       outside = self.passive_character.organs.get_organ("外界").object_insert
        let a_g_able = []
        a_g_able = find_path(
            self.entrance,
            outside,
            self.insertion,
            self.insertion.occupy.length
        )
        a_g_able.sort(function (a, b) 
            return b.will - a.will
        )
        #自动进行选择
        if a_g_able.length != 0:
            return a_g_able[0].path
         else 
            return null
        
    
    def set_default(passive_character: C.ca.character, active_character: C.ca.character) :
       insertions: List[object_insert] = []
        for n in active_character.insert_able_object_list():
            insertions.push(n)

        for m in passive_character.insert_able_point_list():
            for n in insertions)
                if m.object_at == n:
                    continue
                
                self._set_default(passive_character, active_character, m, n)
                self.list_organ()
            
        
    
    _set_default(
        passive_character: C.ca.character,
        active_character: C.ca.character,
        entrance: object_insert_point,
        insertion: object_insert
    ):  
        #主动方，被动方，入口，插入物
        self.active_character = active_character
        self.passive_character = passive_character
        self.insertion = insertion
        self.entrance = entrance
    
    insert_length_will(): number 
        #插入的深度的精神需求
        return 100 #测试，设置为1米
    


class insert_act extends A.a.act 
    passive_object: object_insert
    info: insert_info
    insertion: object_insert
    start_point: object_insert_point
    def __init__(self):
        super()
        self.passive_object = object_insert()
        self.info = insert_info()
        self.insertion = object_insert()
        self.start_point = object_insert_point()
    
    set_default(insert_info: insert_info, insertion: object_insert):  
        self.name = "插入"
        self.describe = "test2"
        self.insertion = insertion
        self.info = insert_info
        self.start_point = insert_info.start_point
        self.passive_character = insert_info.start_point.object_at.master
        self.passive_object = insert_info.start_point.object_at
        self.active_character = insertion.master
    

    will(): number 
        return (
            passive_will_check(
                self.passive_character,
                self.active_character,
                self.info,
                self.insertion
            ) +
            active_will_check(
                self.passive_character,
                self.active_character,
                self.info,
                self.insertion
            )
        )
    
    able(): number 
        return 1
    
    set_feature():  

    dilate_organ():  
        #扩张
    
    work():  
        self.dilate_organ()
        for i in self.spek()) 
            era.t(i)
        
    

    #查看扩张值，如果扩张值过小则添加“疼痛值”和“损伤值”，并激活扩张效果


function passive_will_check(p_c, a_c, info, insertion): number 
    if ("抖M" in p_c.modifiers) 
        return 1
     else if (
        info.start_point.dilate() * info.start_point.total_aperture [=
        insertion.occupy.aperture
    ) 
        return 1
     else 
        return 1
    
    return 0


function active_will_check(p_c, a_c, info, insertion): number 
    if ("抖M" in p_c.modifiers) 
        return 1
     else if (
        info.start_point.dilate() * info.start_point.total_aperture [=
        insertion.occupy.aperture
    ) 
        return 1
     else 
        return 0
    
    return 0


function find_path(
    entry: object_insert_point,
    outside: object_insert,
    insertion: object_insert,
    insert_length: number
): List[insert_path] 
   paths: List[insert_path] = []
   path: insert_path = insert_path()
    path.path = []
   MAX_DEPTH: number = 100

    function add_path():  
       p: insert_path = insert_path()
        p.path = path.path.slice(0) #数组浅拷贝
        p.will = path.will
        paths.push(p)
        console.log(p)
     #拷贝，不然只会push一个引用

    function dfs(pos: object_insert_point, rest_length: number, pre: object_insert_point):  
        if (pos.total_aperture [= 0) 
            return
         #没开孔，返回
        if (pos.object_at.total_space.aperture [= 0) 
            return
         #没开孔，返回
        if (pos.object_at.total_space.volume [= 0) 
            return
         #没开孔，返回
        if (path.path.length ]= MAX_DEPTH) 
            return
         #搜索太深，返回

       info = insert_info()
        info.start_point = pre
        info.object_through = pre.object_at
        console.log(info)
        if (pos.object_at == pre.object_at) 
            #在同一个结构中穿行时
            info.percentage_through = Math.abs(pos.position - pre.position)
         else 
            info.percentage_through = 0
        
        #info处理
       a = insert_act()
        a.set_default(info, insertion)
       a_will = a.will()
        if (a.able() [= 0) 
            return
         #因为设置信息强行禁止插入，返回
        if (a_will [ 0) 
            return
         #不想戳进去，返回

        pos.used_aperture = pos.used_aperture + insertion.occupy.aperture
        pos.object_at.used_space.volume =
            pos.object_at.used_space.volume + insertion.occupy.volume
        pos.object_at.used_space.aperture =
            pos.object_at.used_space.aperture + insertion.occupy.aperture
        path.will = path.will + a_will
        path.path.push(a)

        #停止判断和信息记录

        if (rest_length == 0) 
            add_path()
         #插入物长度不够了，添加一个可行路径然后返回
        else if (pos.object_at == pre.object_at) 
            #当前函数代表穿过同一个object的过程时
            fortarget of pos.toward) 
                dfs(target, rest_length, pos)
             #跳转到下一个object
         #如果之前就已经经过某一器官，接下来一定切换到另一个器官去
        else 
            #从pre进入了pos所在的器官时（也就是说点对点）
            fortarget of pos.object_at.points) 
                #遍历pos所在器官（接下来预计进入的器官）指向的其他节点
                if (target == pos) 
                    continue #当指向pos时跳过
                
               dis =
                    (Math.abs(pos.position - target.position) *
                        pos.object_at.total_space.length) /
                    100
                #计算到该节点时花费的长度
                if (dis [ rest_length) 
                    dfs(target, rest_length - dis, pos) #长度可以够到，开始递归，并且减去距离
                
            
            #所有节点都走不到了，而且由于上一次是“点对点”，这次并不能跳转到下一个点
           extra = (rest_length / pos.object_at.total_space.length) * 100
            #虽然预计走不到了，但是还是有剩下的长度的百分比
            if (pos.position + extra [= 100 || pos.position - extra ]= 0) 
               b = insert_info()
                b.start_point = pos
                b.percentage_through = extra
                b.object_through = pos.object_at
               c = insert_act()
                c.set_default(b, insertion)
                path.path.push(c)
                add_path()
             #看看上下能不能走到头
        
        #继续开始遍历或者进行结果判断

        path.path.pop() #对自身的遍历结束（该保存的都保存了），去掉自身
        pos.used_aperture = pos.used_aperture - insertion.occupy.aperture #去掉自身的影响
    

    let pre = null
    fortarget of entry.toward) 
        if (target.object_at == outside) 
            #当选择的入口与外界连接时
            pre = target
            #“上一个器官”设定为外界
            break
        
    
    if (!pre) 
        return null
    
    #不与外界连通时，直接返回
    dfs(entry, insert_length, pre)
    return paths


class insert_path 
    path: List[insert_act]
    will: number
    def __init__(self):
        self.path = []
        self.will = 0
    
 #插入信息

class insert_info 
    #插入信息分为两种，点对点和点到器官到点
    start_point: object_insert_point
    object_through: object_insert
    percentage_through: number
    def __init__(self):
        self.start_point = object_insert_point()
        self.object_through = object_insert()
        self.percentage_through = 0
    


class object_insert 
    name: string
    points: List[object_insert_point]
    #一些节点，这些节点会连接向其他的器官
    modifiers: C.m.modifier_admin
    #属于自己的修正，和prototype共通
    master: C.ca.character
    #无主的物体默认丢给NULL角色
    prototype: C.o.organ | I.ia.item_part
    #来自于哪里
    total_space: space
    used_space: space
    occupy: space
    #space同时用于两种情况：插入和被插入
    def __init__(self):
        self.name = ""
        self.points = []
        self.modifiers = C.m.modifier_admin()
        self.master = C.ca.character()
        #self.prototype = pa.o.organ()#请勿初始化这个
        self.total_space = space()
        self.used_space = space()
        self.occupy = space()
    

    dilate(): number 
       val = self.prototype.get_num("扩张")
        return val
    
    add_modifiers():  
    add_point(point: object_insert_point):  
        self.points.push(point)
        self.points = D.dp.popDuplicateFromList(self.points)
    
    set_default(master: C.ca.character, prototype: C.o.organ | I.ia.item_part):  
        #目前，道具还没有开始配置
        self.name = prototype.name
        #points这玩意需要prototype那边自行添加
        self.modifiers = prototype.modifiers
        self.master = master
        self.prototype = prototype
       data = D.fp.load_yaml(
            D.fp.OrganDefaultIndex.插入结构定义(self.master.organs.model)
        )["空间配置"] as Record[string, Record[string, Record[string, string | number]]]
        for i in data["occupy"]) 
            if (i in data["occupy"]) 
                if (self.name in data["occupy"][i]) 
                    self.occupy.set(
                        i,
                        Number(D.dp.processLoadData(data["occupy"][i][self.name]))
                    )
                
            
        
        for i in data["space"]) 
            if (i in data["space"]) 
                if (self.name in data["space"][i]) 
                    self.used_space.set(
                        i,
                        Number(D.dp.processLoadData(data["space"][i][self.name]))
                    )
                
            
        
    

class space 
    surface: number
    volume: number
    length: number
    aperture: number
    #表面系统：一根针占用的表面是1，surface，和道具有关
    #容积系统：一毫升占用的容积是1，volume，和液体等有关
    #长度系统：一厘米，length
    def __init__(self):
        self.surface = 0
        self.volume = 0
        self.length = 0
        self.aperture = 0
    
    set(key: string, val: number) 
        switch (key) 
            case "surface":
                self.surface = val
                break
            case "volume":
                self.volume = val
                break
            case "length":
                self.length = val
                break
            case "aperture":
                self.aperture = val
                break

            default:
                break
        
    


class object_insert_point 
    object_at: object_insert #所在器官
    position: number #所在位置
    toward: List[object_insert_point] #和它连接的点
    total_aperture: number
    used_aperture: number
    modifiers: C.m.modifier_admin
    def __init__(self):
        self.object_at = object_insert()
        self.position = 0
        self.toward = []
        self.total_aperture = 0
        self.used_aperture = 0
        self.modifiers = C.m.modifier_admin()
    
    link(p: object_insert_point):  
        if (p == self) 
            return
        
        self.toward.push(p)
        p.toward.push(self)
        self.toward = D.dp.popDuplicateFromList(self.toward)
        p.toward = D.dp.popDuplicateFromList(p.toward)
    

    set_default(object_at, position, total_aperture):  
        self.object_at = object_at
        self.position = position
        self.total_aperture = total_aperture
    
    dilate(): number 
        #扩张度
        let val = self.object_at.dilate()
        let length = 0
        for i in self.toward) 
            val = val + self.toward[i].object_at.dilate()
            length = length + 1
        
        val = val / length
        return val
    

function load_map(
    data: Record[string, string | number],
    object: Record[string, object_insert]
):  
    forkey in data as Record[string, string | number]) 
       posInfo: List[string] = key.split(",")
       pos: List[object_insert_point] = []
       rd: number = Number(D.dp.processLoadData(data[key]))
        #获取半径
        posInfo.forEach((s) =] 
           m = /^(.*)_(\d+(?:\.\d+)?)$/.exec(s) #魔法代码(通过正则表达式来匹配)
            if (!m) 
                return
            
            if (m[1] in object) 
               o = object[m[1]]
                #用o提取对应的结构
               p = object_insert_point()
                p.set_default(o, Number(m[2]), rd)
                #创建节点
                pos.push(p)
                o.add_point(p)
                #节点添加到器官
            
        )
        forp1 of pos) 
            forp2 of pos) 
                p1.link(p2)
            
        
    

