"""
作者：Kevin Zhou
日期：2022年04月25日
"""

from ComAnFun import *

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

class page(myScene):
    def construct(s):
        T1 = Text("What is", t2c={'What': BLUE}).scale(3)
        T2 = Text("dijkstra算法", t2c={'dijkstra算法': YELLOW}).scale(3).next_to(T1, DOWN)
        s.add(T1, T2)
class begin(myScene):
    def construct(s):
        g2 = s.MyGraph(6, pos, edge)

        s.play(Create(g2))
        s.wait()
        s.ChangeColor(g2.cirList[0], RED)
        s.wait()
        r1 = SurroundingRectangle(g2).set_color(WHITE)
        s.play(Create(r1))
        s.wait()


class loop_1(myScene):
    def construct(s):
        posNew = [[0, 2, 0],
                  [-2, 0, 0],
                  [0, 0, 0],
                  [2, 0, 0]]
        for i in range(4):
            pos[i] = posNew[i]
        g2 = s.MyGraph(6, pos, edge).shift(DOWN)
        g2.cirList[0].set_color(RED)
        s.play(Write(g2.cirList[0]))
        s.play(Write(g2.cirList[1]),
               Write(g2.cirList[2]),
               Write(g2.cirList[3]),
               Write(g2.labelList[0]),
               Write(g2.labelList[1]),
               Write(g2.labelList[2]),
               Write(g2.labelList[3]))
        s.play(Write(g2.edgeList[0]),
               Write(g2.edgeList[1]),
               Write(g2.edgeList[2]),
               Write(g2.edgeLabelList[0]),
               Write(g2.edgeLabelList[1]),
               Write(g2.edgeLabelList[2]))
        s.wait()
        s.Flash(g2.cirList[1])
        s.wait()
        s.ChangeColor(g2.cirList[1], ORANGE)
        s.ChangeColor(g2.edgeList[0], YELLOW)
        s.wait()
        s.shift(UP * 2, g2.cirList[1])
        shortest = VGroup(g2.cirList[0], g2.cirList[1])
        r1 = SurroundingRectangle(shortest)
        s.show(r1)
        s.wait()
        g2.cirList[4].move_to([-2, -1, 0])
        s.play(Write(g2.cirList[4]))
        s.play(Write(g2.labelList[4]))
        s.play(Write(g2.edgeList[3]), Write(g2.edgeList[4]))
        s.play(Write(g2.edgeLabelList[3]), Write(g2.edgeLabelList[4]))
        s.wait()

        s.Flash(g2.cirList[2])
        s.wait()
        s.ChangeColor(g2.cirList[2], ORANGE)
        s.ChangeColor(g2.edgeList[3], YELLOW)
        s.play(g2.cirList[0].animate.shift(1*UP),
               g2.cirList[1].animate.shift(1*UP),
               g2.cirList[2].animate.shift(1.5*UP+LEFT),)
        shortest.add(g2.cirList[2])

        r2 = SurroundingRectangle(shortest)
        s.ReplaceTransform(r1, r2)
        # s.shift(RIGHT, g2.cirList[3])
        s.shift(2*LEFT, g2.cirList[4])

        g2.cirList[5].move_to([-1, -1, 0])

        s.play(Write(g2.cirList[5]),
               Write(g2.labelList[5]))
        s.play(Write(g2.edgeList[5]),
               Write(g2.edgeList[6]),
               Write(g2.edgeList[7]))
        s.play(Write(g2.edgeLabelList[5]),
               Write(g2.edgeLabelList[6]),
               Write(g2.edgeLabelList[7]))

        s.wait()

        s.Flash(g2.cirList[4])
        s.wait()
        s.ChangeColor(g2.cirList[4], ORANGE)
        s.ChangeColor(g2.edgeList[4], YELLOW)

        s.shift(UP*1.5+RIGHT, g2.cirList[4])
        shortest.add(g2.cirList[4])
        r1 = SurroundingRectangle(shortest)
        s.ReplaceTransform(r2, r1)

        s.show(g2.edgeList[9], g2.edgeLabelList[9])
        s.wait()

        s.Flash(g2.cirList[3])
        s.wait()
        s.ChangeColor(g2.cirList[3], ORANGE)
        s.ChangeColor(g2.edgeList[7], YELLOW)

        s.shift(UP * 1.5 + LEFT, g2.cirList[3])
        shortest.add(g2.cirList[3])
        r2 = SurroundingRectangle(shortest)
        s.ReplaceTransform(r1, r2)

        s.show(g2.edgeList[8], g2.edgeLabelList[8])
        s.wait()

        s.Flash(g2.cirList[5])
        s.wait()
        s.ChangeColor(g2.cirList[5], ORANGE)
        s.ChangeColor(g2.edgeList[9], YELLOW)
        shortest.add(g2.cirList[5])
        r1 = SurroundingRectangle(shortest)
        s.ReplaceTransform(r2, r1)
        s.wait()
        s.disappear(r1)
        s.disappear(g2.edgeList[1],
                    g2.edgeList[2],
                    g2.edgeList[5],
                    g2.edgeList[6],
                    g2.edgeList[8],
                    g2.edgeLabelList[1],
                    g2.edgeLabelList[2],
                    g2.edgeLabelList[5],
                    g2.edgeLabelList[6],
                    g2.edgeLabelList[8],
                    )
        s.wait()
        s.play(g2.cirList[0].animate.move_to([0, 3, 0]),
               g2.cirList[1].animate.move_to([0, 1.5, 0]),
               g2.cirList[2].animate.move_to([1, 0, 0]),
               g2.cirList[3].animate.move_to([2, -1.5, 0]),
               g2.cirList[4].animate.move_to([-1, 0, 0]),
               g2.cirList[5].animate.move_to([-2, -1.5, 0]),)
        s.wait(2)

