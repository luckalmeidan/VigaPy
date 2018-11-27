import sys

from PyQt4 import QtGui, QtCore

from beampy.beam_solver.definitions import *
from beampy.load_model import LoadNode


class QGraphicArcItem(QtGui.QGraphicsEllipseItem):
    def paint(self):
        pass


class BeamView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 250, 100))

        self.beam_length = 10
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.supports_color = QtCore.Qt.black
        self.loads_color = QtCore.Qt.black

        self.x_s = -40
        self.y_s = 40
        self.v_l = 330

        self.v_width = 15
        self.s_height = 10
        self.a_size = 3

        self.max_load_size = 40

        self.highest_load = 1
        self.factor = self.max_load_size / 1

        self.beam_diagram = QtGui.QGraphicsRectItem(self.x_s, self.y_s, self.v_l, self.v_width)
        self.scene.addItem(self.beam_diagram)

        self.loads = []
        self.supports = []

    def updateView(self, left_hand_support, right_hand_support, support_list, hinge_list, loads):
        self.scene.clear()

        self.factor = self.max_load_size / 20

        self.beam_diagram = QtGui.QGraphicsRectItem(self.x_s, self.y_s, self.v_l, self.v_width)
        self.beam_diagram.setBrush(QtGui.QBrush(7))
        self.scene.addItem(self.beam_diagram)

        self.highest_load = 1
        self.supports = []
        self.hinges = hinge_list

        self.loads = []

        self.supports.append([left_hand_support, 0])

        self.supports.append([right_hand_support, self.beam_length])

        for support in support_list:
            self.supports.append([simply_support, support])

        for support in self.supports:
            self.scene.addItem(self.diagramAddSupport(support[0], support[1]))

        for hinge in self.hinges:
            self.scene.addItem(self.diagramAddHinge(hinge))

        for load in loads:
            if load.pos_1 <= self.beam_length:
                if load.load_type == "P. Load":
                    if abs(load.load_1) > self.highest_load:
                        self.highest_load = abs(load.load_1)

                    self.applyPointLoad(load.load_1, load.pos_1)

                elif load.load_type == "Moment":
                    self.applyMoment(load.load_1, load.pos_1)

                elif load.load_type == "D. Load":
                    if abs(load.load_1) > self.highest_load:
                        self.highest_load = abs(load.load_1)

                    if abs(load.load_2) > self.highest_load:
                        self.highest_load = abs(load.load_2)

                    if load.pos_2 <= self.beam_length:
                        self.applyDistLoad(load.load_1, load.pos_1, load.load_2, load.pos_2)
                    else:
                        print("some loads were not applied due to out of bounds")

                else:
                    print("some loads were not applied due to out of bounds")

        self.factor = self.max_load_size / self.highest_load

        for load in self.loads:
            if load[0] == "moment":
                self.scene.addItem(self.diagramApplyMoment(load[1], load[2]))

            elif load[0] == "point_load":
                self.scene.addItem(self.diagramApplyPointLoad(load[1], load[2]))

            elif load[0] == "dist_load":
                self.scene.addItem(self.diagramApplyDistLoad(load[1], load[2], load[3], load[4]))

    def applyMoment(self, magnitude, distance):
        """

        :param magnitude:
        :param distance:
        :return:
        """

        self.loads.append(["moment", magnitude, distance, 0, 0])

    def applyPointLoad(self, magnitude, distance):

        self.loads.append(["point_load", magnitude, distance, 0, 0])

    def applyDistLoad(self, magnitude_1, distance_1, magnitude_2, distance_2):
        """

        :param magnitude_1:
        :param distance_1:
        :param magnitude_2:
        :param distance_2:
        :return:
        """

        self.loads.append(["dist_load", magnitude_1, distance_1, magnitude_2, distance_2])

    #
    # def __drawSingleLoad(self, magnitude_1,  distance_1):
    #     single_load = QtGui.QGraphicsItemGroup()
    #
    #     load = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_1,
    #                                    self.y_s - magnitude_1 * self.factor,
    #                                    self.x_s + self.v_l / self.beam_length * distance_1,
    #                                    self.y_s)
    #     arrowhead = QtGui.QGraphicsPolygonItem(
    #         QtGui.QPolygonF([QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s),
    #                          QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 - self.a_size,
    #                                        self.y_s - self.a_size * 2),
    #                          QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 + self.a_size,
    #                                        self.y_s - self.a_size * 2)]))
    #
    #     arrowhead.setBrush(QtGui.QBrush(self.loads_color))
    #     arrowhead.setPen(QtGui.QPen(self.loads_color, 1, QtCore.Qt.SolidLine))
    #     load.setPen(QtGui.QPen(self.loads_color, 1, QtCore.Qt.SolidLine))
    #
    #     for member in (load, arrowhead):
    #         single_load.addToGroup(member)
    #
    #     return single_load



    def diagramApplyPointLoad(self, magnitude_1, distance_1):
        diagram_object = QtGui.QGraphicsItemGroup()

        if magnitude_1 < 0:
            magnitude_1 = abs(magnitude_1)

            load = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_1,
                                           self.y_s - magnitude_1 * self.factor,
                                           self.x_s + self.v_l / self.beam_length * distance_1,
                                           self.y_s)
            arrowhead = QtGui.QGraphicsPolygonItem(
                QtGui.QPolygonF([QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s),
                                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 - self.a_size,
                                               self.y_s - self.a_size * 2),
                                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 + self.a_size,
                                               self.y_s - self.a_size * 2)]))

        else:
            magnitude_1 = abs(magnitude_1)

            load = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_1,
                                           self.v_width + self.y_s + magnitude_1 * self.factor,
                                           self.x_s + self.v_l / self.beam_length * distance_1,
                                           self.v_width + self.y_s)

            arrowhead = QtGui.QGraphicsPolygonItem(
                QtGui.QPolygonF(
                    [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s + self.v_width),
                     QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 - self.a_size,
                                   self.y_s + self.v_width + self.a_size * 2),
                     QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 + self.a_size,
                                   self.y_s + self.v_width + self.a_size * 2)]))

        arrowhead.setBrush(QtGui.QBrush(self.loads_color))
        arrowhead.setPen(QtGui.QPen(self.loads_color, 1, QtCore.Qt.SolidLine))
        load.setPen(QtGui.QPen(self.loads_color, 1, QtCore.Qt.SolidLine))

        for member in (load, arrowhead):
            diagram_object.addToGroup(member)

        return diagram_object

    def diagramApplyMoment(self, magnitude_1, distance_1):
        diagram_object = QtGui.QGraphicsItemGroup()

        if magnitude_1 < 0:
            magnitude_1 = abs(magnitude_1)

            path = QtGui.QPainterPath(
                QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s - self.v_width * .25))
            # moment = QtGui.QGraphicsEllipseItem(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s-self.v_width*.15, self.v_width*1.3, self.v_width*1.3)

            b_retangle = QtCore.QRectF(0, 0, self.v_width * 1.5, self.v_width * 1.5)

            b_retangle.moveCenter(
                QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s + self.v_width / 2))
            path.arcTo(b_retangle, 90, -270)
            moment = QtGui.QGraphicsPathItem(path)

            arrowhead = QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(
                [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s - self.v_width * .14),
                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 - self.a_size,
                               self.y_s - self.a_size * 2),
                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 + self.a_size,
                               self.y_s - self.a_size * 2)]))
        else:
            magnitude_1 = abs(magnitude_1)

            path = QtGui.QPainterPath(
                QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s - self.v_width * .25))

            b_retangle = QtCore.QRectF(0, 0, self.v_width * 1.5, self.v_width * 1.5)

            b_retangle.moveCenter(
                QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s + self.v_width / 2))
            path.arcTo(b_retangle, 90, 270)
            moment = QtGui.QGraphicsPathItem(path)

            arrowhead = QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(
                [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s - self.v_width * .14),
                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 - self.a_size,
                               self.y_s - self.a_size * 2),
                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 + self.a_size,
                               self.y_s - self.a_size * 2)]))

        arrowhead.setBrush(QtGui.QBrush(self.loads_color))
        arrowhead.setPen(QtGui.QPen(self.loads_color, 1, QtCore.Qt.SolidLine))
        moment.setPen(QtGui.QPen(self.loads_color, 1.6, QtCore.Qt.SolidLine))

        for member in (moment, arrowhead):
            diagram_object.addToGroup(member)

        return diagram_object

    def diagramAddHinge(self, distance):
        diagram_object = QtGui.QGraphicsItemGroup()

        b_retangle = QtCore.QRectF(0, 0, self.v_width, self.v_width)

        b_retangle.moveCenter(
            QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance, self.y_s + self.v_width / 2))

        hinge = QtGui.QGraphicsEllipseItem(b_retangle)

        hinge.setPen(QtGui.QPen(self.supports_color, 1.3, QtCore.Qt.SolidLine))
        hinge.setBrush(QtCore.Qt.white)

        diagram_object.addToGroup(hinge)

        return diagram_object

    def diagramAddSupport(self, support_type, distance):
        diagram_object = QtGui.QGraphicsItemGroup()

        if support_type is simply_support:
            support = QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(
                [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance, self.y_s + self.v_width),
                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance - self.s_height * .6,
                               self.y_s + self.v_width + self.s_height),
                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance + self.s_height * .6,
                               self.y_s + self.v_width + self.s_height)]))

            support_line = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance - 10,
                                                   self.y_s + self.v_width + self.s_height,
                                                   self.x_s + self.v_l / self.beam_length * distance + 10,
                                                   self.y_s + self.v_width + self.s_height)

            support_hatch = QtGui.QGraphicsRectItem(
                self.x_s + self.v_l / self.beam_length * distance - self.s_height,
                self.y_s + self.v_width + self.s_height,
                self.s_height * 2,
                self.v_width * .45)

            support_hatch.setBrush(QtGui.QBrush(self.supports_color, 12))
            support_hatch.setPen(QtGui.QPen(self.supports_color, 0, 0))
            support.setPen(QtGui.QPen(self.supports_color, 1, QtCore.Qt.SolidLine))
            support_line.setPen(QtGui.QPen(self.supports_color, 1.5, QtCore.Qt.SolidLine))

        elif support_type is fixed_support:
            if distance == 0:
                support = QtGui.QGraphicsPolygonItem()

                support_line = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance,
                                                       self.y_s - self.v_width * .9,
                                                       self.x_s + self.v_l / self.beam_length * distance,
                                                       self.y_s + self.v_width + self.v_width * .9)

                support_hatch = QtGui.QGraphicsRectItem(
                    self.x_s + self.v_l / self.beam_length * distance - self.v_width * .9,
                    self.y_s - self.v_width * .9,
                    self.v_width * .9,
                    self.v_width + self.v_width * 1.8)

            else:
                support = QtGui.QGraphicsPolygonItem()

                support_line = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance, self.y_s - 10,
                                                       self.x_s + self.v_l / self.beam_length * distance,
                                                       self.y_s + self.v_width + 10)
                support_hatch = QtGui.QGraphicsRectItem(self.x_s + self.v_l / self.beam_length * distance,
                                                        self.y_s - 10, 10, self.v_width + 20)

            support_hatch.setBrush(QtGui.QBrush(self.supports_color, 12))
            support_hatch.setPen(QtGui.QPen(self.supports_color, 0, 0))

            support_line.setPen(QtGui.QPen(self.supports_color, 1.5, QtCore.Qt.SolidLine))

        elif support_type is free_support:
            support = QtGui.QGraphicsLineItem()
            support_line = QtGui.QGraphicsLineItem()
            support_hatch = QtGui.QGraphicsRectItem()

        for support_object in (support, support_hatch, support_line):
            diagram_object.addToGroup(support_object)

        return diagram_object

    def diagramApplyDistLoad(self, magnitude_1, distance_1, magnitude_2, distance_2):
        diagram_object = QtGui.QGraphicsItemGroup()

        if magnitude_1 <= 0 and magnitude_2 <= 0:
            magnitude_1 = abs(magnitude_1)
            magnitude_2 = abs(magnitude_2)

            load_start = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_1,
                                                 self.y_s - magnitude_1 * self.factor,
                                                 self.x_s + self.v_l / self.beam_length * distance_1,
                                                 self.y_s)

            arrowhead_start = QtGui.QGraphicsPolygonItem(
                QtGui.QPolygonF([QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s),
                                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 - self.a_size,
                                               self.y_s - self.a_size * 2),
                                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 + self.a_size,
                                               self.y_s - self.a_size * 2)]))

            load_middle = QtGui.QGraphicsLineItem(
                self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0,
                self.y_s - (magnitude_1 + magnitude_2) / 2.0 * self.factor,
                self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0,
                self.y_s)

            arrowhead_middle = QtGui.QGraphicsPolygonItem(
                QtGui.QPolygonF(
                    [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0, self.y_s),
                     QtCore.QPoint(
                         self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0 - self.a_size,
                         self.y_s - self.a_size * 2),
                     QtCore.QPoint(
                         self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0 + self.a_size,
                         self.y_s - self.a_size * 2)]))

            load_end = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_2,
                                               self.y_s - magnitude_2 * self.factor,
                                               self.x_s + self.v_l / self.beam_length * distance_2,
                                               self.y_s)

            arrowhead_end = QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(
                [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_2, self.y_s),
                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_2 - self.a_size,
                               self.y_s - self.a_size * 2),
                 QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_2 + self.a_size,
                               self.y_s - self.a_size * 2)]))

            union_line = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_1,
                                                 self.y_s - magnitude_1 * self.factor,
                                                 self.x_s + self.v_l / self.beam_length * distance_2,
                                                 self.y_s - magnitude_2 * self.factor)
        elif magnitude_1 >= 0 and magnitude_2 >= 0:
            magnitude_1 = abs(magnitude_1)
            magnitude_2 = abs(magnitude_2)

            load_start = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_1,
                                                 self.v_width + self.y_s + magnitude_1 * self.factor,
                                                 self.x_s + self.v_l / self.beam_length * distance_1,
                                                 self.v_width + self.y_s)

            arrowhead_start = QtGui.QGraphicsPolygonItem(
                QtGui.QPolygonF(
                    [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1, self.y_s + self.v_width),
                     QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 - self.a_size,
                                   self.y_s + self.v_width + self.a_size * 2),
                     QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_1 + self.a_size,
                                   self.y_s + self.v_width + self.a_size * 2)]))

            load_end = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_2,
                                               self.v_width + self.y_s + magnitude_2 * self.factor,
                                               self.x_s + self.v_l / self.beam_length * distance_2,
                                               self.y_s + self.v_width)

            load_middle = QtGui.QGraphicsLineItem(
                self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0,
                self.v_width + self.y_s + (magnitude_1 + magnitude_2) / 2.0 * self.factor,
                self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0,
                self.y_s + self.v_width)

            arrowhead_middle = QtGui.QGraphicsPolygonItem(
                QtGui.QPolygonF(
                    [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0,
                                   self.y_s + self.v_width),
                     QtCore.QPoint(
                         self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0 - self.a_size,
                         self.y_s + self.v_width + self.a_size * 2),
                     QtCore.QPoint(
                         self.x_s + self.v_l / self.beam_length * (distance_1 + distance_2) / 2.0 + self.a_size,
                         self.y_s + self.v_width + self.a_size * 2)]))

            arrowhead_end = QtGui.QGraphicsPolygonItem(
                QtGui.QPolygonF(
                    [QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_2, self.y_s + self.v_width),
                     QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_2 - self.a_size,
                                   self.y_s + self.v_width + self.a_size * 2),
                     QtCore.QPoint(self.x_s + self.v_l / self.beam_length * distance_2 + self.a_size,
                                   self.y_s + self.v_width + self.a_size * 2)]))

            union_line = QtGui.QGraphicsLineItem(self.x_s + self.v_l / self.beam_length * distance_1,
                                                 self.y_s + self.v_width + magnitude_1 * self.factor,
                                                 self.x_s + self.v_l / self.beam_length * distance_2,
                                                 self.y_s + self.v_width + magnitude_2 * self.factor)
        else:
            return diagram_object

        for arrow in (arrowhead_start, arrowhead_middle, arrowhead_end):
            arrow.setBrush(QtGui.QBrush(self.loads_color))
            arrow.setPen(QtGui.QPen(self.loads_color, 1, QtCore.Qt.SolidLine))

        for line in (load_start, load_middle, load_end, union_line):
            line.setPen(QtGui.QPen(self.loads_color, 1, QtCore.Qt.SolidLine))

        for member in (load_start, load_end, load_middle, arrowhead_start, arrowhead_middle, arrowhead_end, union_line):
            diagram_object.addToGroup(member)

        return diagram_object


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    root_node = LoadNode("RootNode")

    LoadNode("Point Load", -5, 5, parent=root_node)
    LoadNode("Moment", -10, 2, parent=root_node)
    LoadNode("Distr. Load", -5, 6, -10, 10, parent=root_node)

    left_hand_support = fixed_support
    right_hand_support = simply_support
    support_list = [3]
    hinge_list = [3]

    view = BeamView()
    view.scene.setSceneRect(QtCore.QRectF(-50, -50, 350, 250))

    view.updateView(left_hand_support, right_hand_support, support_list, hinge_list, root_node.children)

    view.show()
    sys.exit(app.exec_())
