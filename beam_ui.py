from PyQt4 import QtCore, QtGui
import pyui_creator
import sys
from beam_solver import solver
from beam_solver.definitions import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from load_model import LoadModel
from load_model import LoadNode

pyui_creator.updateApplication()

import beamPyUI

class BeamApp(QtGui.QMainWindow, beamPyUI.Ui_MainWindow):


    def __init__(self, parent=None):


        super(BeamApp, self).__init__(parent)

        self.ui = beamPyUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.beam = solver.Beam(1, 1, 4)


        self.model = None
        self.root_node = LoadNode("RootNode")
        self.model = LoadModel(self.root_node)

        self.ui.load_treeview.setModel(self.model)

        self.__plot_figure, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(4, 1, sharex=True)
        self.plot_canvas = FigureCanvas(self.__plot_figure)
        self.plot_canvas_toolbar = NavigationToolbar(self.plot_canvas, self, coordinates=True)
        plt.subplots_adjust(top=.98, bottom=.04, right=.95, left=.13, hspace=0.12)

        self.ui.plots_widget_vl.addWidget(self.plot_canvas)
        self.ui.plots_widget_vl.addWidget(self.plot_canvas_toolbar)

        self.__plot_beam = plt.figure(2)
        self.beam_canvas = FigureCanvas(self.__plot_beam)
        self.beam_canvas_toolbar = NavigationToolbar(self.beam_canvas, self, coordinates=True)

        self.ui.beam_draw_widget_vl.addWidget(self.beam_canvas)
        self.ui.beam_draw_widget_vl.addWidget(self.beam_canvas_toolbar)

        self.__plot_beam.set_facecolor('none')
        self.__plot_figure.set_facecolor('none')
        self.ui.length_dspn.valueChanged.connect(self.__setValidators)

        self.ui.calculate_beam.clicked.connect(self.calculateButton)
        self.ui.remove_support_btn.clicked.connect(self.removeSupport)
        self.ui.remove_load_btn.clicked.connect(self.removeLoadItem)
        self.ui.add_load_btn.clicked.connect(self.addLoadItem)
        self.ui.load_treeview.clicked.connect(self.__setSelection)

        self.ui.supports_combo.setValidator(QtGui.QDoubleValidator())

        self.__setValidators()

    def __setValidators(self):
        self.ui.moment_pos_dpsn.setMaximum(self.ui.length_dspn.value())
        self.ui.pnt_load_pos_dpsn.setMaximum(self.ui.length_dspn.value())

        self.ui.distr_load_end_pos.setMaximum(self.ui.length_dspn.value())

        self.ui.distr_load_start_pos.setMaximum(self.ui.length_dspn.value())

    def __setSelection(self, current, old=None):
        self.load_selected = current.internalPointer()


    def setBeamProperties(self):
        self.beam.beam_length = self.ui.length_dspn.value()
        self.beam.young_modulus = self.ui.young_module_dpsn.value()
        self.beam.inertia_moment = self.ui.inertia_moment_dspn.value()

    def setSupports(self):
        if self.ui.left_support_combo.currentText() == "Simply":
            left_support = simply_support

        elif self.ui.left_support_combo.currentText() == "Free":
            left_support = free_support

        elif self.ui.left_support_combo.currentText() == "Fixed":
            left_support = fixed_support

        else:
            assert False, "Something wrong in support definition"
            pass

        if self.ui.right_support_combo.currentText() == "Simply":
            right_support = simply_support

        elif self.ui.right_support_combo.currentText() == "Free":
            right_support = free_support

        elif self.ui.right_support_combo.currentText() == "Fixed":
            right_support = fixed_support

        else:
            assert False, "Something wrong in support definition"
            pass

        self.beam.setBoundary(left_support, right_support)

        support_list = []
        support_list = [(float(self.ui.supports_combo.itemText(i)))
                                     for i in range(self.ui.supports_combo.count()) if float(self.ui.supports_combo.itemText(i)) <= self.ui.length_dspn.value()]

        self.beam.beam_supports = support_list

    def removeSupport(self):
        self.ui.supports_combo.removeItem(self.ui.supports_combo.currentIndex())
        support_list = [float(self.ui.supports_combo.itemText(i))
                                     for i in range(self.ui.supports_combo.count())]

        self.beam.beam_supports = support_list


    def removeLoadItem(self):
        if self.model.rowCount(self.ui.load_treeview.rootIndex()) == 0:
            return

        self.load_selected.parent().removeChild(self.load_selected.row())
        self.model = LoadModel(self.root_node)
        self.ui.load_treeview.setModel(self.model)


        try:
            self.ui.load_treeview.setCurrentIndex(self.model.index(self.model.rowCount(
                self.ui.load_treeview.rootIndex()) - 1, 0, self.ui.load_treeview.rootIndex()))

            self.__setSelection(self.ui.load_treeview.currentIndex(), old=None)

        except IndexError:
            pass


        pass


    def addLoadItem(self):

        if self.ui.loads_tab.currentIndex() == 0:
            assert (self.ui.pnt_load_up_chkbtn.isChecked() or self.ui.pnt_load_down_chkbtn.isChecked()), "No Button checked"
            assert not (self.ui.pnt_load_up_chkbtn.isChecked() and self.ui.pnt_load_down_chkbtn.isChecked()), "Both Button checked"

            if self.ui.pnt_load_up_chkbtn.isChecked():
                magnitude = self.ui.pnt_load_mag_dpsn.value()

            elif self.ui.pnt_load_down_chkbtn.isChecked():
                magnitude = -self.ui.pnt_load_mag_dpsn.value()


            LoadNode("Point Load", magnitude, self.ui.pnt_load_pos_dpsn.value(), parent=self.root_node)

        if self.ui.loads_tab.currentIndex() == 1:
            assert (
            self.ui.moment_cw_chkbtn.isChecked() or self.ui.moment_ccw_chkbtn.isChecked()), "No Button checked"
            assert not (
            self.ui.moment_cw_chkbtn.isChecked() and self.ui.moment_ccw_chkbtn.isChecked()), "Both Button checked"

            if self.ui.moment_cw_chkbtn.isChecked():
                magnitude = self.ui.moment_mag_dpsn.value()

            elif self.ui.moment_ccw_chkbtn.isChecked():
                magnitude = -self.ui.moment_mag_dpsn.value()

            LoadNode("Moment", magnitude, self.ui.moment_pos_dpsn.value(), parent=self.root_node)
            print("Moment")

        if self.ui.loads_tab.currentIndex() == 2:
            assert (
            self.ui.up_distr_load_chkbtn.isChecked() or self.ui.down_distr_load_chkbtn.isChecked()), "No Button checked"
            assert not (
            self.ui.up_distr_load_chkbtn.isChecked() and self.ui.down_distr_load_chkbtn.isChecked()), "Both Button checked"

            if self.ui.up_distr_load_chkbtn.isChecked():
                magnitude_1 = self.ui.distr_load_start_mag.value()
                magnitude_2 = self.ui.distr_load_end_mag.value()

            elif self.ui.down_distr_load_chkbtn.isChecked():
                magnitude_1 = -self.ui.distr_load_start_mag.value()
                magnitude_2 = -self.ui.distr_load_end_mag.value()

            LoadNode("Distr. Load", magnitude_1, self.ui.distr_load_start_pos.value(), magnitude_2,
                     self.ui.distr_load_end_pos.value(), parent=self.root_node)


        self.model = LoadModel(self.root_node)
        self.ui.load_treeview.setModel(self.model)

        self.ui.load_treeview.setCurrentIndex(self.model.index(self.model.rowCount(
            self.ui.load_treeview.rootIndex()) - 1, 0, self.ui.load_treeview.rootIndex()))

        self.__setSelection(self.ui.load_treeview.currentIndex(), old=None)

    def defineLoads(self):
        self.beam.resetLoads()

        for load in self.root_node.children:
            if load.pos_1 <= self.ui.length_dspn.value():
                if load.load_type == "Point Load":
                    self.beam.applyPointLoad(load.load_1, load.pos_1)
                elif load.load_type == "Moment":
                    self.beam.applyMoment(load.load_1, load.pos_1)
                elif load.load_type == "Distr. Load":
                    if load.pos_2 <= self.ui.length_dspn.value():
                        self.beam.applyDistLoad(load.load_1, load.pos_1, load.load_2, load.pos_2)
                    else:
                        print("some loads were not applied due to out of bounds")

                        ### TOO UGLY



            else:
                print("some loads were not applied due to out of bounds")





    def calculateButton(self):
        self.setBeamProperties()
        self.setSupports()
        self.defineLoads()
        self.ax1.cla()
        self.ax2.cla()
        self.ax3.cla()
        self.ax4.cla()

        self.beam.calculate()


        self.beam.plotEquations(self.__plot_figure, (self.ax1, self.ax2, self.ax3, self.ax4))


        self.plot_canvas.draw()

        print("finished")



def main():

    app = QtGui.QApplication(sys.argv)
    # app.setStyle("gtk+")

    beam_app = BeamApp()
    beam_app.show()

    app.exec_()

    # inifile.close()
    sys.exit(app.exec_())
    return main_window


if __name__ == "__main__":
    main()
