"""
作者：Kevin Zhou
日期：2022年03月31日
"""
from manim import *




def P(x, y):
    """
    生成坐标，单纯方便调参
    :param x: 坐标X
    :param y: 坐标Y
    :return:
    """
    return x * RIGHT + y * UP


class myGraph(VGroup):
    def __init__(self, num, pos, edge, **kwargs):
        super().__init__(**kwargs)
        cirList = VGroup()
        labelList = VGroup()
        edgeList = VGroup()
        edgeLabelList = VGroup()
        for i in range(num):
            cirList.add(self.myCircle().move_to(pos[i]))
            labelList.add(self.label(i + 1, cirList[i], color=YELLOW, follow=1))
        for i in range(len(edge)):
            link = self.link_arr(cirList[edge[i][0] - 1], cirList[edge[i][1] - 1], label=str(edge[i][2]))
            edgeList.add(link[0])
            edgeLabelList.add(link[1])

        self.cirList = cirList
        self.labelList = labelList
        self.edgeList = edgeList
        self.edgeLabelList = edgeLabelList
        self.add(self.cirList, self.labelList, self.edgeList, self.edgeLabelList)


class myScene(Scene):
    """
    整合了一些动画常用方法
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shift(self, pos, *obj):
        """
        移动动画 （相对坐标）
        :param obj:
        :param pos:
        """
        lis = []
        for o in obj:
            lis.append(o.animate.shift(pos))
        self.play(*lis)

    def move(self, obj, pos):
        """
        移动动画 （绝对坐标）
        :param obj:
        :param pos: 坐标 (x,y) 或者  (a,b,c)
        """
        if len(pos) > 2:
            self.play(obj.animate.move_to(pos))
        else:
            self.play(obj.animate.move_to(P(*pos)))

    def show(self, *obj):
        """
        动画显示
        :param obj:
        """
        for o in obj:
            self.play(Write(o))

    def create(self, *obj):
        """
        动画显示
        :param obj:
        """
        lis = []
        for o in obj:
            lis.append(Create(o))
        self.play(*lis)

    def ReplaceTransform(self, obj1, obj2):
        """
        转换动画，本体消失
        :param obj1:
        :param obj2:
        """
        self.play(ReplacementTransform(obj1, obj2))

    def transform(self, obj1, obj2):
        """
        转换动画,本体不消失
        :rtype: object
        :param obj1:
        :param obj2:
        """
        self.play(ReplacementTransform(obj1.copy(), obj2))

    def disappear(self, *obj):
        """
        消失动画
        :param obj:
        """
        lis = []
        for o in obj:
            lis.append(Unwrite(o))
        self.play(*lis)

    def swap(self, obj1, obj2, wait=0, flash=0):
        """
        the animation of swap two object
        :param wait:
        :param self: Scene
        :param obj1:
        :param obj2:
        """
        if flash == 1:
            self.play(Flash(obj2))
        tem = obj1.get_center()
        self.play(obj1.animate.move_to(obj2.get_center()), obj2.animate.move_to(tem))
        if wait > 0:
            self.wait(wait)

    def ChangeColor(self, obj, color):
        self.play(obj.animate.set_color(WHITE).set_fill(color, opacity=1))

    def Flash(self, obj):
        self.play(Flash(obj))

    def MakeText(self, *text, buff=0.2, align=0, dot=0):
        """
        把标记语言文本打包成一个组
        :param dot: 是否加点
        :param align: 为0时居中对其，为1是以左边线对其
        :param buff:行间距
        :param text: 内容
        :return:返回VGroup
        """
        textSet = VGroup()
        for t in text:
            if isinstance(t, list):
                if len(t) != 1:
                    T = Text(t[0], t2c=t[1])
                    textSet.add(T)
                else:
                    T = Text(t[0])
                    textSet.add(T)
            if isinstance(t, str):
                T = Text(t)
                textSet.add(T)
            else:
                textSet.add(t)
        textSet.arrange(DOWN, buff=buff)
        if align == 1:
            for t in textSet:
                t.align_to(textSet[0], LEFT)
        if dot == 1:
            for i in range(len(text)):
                dot = Dot().next_to(textSet[i], LEFT)
                textSet.add(dot)
        return textSet

    def MakeTitle(self, *text, buff=0.2, align=0):
        """
        合成标题
        :rtype: object
        :param align: 行间距
        :param text: 文字内容
        :param buff: 行间距
        """
        title = self.MakeText(*text, buff=buff, align=align)
        underline_width = config["frame_width"] - 2
        underline = Line()
        underline.width = underline_width
        underline.next_to(title, DOWN)
        title.add(underline)
        title.to_edge(UP)
        return title

    def link(self, obj1, obj2, buff=0.0, width=8, color=WHITE, follow=1):
        """
        创建一个连接线
        :param follow: 是否跟随
        :param color:  颜色
        :param width: 线宽
        :param buff: 间距
        :param obj1: 起点
        :param obj2: 终点
        """
        l1 = Line(obj1.get_center(), obj2.get_center(), buff=buff).set_stroke(color, width)
        if follow == 1:
            l1.add_updater(lambda z: z.become(Line(obj1.get_center(), obj2.get_center(), buff=buff)
                                              .set_stroke(color, width)))
        return l1

    def link_arr(self, obj1, obj2,
                 buff=0.0,
                 width=5,
                 color=WHITE,
                 follow=1,
                 label='',
                 label_size=0.5,
                 Curved=0):
        buff = obj1.width / 2
        if Curved == 1:
            l1 = CurvedArrow(obj1.get_center(), obj2.get_center()).set_stroke(color, width)
            vec = (obj1.get_center() - obj2.get_center())
            vec = vec * 1 / ((vec[0] ** 2 + vec[1] ** 2) ** 1 / 2)
            v = [vec[1], vec[0]]
            l1.shift(2.1 * buff * P(-v[0], v[1]))
        else:
            l1 = Arrow(obj1.get_center(), obj2.get_center(), buff=buff + 0.1,
                       max_tip_length_to_length_ratio=0.05).set_stroke(color, width)
        if follow == 1:
            def C_updater(obj):
                l1 = CurvedArrow(obj1.get_center(), obj2.get_center()).set_stroke(color, width)
                l1.set_color(obj.color)
                vec = (obj1.get_center() - obj2.get_center())
                vec = vec * 1 / ((vec[0] ** 2 + vec[1] ** 2) ** 1 / 2)
                v = [vec[1], vec[0]]
                l1.shift(2.1 * buff * P(-v[0], v[1]))
                obj.become(l1)

            def A_updater(obj):
                l1 = Arrow(obj1.get_center(), obj2.get_center(), buff=buff + 0.1,
                           max_tip_length_to_length_ratio=0.05).set_stroke(color, width)
                l1.set_color(obj.color)
                obj.become(l1)

            if Curved == 1:
                l1.add_updater(C_updater)
            else:
                l1.add_updater(A_updater)
        if label != '':
            t1 = Text(label).set_color(WHITE)
            x = (obj1.get_center() - obj2.get_center())[0]
            if x == 0:
                t1.move_to(l1.get_center()).shift(RIGHT * 0.5 * label_size).scale(label_size)
            else:
                t1.move_to(l1.get_center()).shift(UP * 0.5 * label_size).scale(label_size)
            if follow == 1:
                def T_updater(obj):
                    a = (obj1.get_center() - obj2.get_center())[0]
                    if a == 0:
                        obj.move_to(l1.get_center()).shift(RIGHT * 0.5 * label_size)
                    else:
                        obj.move_to(l1.get_center()).shift(UP * 0.5 * label_size)

                t1.add_updater(T_updater)

        if label != '':
            return [l1, t1]
        return l1

    # def link_
    def label(self, num, obj, size=1, color=BLUE, follow=0):
        """
        生成下标
        :param num:数字
        :param obj:主物体
        :param size:大小
        :param color:颜色
        :param follow: 是否跟随
        :return:
        """
        lab = Integer(number=num).set_color(color).scale(size).move_to(obj.get_center()).set_stroke(color, 2)
        if follow == 1:
            lab.add_updater(lambda d: d.move_to(obj.get_center()))
        return lab

    def TitleAnimation(self, T1):
        """
        显示居中标题加上移动画
        """
        self.show(T1)
        title = self.MakeTitle(T1.copy())
        self.wait()
        self.ReplaceTransform(T1, title)
        return title

    def Graph(self, num, pos, edge):
        """
        通用图
        edge格式 (点， 点， 路径长)
        顶点顺序默认从1开始数  1,2,3...
        """
        cirList = VGroup()
        labelList = VGroup()
        edgeList = VGroup()
        edgeLabelList = VGroup()
        for i in range(num):
            cirList.add(self.myCircle().move_to(pos[i]))
            labelList.add(self.label(i + 1, cirList[i], color=YELLOW, follow=1))
        for i in range(len(edge)):
            link = self.link_arr(cirList[edge[i][0] - 1], cirList[edge[i][1] - 1], label=str(edge[i][2]))
            edgeList.add(link[0])
            edgeLabelList.add(link[1])
        graph = VGroup(cirList, labelList, edgeList, edgeLabelList)
        return graph

    def myCircle(self):
        """
        常用圆
        """
        return Circle(radius=0.5).set_color(WHITE).set_fill(BLACK, opacity=1)

    def labelCircle(self, num, color=BLUE):
        cir = VGroup()
        c1 = self.myCircle()
        label = self.label(num, c1, color=color, follow=1)
        cir.add(c1, label)
        return cir

    def MyGraph(self, num, pos, edge):
        """
        通用图
        edge格式 (点， 点， 路径长)
        顶点顺序默认从1开始数  1,2,3...
        基于类实现
        """

        class myGraph(VGroup):
            def __init__(s, **kwargs):
                super().__init__(**kwargs)
                cirList = VGroup()
                labelList = VGroup()
                edgeList = VGroup()
                edgeLabelList = VGroup()
                for i in range(num):
                    cirList.add(self.myCircle().move_to(pos[i]))
                    labelList.add(self.label(i + 1, cirList[i], color=YELLOW, follow=1))
                for i in range(len(edge)):
                    link = self.link_arr(cirList[edge[i][0] - 1], cirList[edge[i][1] - 1], label=str(edge[i][2]))
                    edgeList.add(link[0])
                    edgeLabelList.add(link[1])

                s.cirList = cirList
                s.labelList = labelList
                s.edgeList = edgeList
                s.edgeLabelList = edgeLabelList
                s.add(s.cirList, s.labelList, s.edgeList, s.edgeLabelList)

        return myGraph()

    def Tree(self, num, pos, edge, label):
        cirList = VGroup()
        edgeList = VGroup()
        for i in range(num):
            cirList.add(self.labelCircle(label[i]).move_to(pos[i][0]*RIGHT+pos[i][1]*UP))
        for i in range(len(edge)):
            link = self.link(cirList[edge[i][0] - 1], cirList[edge[i][1] - 1], buff=0.5)
            edgeList.add(link)
        Tree = VGroup()
        Tree.add(cirList, edgeList)
        return Tree

    def TitleAim(self, text, color):
        t1 = Text(text, t2c=color)
        self.show(t1)
        title = self.MakeTitle(t1.copy())
        self.wait(3)
        self.ReplaceTransform(t1, title)
        self.wait(3)
        return title

    def catalogue(self,text):
        t = self.MakeText(*text, align=1, dot=1)
        self.show(t)
        self.wait(2)
        return t

    #     开头动画模板
    #     title = s.TitleAim("插入操作", {'插入操作': ORANGE})       标题
    #     catalogue = s.catalogue(["第一", "第二", "第三", "第四"])  目录
    #     s.disappear(title, catalogue)                           动画


# --------------------------------------------------
# 测试
class text(myScene):
    def construct(s):
        T1 = Text("Johnson-Trotter算法").shift(UP)
        # T2 = Text("是一可以生成任意数量元素排列的算法", t2c={'任意数量': RED})
        # text = [["是一可以生成任意数量元素排列的算法", {'任意数量': RED}],
        #         ["Johnson-Trotter算法"]]  # 推荐形式 ******
        # t = s.MakeText(*text, align=1)
        #
        # t2cwords = Text('任意数量', t2c={'任意': YELLOW, '数量': RED})  # 推荐形式 ****
        # t2cwords.to_edge(UP)
        # title = s.MakeTitle(*text)
        # cir1 = Circle()
        # cir2 = Circle().shift([2, 2, 0])
        # link2 = s.link(cir1, cir2, buff=0, width=8)
        # # s.add(title, link)
        # # s.transform(title, T1)
        # # s.shift(P(0, -4), title, T1)
        # s.add(cir1, cir2, link2)
        # s.next_section()
        # title = s.TitleAnimation(T1)
        # s.disappear(title)
        cir = Circle().scale(2)
        cir1 = Circle().shift(4 * RIGHT + UP).scale(2)
        link = s.link_arr(cir, cir1, label="5", Curved=0)
        s.add(link[0], link[1], cir, cir1)
        # label = '5'
        # t1 = Text(label).set_color(WHITE)
        # s.add(t1)


class textGraph(myScene):
    def construct(s):
        num = 6
        pos = [[-3, 0, 0],
               [0, 2, 0],
               [0, 0, 0],
               [0, -2, 0],
               [3, 1, 0],
               [3, -1, 0]]
        # edge (点， 点， 路径长)
        edge = [[1, 2, 1],
                [1, 3, 3],
                [1, 4, 3],
                [2, 3, 1],
                [2, 5, 1],
                [3, 5, 1],
                [3, 6, 3],
                [3, 4, 1],
                [4, 6, 1],
                [5, 6, 2]]
        cirList = VGroup()
        labelList = VGroup()
        edgeList = VGroup()
        edgeLabelList = VGroup()
        for i in range(num):
            cirList.add(s.myCircle().move_to(pos[i]))
            labelList.add(s.label(i + 1, cirList[i], color=YELLOW))
        for i in range(len(edge)):
            link = s.link_arr(cirList[edge[i][0] - 1], cirList[edge[i][1] - 1], label=str(edge[i][2]))
            edgeList.add(link[0])
            edgeLabelList.add(link[1])
        graph = VGroup(cirList, labelList, edgeList, edgeLabelList)
        s.add(graph)

        g1 = s.Graph(6, pos, edge)
        g2 = s.MyGraph(6, pos, edge)
        s.add(g1, g2)

# 坐标参考图
class numplane(myScene):
    def construct(s):
        p = NumberPlane()
        s.add(p)
        for i in range(7):
            lab = Integer(number=i)
            lab.move_to(i*RIGHT)
            s.add(lab)

        for i in range(7):
            lab = Integer(number=i)
            lab.move_to(-i * RIGHT)
            s.add(lab)

        for i in range(4):
            lab = Integer(number=i)
            lab.move_to(i * UP)
            s.add(lab)

        for i in range(4):
            lab = Integer(number=i)
            lab.move_to(-i * UP)
            s.add(lab)