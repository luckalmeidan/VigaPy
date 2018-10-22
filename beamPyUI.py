# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Lucas\PycharmProjects\BeamProject\beamPyUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1413, 670)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.main_gl = QtGui.QGridLayout()
        self.main_gl.setObjectName(_fromUtf8("main_gl"))
        self.load_treeview = QtGui.QTreeView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_treeview.sizePolicy().hasHeightForWidth())
        self.load_treeview.setSizePolicy(sizePolicy)
        self.load_treeview.setMinimumSize(QtCore.QSize(500, 0))
        self.load_treeview.setObjectName(_fromUtf8("load_treeview"))
        self.main_gl.addWidget(self.load_treeview, 1, 1, 2, 1)
        self.beam_draw_widget = QtGui.QWidget(self.centralwidget)
        self.beam_draw_widget.setObjectName(_fromUtf8("beam_draw_widget"))
        self.beam_draw_widget_vl = QtGui.QVBoxLayout(self.beam_draw_widget)
        self.beam_draw_widget_vl.setObjectName(_fromUtf8("beam_draw_widget_vl"))
        self.main_gl.addWidget(self.beam_draw_widget, 0, 0, 1, 3)
        self.add_remove_hl = QtGui.QHBoxLayout()
        self.add_remove_hl.setObjectName(_fromUtf8("add_remove_hl"))
        self.add_load_btn = QtGui.QPushButton(self.centralwidget)
        self.add_load_btn.setObjectName(_fromUtf8("add_load_btn"))
        self.add_remove_hl.addWidget(self.add_load_btn)
        self.remove_load_btn = QtGui.QPushButton(self.centralwidget)
        self.remove_load_btn.setObjectName(_fromUtf8("remove_load_btn"))
        self.add_remove_hl.addWidget(self.remove_load_btn)
        self.main_gl.addLayout(self.add_remove_hl, 2, 2, 1, 1)
        self.properties_supports_vl = QtGui.QGridLayout()
        self.properties_supports_vl.setObjectName(_fromUtf8("properties_supports_vl"))
        self.beam_properties_gb = QtGui.QGroupBox(self.centralwidget)
        self.beam_properties_gb.setObjectName(_fromUtf8("beam_properties_gb"))
        self.beam_properties_gb_vl = QtGui.QGridLayout(self.beam_properties_gb)
        self.beam_properties_gb_vl.setObjectName(_fromUtf8("beam_properties_gb_vl"))
        self.nl_dspn = QtGui.QDoubleSpinBox(self.beam_properties_gb)
        self.nl_dspn.setDecimals(4)
        self.nl_dspn.setMinimum(-9999.0)
        self.nl_dspn.setMaximum(9999.0)
        self.nl_dspn.setProperty("value", 0.0)
        self.nl_dspn.setObjectName(_fromUtf8("nl_dspn"))
        self.beam_properties_gb_vl.addWidget(self.nl_dspn, 4, 1, 1, 2)
        self.lbl_length_2 = QtGui.QLabel(self.beam_properties_gb)
        self.lbl_length_2.setObjectName(_fromUtf8("lbl_length_2"))
        self.beam_properties_gb_vl.addWidget(self.lbl_length_2, 4, 0, 1, 1)
        self.lbl_inertia_moment = QtGui.QLabel(self.beam_properties_gb)
        self.lbl_inertia_moment.setObjectName(_fromUtf8("lbl_inertia_moment"))
        self.beam_properties_gb_vl.addWidget(self.lbl_inertia_moment, 1, 0, 1, 1)
        self.lbl_height = QtGui.QLabel(self.beam_properties_gb)
        self.lbl_height.setObjectName(_fromUtf8("lbl_height"))
        self.beam_properties_gb_vl.addWidget(self.lbl_height, 2, 0, 1, 1)
        self.inertia_moment_dspn = QtGui.QDoubleSpinBox(self.beam_properties_gb)
        self.inertia_moment_dspn.setDecimals(4)
        self.inertia_moment_dspn.setMinimum(0.0001)
        self.inertia_moment_dspn.setMaximum(9999.0)
        self.inertia_moment_dspn.setProperty("value", 10.0)
        self.inertia_moment_dspn.setObjectName(_fromUtf8("inertia_moment_dspn"))
        self.beam_properties_gb_vl.addWidget(self.inertia_moment_dspn, 1, 1, 1, 2)
        self.lbl_young_module = QtGui.QLabel(self.beam_properties_gb)
        self.lbl_young_module.setObjectName(_fromUtf8("lbl_young_module"))
        self.beam_properties_gb_vl.addWidget(self.lbl_young_module, 0, 0, 1, 1)
        self.young_module_dpsn = QtGui.QDoubleSpinBox(self.beam_properties_gb)
        self.young_module_dpsn.setMinimum(1.0)
        self.young_module_dpsn.setMaximum(99999.0)
        self.young_module_dpsn.setSingleStep(10.0)
        self.young_module_dpsn.setProperty("value", 200.0)
        self.young_module_dpsn.setObjectName(_fromUtf8("young_module_dpsn"))
        self.beam_properties_gb_vl.addWidget(self.young_module_dpsn, 0, 1, 1, 2)
        self.height_dpsn = QtGui.QDoubleSpinBox(self.beam_properties_gb)
        self.height_dpsn.setDecimals(4)
        self.height_dpsn.setMinimum(0.0001)
        self.height_dpsn.setMaximum(9999.0)
        self.height_dpsn.setProperty("value", 2.0)
        self.height_dpsn.setObjectName(_fromUtf8("height_dpsn"))
        self.beam_properties_gb_vl.addWidget(self.height_dpsn, 2, 1, 1, 2)
        self.lbl_length = QtGui.QLabel(self.beam_properties_gb)
        self.lbl_length.setObjectName(_fromUtf8("lbl_length"))
        self.beam_properties_gb_vl.addWidget(self.lbl_length, 5, 0, 1, 1)
        self.length_dspn = QtGui.QDoubleSpinBox(self.beam_properties_gb)
        self.length_dspn.setDecimals(4)
        self.length_dspn.setMinimum(0.0001)
        self.length_dspn.setMaximum(9999.0)
        self.length_dspn.setProperty("value", 10.0)
        self.length_dspn.setObjectName(_fromUtf8("length_dspn"))
        self.beam_properties_gb_vl.addWidget(self.length_dspn, 5, 1, 1, 2)
        self.properties_supports_vl.addWidget(self.beam_properties_gb, 1, 0, 1, 1)
        self.calculate_beam = QtGui.QPushButton(self.centralwidget)
        self.calculate_beam.setObjectName(_fromUtf8("calculate_beam"))
        self.properties_supports_vl.addWidget(self.calculate_beam, 3, 0, 1, 1)
        self.supports_gb = QtGui.QGroupBox(self.centralwidget)
        self.supports_gb.setObjectName(_fromUtf8("supports_gb"))
        self.supports_gb_gl = QtGui.QGridLayout(self.supports_gb)
        self.supports_gb_gl.setObjectName(_fromUtf8("supports_gb_gl"))
        self.lbl_add_support = QtGui.QLabel(self.supports_gb)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_add_support.sizePolicy().hasHeightForWidth())
        self.lbl_add_support.setSizePolicy(sizePolicy)
        self.lbl_add_support.setObjectName(_fromUtf8("lbl_add_support"))
        self.supports_gb_gl.addWidget(self.lbl_add_support, 2, 0, 1, 1)
        self.lbl_left_support = QtGui.QLabel(self.supports_gb)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_left_support.sizePolicy().hasHeightForWidth())
        self.lbl_left_support.setSizePolicy(sizePolicy)
        self.lbl_left_support.setObjectName(_fromUtf8("lbl_left_support"))
        self.supports_gb_gl.addWidget(self.lbl_left_support, 0, 0, 1, 1)
        self.supports_combo = QtGui.QComboBox(self.supports_gb)
        self.supports_combo.setEditable(True)
        self.supports_combo.setDuplicatesEnabled(False)
        self.supports_combo.setObjectName(_fromUtf8("supports_combo"))
        self.supports_gb_gl.addWidget(self.supports_combo, 3, 0, 1, 1)
        self.lbl_right_support = QtGui.QLabel(self.supports_gb)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_right_support.sizePolicy().hasHeightForWidth())
        self.lbl_right_support.setSizePolicy(sizePolicy)
        self.lbl_right_support.setObjectName(_fromUtf8("lbl_right_support"))
        self.supports_gb_gl.addWidget(self.lbl_right_support, 0, 1, 1, 1)
        self.left_support_combo = QtGui.QComboBox(self.supports_gb)
        self.left_support_combo.setObjectName(_fromUtf8("left_support_combo"))
        self.left_support_combo.addItem(_fromUtf8(""))
        self.left_support_combo.addItem(_fromUtf8(""))
        self.left_support_combo.addItem(_fromUtf8(""))
        self.supports_gb_gl.addWidget(self.left_support_combo, 1, 0, 1, 1)
        self.right_support_combo = QtGui.QComboBox(self.supports_gb)
        self.right_support_combo.setObjectName(_fromUtf8("right_support_combo"))
        self.right_support_combo.addItem(_fromUtf8(""))
        self.right_support_combo.addItem(_fromUtf8(""))
        self.right_support_combo.addItem(_fromUtf8(""))
        self.supports_gb_gl.addWidget(self.right_support_combo, 1, 1, 1, 1)
        self.remove_support_btn = QtGui.QPushButton(self.supports_gb)
        self.remove_support_btn.setObjectName(_fromUtf8("remove_support_btn"))
        self.supports_gb_gl.addWidget(self.remove_support_btn, 4, 0, 1, 1)
        self.lbl_add_support_2 = QtGui.QLabel(self.supports_gb)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_add_support_2.sizePolicy().hasHeightForWidth())
        self.lbl_add_support_2.setSizePolicy(sizePolicy)
        self.lbl_add_support_2.setObjectName(_fromUtf8("lbl_add_support_2"))
        self.supports_gb_gl.addWidget(self.lbl_add_support_2, 2, 1, 1, 1)
        self.hinges_combo = QtGui.QComboBox(self.supports_gb)
        self.hinges_combo.setEditable(True)
        self.hinges_combo.setDuplicatesEnabled(False)
        self.hinges_combo.setObjectName(_fromUtf8("hinges_combo"))
        self.supports_gb_gl.addWidget(self.hinges_combo, 3, 1, 1, 1)
        self.remove_hinge_btn = QtGui.QPushButton(self.supports_gb)
        self.remove_hinge_btn.setObjectName(_fromUtf8("remove_hinge_btn"))
        self.supports_gb_gl.addWidget(self.remove_hinge_btn, 4, 1, 1, 1)
        self.properties_supports_vl.addWidget(self.supports_gb, 2, 0, 1, 1)
        self.main_gl.addLayout(self.properties_supports_vl, 1, 0, 2, 1)
        self.loads_tab = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loads_tab.sizePolicy().hasHeightForWidth())
        self.loads_tab.setSizePolicy(sizePolicy)
        self.loads_tab.setObjectName(_fromUtf8("loads_tab"))
        self.pnt_load_tab_widget = QtGui.QWidget()
        self.pnt_load_tab_widget.setObjectName(_fromUtf8("pnt_load_tab_widget"))
        self.pnt_load_tab_widget_gl_4 = QtGui.QGridLayout(self.pnt_load_tab_widget)
        self.pnt_load_tab_widget_gl_4.setHorizontalSpacing(0)
        self.pnt_load_tab_widget_gl_4.setObjectName(_fromUtf8("pnt_load_tab_widget_gl_4"))
        self.pnt_load_up_chkbtn = QtGui.QPushButton(self.pnt_load_tab_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnt_load_up_chkbtn.sizePolicy().hasHeightForWidth())
        self.pnt_load_up_chkbtn.setSizePolicy(sizePolicy)
        self.pnt_load_up_chkbtn.setMinimumSize(QtCore.QSize(100, 100))
        self.pnt_load_up_chkbtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.pnt_load_up_chkbtn.setCheckable(True)
        self.pnt_load_up_chkbtn.setAutoExclusive(True)
        self.pnt_load_up_chkbtn.setObjectName(_fromUtf8("pnt_load_up_chkbtn"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.pnt_load_up_chkbtn)
        self.pnt_load_tab_widget_gl_4.addWidget(self.pnt_load_up_chkbtn, 0, 0, 1, 1)
        self.pnt_load_down_chkbtn = QtGui.QPushButton(self.pnt_load_tab_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnt_load_down_chkbtn.sizePolicy().hasHeightForWidth())
        self.pnt_load_down_chkbtn.setSizePolicy(sizePolicy)
        self.pnt_load_down_chkbtn.setMinimumSize(QtCore.QSize(100, 100))
        self.pnt_load_down_chkbtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.pnt_load_down_chkbtn.setCheckable(True)
        self.pnt_load_down_chkbtn.setChecked(True)
        self.pnt_load_down_chkbtn.setAutoExclusive(True)
        self.pnt_load_down_chkbtn.setObjectName(_fromUtf8("pnt_load_down_chkbtn"))
        self.buttonGroup.addButton(self.pnt_load_down_chkbtn)
        self.pnt_load_tab_widget_gl_4.addWidget(self.pnt_load_down_chkbtn, 0, 1, 1, 1)
        self.lbl_point_load_mag = QtGui.QLabel(self.pnt_load_tab_widget)
        self.lbl_point_load_mag.setObjectName(_fromUtf8("lbl_point_load_mag"))
        self.pnt_load_tab_widget_gl_4.addWidget(self.lbl_point_load_mag, 2, 0, 1, 1)
        self.pnt_load_mag_dpsn = QtGui.QDoubleSpinBox(self.pnt_load_tab_widget)
        self.pnt_load_mag_dpsn.setDecimals(2)
        self.pnt_load_mag_dpsn.setMinimum(0.0)
        self.pnt_load_mag_dpsn.setMaximum(9999.0)
        self.pnt_load_mag_dpsn.setProperty("value", 5.0)
        self.pnt_load_mag_dpsn.setObjectName(_fromUtf8("pnt_load_mag_dpsn"))
        self.pnt_load_tab_widget_gl_4.addWidget(self.pnt_load_mag_dpsn, 2, 1, 1, 1)
        self.lbl_point_load_pos = QtGui.QLabel(self.pnt_load_tab_widget)
        self.lbl_point_load_pos.setObjectName(_fromUtf8("lbl_point_load_pos"))
        self.pnt_load_tab_widget_gl_4.addWidget(self.lbl_point_load_pos, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.pnt_load_tab_widget_gl_4.addItem(spacerItem, 1, 0, 1, 2)
        self.pnt_load_pos_dpsn = QtGui.QDoubleSpinBox(self.pnt_load_tab_widget)
        self.pnt_load_pos_dpsn.setMaximum(9999.0)
        self.pnt_load_pos_dpsn.setProperty("value", 5.0)
        self.pnt_load_pos_dpsn.setObjectName(_fromUtf8("pnt_load_pos_dpsn"))
        self.pnt_load_tab_widget_gl_4.addWidget(self.pnt_load_pos_dpsn, 3, 1, 1, 1)
        self.loads_tab.addTab(self.pnt_load_tab_widget, _fromUtf8(""))
        self.moment_tab_widget = QtGui.QWidget()
        self.moment_tab_widget.setObjectName(_fromUtf8("moment_tab_widget"))
        self.pnt_load_tab_widget_gl = QtGui.QGridLayout(self.moment_tab_widget)
        self.pnt_load_tab_widget_gl.setHorizontalSpacing(0)
        self.pnt_load_tab_widget_gl.setObjectName(_fromUtf8("pnt_load_tab_widget_gl"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.pnt_load_tab_widget_gl.addItem(spacerItem1, 1, 0, 1, 2)
        self.moment_pos_dpsn = QtGui.QDoubleSpinBox(self.moment_tab_widget)
        self.moment_pos_dpsn.setObjectName(_fromUtf8("moment_pos_dpsn"))
        self.pnt_load_tab_widget_gl.addWidget(self.moment_pos_dpsn, 4, 1, 1, 1)
        self.moment_ccw_chkbtn = QtGui.QPushButton(self.moment_tab_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moment_ccw_chkbtn.sizePolicy().hasHeightForWidth())
        self.moment_ccw_chkbtn.setSizePolicy(sizePolicy)
        self.moment_ccw_chkbtn.setMinimumSize(QtCore.QSize(100, 100))
        self.moment_ccw_chkbtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.moment_ccw_chkbtn.setCheckable(True)
        self.moment_ccw_chkbtn.setAutoExclusive(True)
        self.moment_ccw_chkbtn.setObjectName(_fromUtf8("moment_ccw_chkbtn"))
        self.pnt_load_tab_widget_gl.addWidget(self.moment_ccw_chkbtn, 0, 1, 1, 1)
        self.lbl_moment_pos = QtGui.QLabel(self.moment_tab_widget)
        self.lbl_moment_pos.setObjectName(_fromUtf8("lbl_moment_pos"))
        self.pnt_load_tab_widget_gl.addWidget(self.lbl_moment_pos, 3, 0, 1, 1)
        self.lbl_moment_mag = QtGui.QLabel(self.moment_tab_widget)
        self.lbl_moment_mag.setObjectName(_fromUtf8("lbl_moment_mag"))
        self.pnt_load_tab_widget_gl.addWidget(self.lbl_moment_mag, 4, 0, 1, 1)
        self.moment_mag_dpsn = QtGui.QDoubleSpinBox(self.moment_tab_widget)
        self.moment_mag_dpsn.setObjectName(_fromUtf8("moment_mag_dpsn"))
        self.pnt_load_tab_widget_gl.addWidget(self.moment_mag_dpsn, 3, 1, 1, 1)
        self.moment_cw_chkbtn = QtGui.QPushButton(self.moment_tab_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moment_cw_chkbtn.sizePolicy().hasHeightForWidth())
        self.moment_cw_chkbtn.setSizePolicy(sizePolicy)
        self.moment_cw_chkbtn.setMinimumSize(QtCore.QSize(100, 100))
        self.moment_cw_chkbtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.moment_cw_chkbtn.setCheckable(True)
        self.moment_cw_chkbtn.setChecked(True)
        self.moment_cw_chkbtn.setAutoExclusive(True)
        self.moment_cw_chkbtn.setObjectName(_fromUtf8("moment_cw_chkbtn"))
        self.pnt_load_tab_widget_gl.addWidget(self.moment_cw_chkbtn, 0, 0, 1, 1)
        self.loads_tab.addTab(self.moment_tab_widget, _fromUtf8(""))
        self.distr_load_tab_widget = QtGui.QWidget()
        self.distr_load_tab_widget.setObjectName(_fromUtf8("distr_load_tab_widget"))
        self.distr_load_tab_widget_gl = QtGui.QGridLayout(self.distr_load_tab_widget)
        self.distr_load_tab_widget_gl.setHorizontalSpacing(0)
        self.distr_load_tab_widget_gl.setObjectName(_fromUtf8("distr_load_tab_widget_gl"))
        self.down_distr_load_chkbtn = QtGui.QPushButton(self.distr_load_tab_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.down_distr_load_chkbtn.sizePolicy().hasHeightForWidth())
        self.down_distr_load_chkbtn.setSizePolicy(sizePolicy)
        self.down_distr_load_chkbtn.setMinimumSize(QtCore.QSize(100, 100))
        self.down_distr_load_chkbtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.down_distr_load_chkbtn.setCheckable(True)
        self.down_distr_load_chkbtn.setChecked(True)
        self.down_distr_load_chkbtn.setAutoExclusive(True)
        self.down_distr_load_chkbtn.setObjectName(_fromUtf8("down_distr_load_chkbtn"))
        self.distr_load_tab_widget_gl.addWidget(self.down_distr_load_chkbtn, 0, 1, 1, 1)
        self.up_distr_load_chkbtn = QtGui.QPushButton(self.distr_load_tab_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.up_distr_load_chkbtn.sizePolicy().hasHeightForWidth())
        self.up_distr_load_chkbtn.setSizePolicy(sizePolicy)
        self.up_distr_load_chkbtn.setMinimumSize(QtCore.QSize(100, 100))
        self.up_distr_load_chkbtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.up_distr_load_chkbtn.setCheckable(True)
        self.up_distr_load_chkbtn.setChecked(False)
        self.up_distr_load_chkbtn.setAutoExclusive(True)
        self.up_distr_load_chkbtn.setObjectName(_fromUtf8("up_distr_load_chkbtn"))
        self.distr_load_tab_widget_gl.addWidget(self.up_distr_load_chkbtn, 0, 0, 1, 1)
        self.lbl_start_distr_load_pos = QtGui.QLabel(self.distr_load_tab_widget)
        self.lbl_start_distr_load_pos.setObjectName(_fromUtf8("lbl_start_distr_load_pos"))
        self.distr_load_tab_widget_gl.addWidget(self.lbl_start_distr_load_pos, 3, 0, 1, 1)
        self.lbl_start_distr_load_mag = QtGui.QLabel(self.distr_load_tab_widget)
        self.lbl_start_distr_load_mag.setObjectName(_fromUtf8("lbl_start_distr_load_mag"))
        self.distr_load_tab_widget_gl.addWidget(self.lbl_start_distr_load_mag, 2, 0, 1, 1)
        self.lbl_end_distr_load_pos = QtGui.QLabel(self.distr_load_tab_widget)
        self.lbl_end_distr_load_pos.setObjectName(_fromUtf8("lbl_end_distr_load_pos"))
        self.distr_load_tab_widget_gl.addWidget(self.lbl_end_distr_load_pos, 5, 0, 1, 1)
        self.lbl_end_distr_load_mag = QtGui.QLabel(self.distr_load_tab_widget)
        self.lbl_end_distr_load_mag.setObjectName(_fromUtf8("lbl_end_distr_load_mag"))
        self.distr_load_tab_widget_gl.addWidget(self.lbl_end_distr_load_mag, 4, 0, 1, 1)
        self.distr_load_start_mag = QtGui.QDoubleSpinBox(self.distr_load_tab_widget)
        self.distr_load_start_mag.setObjectName(_fromUtf8("distr_load_start_mag"))
        self.distr_load_tab_widget_gl.addWidget(self.distr_load_start_mag, 2, 1, 1, 1)
        self.distr_load_start_pos = QtGui.QDoubleSpinBox(self.distr_load_tab_widget)
        self.distr_load_start_pos.setObjectName(_fromUtf8("distr_load_start_pos"))
        self.distr_load_tab_widget_gl.addWidget(self.distr_load_start_pos, 3, 1, 1, 1)
        self.distr_load_end_mag = QtGui.QDoubleSpinBox(self.distr_load_tab_widget)
        self.distr_load_end_mag.setObjectName(_fromUtf8("distr_load_end_mag"))
        self.distr_load_tab_widget_gl.addWidget(self.distr_load_end_mag, 4, 1, 1, 1)
        self.distr_load_end_pos = QtGui.QDoubleSpinBox(self.distr_load_tab_widget)
        self.distr_load_end_pos.setObjectName(_fromUtf8("distr_load_end_pos"))
        self.distr_load_tab_widget_gl.addWidget(self.distr_load_end_pos, 5, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.distr_load_tab_widget_gl.addItem(spacerItem2, 1, 0, 1, 2)
        self.loads_tab.addTab(self.distr_load_tab_widget, _fromUtf8(""))
        self.main_gl.addWidget(self.loads_tab, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.main_gl)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1413, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.plot_dock = QtGui.QDockWidget(MainWindow)
        self.plot_dock.setMinimumSize(QtCore.QSize(400, 58))
        self.plot_dock.setObjectName(_fromUtf8("plot_dock"))
        self.plot_dock_contents = QtGui.QWidget()
        self.plot_dock_contents.setObjectName(_fromUtf8("plot_dock_contents"))
        self.plot_dock_contents_vl = QtGui.QVBoxLayout(self.plot_dock_contents)
        self.plot_dock_contents_vl.setMargin(0)
        self.plot_dock_contents_vl.setSpacing(0)
        self.plot_dock_contents_vl.setObjectName(_fromUtf8("plot_dock_contents_vl"))
        self.plots_widget = QtGui.QWidget(self.plot_dock_contents)
        self.plots_widget.setObjectName(_fromUtf8("plots_widget"))
        self.plots_widget_vl = QtGui.QVBoxLayout(self.plots_widget)
        self.plots_widget_vl.setMargin(0)
        self.plots_widget_vl.setSpacing(0)
        self.plots_widget_vl.setObjectName(_fromUtf8("plots_widget_vl"))
        self.plot_dock_contents_vl.addWidget(self.plots_widget)
        self.plot_dock.setWidget(self.plot_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.plot_dock)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.loads_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.add_load_btn.setText(_translate("MainWindow", "Add", None))
        self.remove_load_btn.setText(_translate("MainWindow", "Remove Selected", None))
        self.beam_properties_gb.setTitle(_translate("MainWindow", "Beam Properties", None))
        self.lbl_length_2.setText(_translate("MainWindow", "Neutral Line (m)", None))
        self.lbl_inertia_moment.setText(_translate("MainWindow", "Inertia (m^4)", None))
        self.lbl_height.setText(_translate("MainWindow", "Height (m)", None))
        self.lbl_young_module.setText(_translate("MainWindow", "E (GPa)", None))
        self.lbl_length.setText(_translate("MainWindow", "Length (m)", None))
        self.calculate_beam.setText(_translate("MainWindow", "Calculate", None))
        self.supports_gb.setTitle(_translate("MainWindow", "Supports", None))
        self.lbl_add_support.setText(_translate("MainWindow", "Add Supports", None))
        self.lbl_left_support.setText(_translate("MainWindow", "Left Support", None))
        self.lbl_right_support.setText(_translate("MainWindow", "Right Support", None))
        self.left_support_combo.setItemText(0, _translate("MainWindow", "Simply", None))
        self.left_support_combo.setItemText(1, _translate("MainWindow", "Fixed", None))
        self.left_support_combo.setItemText(2, _translate("MainWindow", "Free", None))
        self.right_support_combo.setItemText(0, _translate("MainWindow", "Simply", None))
        self.right_support_combo.setItemText(1, _translate("MainWindow", "Fixed", None))
        self.right_support_combo.setItemText(2, _translate("MainWindow", "Free", None))
        self.remove_support_btn.setText(_translate("MainWindow", "Remove Support", None))
        self.lbl_add_support_2.setText(_translate("MainWindow", "Add Hinges", None))
        self.remove_hinge_btn.setText(_translate("MainWindow", "Remove Hinge", None))
        self.pnt_load_up_chkbtn.setText(_translate("MainWindow", "Up", None))
        self.pnt_load_down_chkbtn.setText(_translate("MainWindow", "Down", None))
        self.lbl_point_load_mag.setText(_translate("MainWindow", "Load Magnitude:", None))
        self.lbl_point_load_pos.setText(_translate("MainWindow", "Load Position: ", None))
        self.loads_tab.setTabText(self.loads_tab.indexOf(self.pnt_load_tab_widget), _translate("MainWindow", "Point Load", None))
        self.moment_ccw_chkbtn.setText(_translate("MainWindow", "CCW", None))
        self.lbl_moment_pos.setText(_translate("MainWindow", "Moment Magnitude:", None))
        self.lbl_moment_mag.setText(_translate("MainWindow", "Moment Position: ", None))
        self.moment_cw_chkbtn.setText(_translate("MainWindow", "CW", None))
        self.loads_tab.setTabText(self.loads_tab.indexOf(self.moment_tab_widget), _translate("MainWindow", "Moment", None))
        self.down_distr_load_chkbtn.setText(_translate("MainWindow", "Down", None))
        self.up_distr_load_chkbtn.setText(_translate("MainWindow", "Up", None))
        self.lbl_start_distr_load_pos.setText(_translate("MainWindow", "Start Position: ", None))
        self.lbl_start_distr_load_mag.setText(_translate("MainWindow", "Start Magnitude:", None))
        self.lbl_end_distr_load_pos.setText(_translate("MainWindow", "End Position: ", None))
        self.lbl_end_distr_load_mag.setText(_translate("MainWindow", "End Magnitude:", None))
        self.loads_tab.setTabText(self.loads_tab.indexOf(self.distr_load_tab_widget), _translate("MainWindow", "Distributed Load", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.plot_dock.setWindowTitle(_translate("MainWindow", "Shear, bending, angle and displacement diagrams", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

