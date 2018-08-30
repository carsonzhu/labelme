from qtpy import QT_VERSION
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

QT5 = QT_VERSION[0] == '5'  # NOQA

import labelme.utils

class ExportDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(ExportDialog, self).__init__(parent)

        self.setWindowTitle("Export Masks Dialog")

        layout = QtWidgets.QVBoxLayout()

        self.instance_seg = QtWidgets.QRadioButton('VOC-like dataset for instance segmentation')
        self.semantic_seg = QtWidgets.QRadioButton('VOC-like dataset for semantic segmentation')

        self.instance_seg.setChecked(True)
        layout.addWidget(self.instance_seg)
        layout.addWidget(self.semantic_seg)

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.instance_seg, 0)
        self.button_group.addButton(self.semantic_seg, 1)

        # buttons
        self.buttonBox = bb = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self,
        )
        bb.button(bb.Ok).setIcon(labelme.utils.newIcon('done'))
        bb.button(bb.Cancel).setIcon(labelme.utils.newIcon('undo'))
        bb.accepted.connect(self.confirm)
        bb.rejected.connect(self.cancel_action)
        layout.addWidget(bb)
        self.setLayout(layout)

    def confirm(self):
        self.accept()

    def cancel_action(self):
        self.reject()

    def GetSelectedId(self):
        return self.button_group.checkedId()