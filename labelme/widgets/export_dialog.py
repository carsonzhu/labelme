#-*- coding: UTF-8 -*- 
from qtpy import QT_VERSION
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

from labelme.utils import exportVOC_semantic
from labelme.utils import exportVOC_instance
from labelme.utils import exportMITP_grasp
from labelme.utils import exportMITP_suction

QT5 = QT_VERSION[0] == '5'  # NOQA

import labelme.utils
import shutil
import os.path as osp

class ExportDialog(QtWidgets.QDialog):
    def __init__(self, parent , in_dir):
        super(ExportDialog, self).__init__(parent)

        self.setWindowTitle("Export Masks Dialog")

        layout = QtWidgets.QVBoxLayout()

        self.in_directory = in_dir

        self.instance_seg = QtWidgets.QRadioButton('VOC-like dataset for instance segmentation')
        self.semantic_seg = QtWidgets.QRadioButton('VOC-like dataset for semantic segmentation')
        self.grasp_seg = QtWidgets.QRadioButton('parallel-jaw-grasping dataset')
        self.suction_seg = QtWidgets.QRadioButton('suction-based-grasping dataset')

        self.instance_seg.setChecked(True)
        layout.addWidget(self.instance_seg)
        layout.addWidget(self.semantic_seg)
        layout.addWidget(self.grasp_seg)
        layout.addWidget(self.suction_seg)

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.instance_seg, 0)
        self.button_group.addButton(self.semantic_seg, 1)
        self.button_group.addButton(self.grasp_seg, 2)
        self.button_group.addButton(self.suction_seg, 3)

        # buttons
        self.buttonBox = bb = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self,
        )
        bb.button(bb.Ok).setText("&Export")
        bb.button(bb.Ok).setIcon(labelme.utils.newIcon('done'))
        bb.button(bb.Cancel).setIcon(labelme.utils.newIcon('undo'))
        bb.accepted.connect(self.confirm)
        bb.rejected.connect(self.cancel_action)
        layout.addWidget(bb)
        self.setLayout(layout)

    def confirm(self):
        self.accept()
        out_dir_instance = self.in_directory + "_voc_instance"
        out_dir_semantic = self.in_directory + "_voc_semantic"
        out_dir_grasp = self.in_directory + "_grasp"
        out_dir_suction = self.in_directory + "_suction"
        labels_file = osp.join(osp.join(self.in_directory, ".."), "labels.txt")
        if osp.exists(labels_file) == False:
            print('labels_file does not exist:', labels_file)
            QtWidgets.QMessageBox.warning(self,"warning","labels file does not exist: " + labels_file + " , Please create a valid labels file before exporting!", QtWidgets.QMessageBox.Ok)
            return -1
        if self.button_group.checkedId() == 0:
            isExist = exportVOC_instance(labels_file, self.in_directory, out_dir_instance)
            if isExist:
                button = QtWidgets.QMessageBox.question(self,"Question","Output directory already exists: " + out_dir_instance + " , Do you want to replace the dirctory？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if button == QtWidgets.QMessageBox.Yes:
                    print("...... Regenerate VOC-like datasets for instance segmenattion ......")
                    shutil.rmtree(out_dir_instance, ignore_errors=True)
                    exportVOC_instance(labels_file, self.in_directory, out_dir_instance)
        elif self.button_group.checkedId() == 1:
            isExist = exportVOC_semantic(labels_file, self.in_directory, out_dir_semantic)
            if isExist:
                button = QtWidgets.QMessageBox.question(self,"Question","Output directory already exists: " + out_dir_semantic + " , Do you want to replace the dirctory？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if button == QtWidgets.QMessageBox.Yes:
                    print("...... Regenerate VOC-like datasets for semantic segmenattion ......")
                    shutil.rmtree(out_dir_semantic, ignore_errors=True)
                    exportVOC_semantic(labels_file, self.in_directory, out_dir_semantic)
        elif self.button_group.checkedId() == 2:
            isExist = exportMITP_grasp(labels_file, self.in_directory, out_dir_grasp)
            if isExist:
                button = QtWidgets.QMessageBox.question(self,"Question","Output directory already exists: " + out_dir_grasp + " , Do you want to replace the dirctory？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if button == QtWidgets.QMessageBox.Yes:
                    print("...... Regenerate grasping datasets ......")
                    shutil.rmtree(out_dir_grasp, ignore_errors=True)
                    exportMITP_grasp(labels_file, self.in_directory, out_dir_grasp)
        elif self.button_group.checkedId() == 3:
            isExist = exportMITP_suction(labels_file, self.in_directory, out_dir_suction)
            if isExist:
                button = QtWidgets.QMessageBox.question(self,"Question","Output directory already exists: " + out_dir_suction + " , Do you want to replace the dirctory？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if button == QtWidgets.QMessageBox.Yes:
                    print("...... Regenerate suction-based grasping datasets ......")
                    shutil.rmtree(out_dir_suction, ignore_errors=True)
                    exportMITP_suction(labels_file, self.in_directory, out_dir_suction)
        
    def cancel_action(self):
        self.reject()

    def GetSelectedId(self):
        return self.button_group.checkedId()