import sys
from collections import deque
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class view(QWidget):
    def __init__(self, data):
        super(view, self).__init__()
        self.tree = QTreeView(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Height', 'Weight'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.n_map = {}
        self.importData(data)
        self.tree.expandAll()

    def importData(self, data, parent=None):
        self.model.setRowCount(0)
        if parent is None:
            parent = self.model.invisibleRootItem()
        for node in data:
            parent.appendRow([
                QStandardItem(node['name']),
                QStandardItem(node['data']),
                # QStandardItem(child['weight'])
            ])
            self.n_map[node['name']] = parent.child(parent.rowCount() - 1)
            children = node.get("children", ())
            # for child in children:
            self.importData(children, self.n_map[node['name']])

        # while values:
        #     value = values.popleft()
        #     if value['unique_id'] == 1:
        #         parent = root
        #     else:
        #         pid = value['parent_id']
        #         if pid not in seen:
        #             values.append(value)
        #             continue
        #         parent = seen[pid]
        #     unique_id = value['unique_id']
        #     parent.appendRow([
        #         QStandardItem(value['short_name']),
        #         QStandardItem(value['height']),
        #         QStandardItem(value['weight'])
        #     ])
        #     seen[unique_id] = parent.child(parent.rowCount() - 1)

if __name__ == '__main__':

    data = [
        {'name': 'Test', "data": 2, "children": [
            {'name': 'Test2', "data": 5, },
            {'name': 'Test3', "data": 4, }
        ]
        },
        {'name': 'Test2', "data": 6, "children": [
            {'name': 'Test2', "data": 5, },
            {'name': 'Test3', "data": 4, }
        ]
        },
        # {'unique_id': 2, 'parent_id': 1, 'short_name': 'Class 1', 'height': ' ', 'weight': ' '},
        # {'unique_id': 3, 'parent_id': 2, 'short_name': 'Lucy', 'height': '162', 'weight': '50'},
        # {'unique_id': 4, 'parent_id': 2, 'short_name': 'Joe', 'height': '175', 'weight': '65'},
        # {'unique_id': 5, 'parent_id': 1, 'short_name': 'Class 2', 'height': ' ', 'weight': ' '},
        # {'unique_id': 6, 'parent_id': 5, 'short_name': 'Lily', 'height': '170', 'weight': '55'},
        # {'unique_id': 7, 'parent_id': 5, 'short_name': 'Tom', 'height': '180', 'weight': '75'},
        # {'unique_id': 8, 'parent_id': 1, 'short_name': 'Class 3', 'height': ' ', 'weight': ' '},
        # {'unique_id': 9, 'parent_id': 8, 'short_name': 'Jack', 'height': '178', 'weight': '80'},
        # {'unique_id': 10, 'parent_id': 8, 'short_name': 'Tim', 'height': '172', 'weight': '60'}
    ]

    app = QApplication(sys.argv)
    view = view(data)
    view.setGeometry(300, 100, 600, 300)
    view.setWindowTitle('QTreeview Example')
    view.show()
    sys.exit(app.exec_())