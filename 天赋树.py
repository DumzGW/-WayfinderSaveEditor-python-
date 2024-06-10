from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox,QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, QRectF
import json

class TalentTreeWindow(QMainWindow):
    def __init__(self, character_index):
        super().__init__()
        self.character_index = character_index
        self.initUI()

    def initUI(self):
        self.setWindowTitle('天赋树修改')
        self.setGeometry(100, 100, 1000, 1000)
        self.graphWidget = GraphWidget(parent=self)
        self.setCentralWidget(self.graphWidget)

        self.reset_button = QPushButton('重置', self)
        self.reset_button.clicked.connect(self.reset_talents)
        self.reset_button.setGeometry(10, 10, 100, 30)

        
        self.load_data()

    def load_data(self):
        # Load bin data and find character's talents
        from 角色修改 import load_bin_file, get_CharName, load_config,path0,trans_text,load_translation_file,resource_path
        self.bin_data = load_bin_file(path0(load_config()['output_path_1']))
        self.translation_data = load_translation_file(resource_path(load_config()["trans_path"]))
        self.character_name = trans_text(self.translation_data, get_CharName(self.bin_data, self.character_index), 'Ename')
        self.unlocked_nodes = self.find_talents()

    def find_talents(self):
        archetype_tree_data = self.bin_data['playerData']['m_ArchetypeTreeData']['m_UnlockedTreeData']
        for data in archetype_tree_data:
            if data['characterName'] == self.character_name:
                return data['unlockedNodes']
        return []

    def reset_talents(self):
        # Reset talents logic
        archetype_tree_data = self.bin_data['playerData']['m_ArchetypeTreeData']['m_UnlockedTreeData']
        for data in archetype_tree_data:
            if data['characterName'] == self.character_name:
                data['unlockedNodes'] = []
                self.save_data()
                QMessageBox.information(self, '提示', '天赋已重置！')
                return

    def save_data(self):
        from 角色修改 import load_config,path0
        with open(path0(load_config()['output_path_1']), 'w', encoding='utf-8') as bin_file:
            json.dump(self.bin_data, bin_file, ensure_ascii=False, indent=2)

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout) 
        self.show_message = True   
        # 定义节点位置和连接线
        self.nodes = {
            1: QPointF(700, 600),
            2: QPointF(710, 480),
            3: QPointF(714, 367),
            4: QPointF(720, 250),
            5: QPointF(729, 143),
            6: QPointF(741, 28),
            7: QPointF(631, 53),
            8: QPointF(559, 126),
            9: QPointF(569, 208),
            10: QPointF(486, 177),
            25: QPointF(397, 155),
            24: QPointF(253, 193),
            23: QPointF(147, 276),
            22: QPointF(124, 412),
            21: QPointF(163, 550),
            20: QPointF(225, 621),
            18: QPointF(300, 678),
            19: QPointF(223, 710),
            11: QPointF(591, 325),
            12: QPointF(610, 427),
            13: QPointF(501, 490),
            14: QPointF(508, 308),
            15: QPointF(433, 338),
            17: QPointF(413, 637),
            16: QPointF(350, 581),
            33: QPointF(345, 500),
            34: QPointF(367, 400),
            35: QPointF(312, 373),
            36: QPointF(235, 332),
            31: QPointF(610, 664),
            30: QPointF(510, 725),
            32: QPointF(507, 605),
            26: QPointF(190, 807),
            27: QPointF(225, 918),
            28: QPointF(321, 854),
            29: QPointF(410, 790),
            111: QPointF(800, 250),
            37: QPointF(900.0, 600.0),
            110: QPointF(1150, 861.0),
            38: QPointF(998.9230484541326, 668.6602540378443),
            39: QPointF(1094.7839190817742, 728.6243556529821),
            40: QPointF(1193.1088913245535, 792.3205080756886),
            41: QPointF(1281.2736095294886, 853.6147367097486),
            42: QPointF(1374.866530964699, 921.5070415551619),
            43: QPointF(1408.215895870088, 813.7442471388736),
            44: QPointF(1380.9960413938238, 714.890418066394),
            46: QPointF(1304.9819582834998, 682.5506721042384),
            45: QPointF(1373.3287458008176, 626.1705635901301),
            66: QPointF(1436.881304684075, 560.094302653315),
            67: QPointF(1475.9723393402664, 416.38664450835586),
            68: QPointF(1457.092230826158, 283.0879517072053),
            69: QPointF(1350.8127759114743, 195.16936742016327),
            70: QPointF(1211.801270189222, 159.94435816775643),
            56: QPointF(1119.3134665205266, 178.1379332023916),
            58: QPointF(1032.4500185048137, 214.5898384862245),
            57: QPointF(1043.2372055837116, 131.90588239482275),
            47: QPointF(1192.6569860407208, 643.1032309874961),
            48: QPointF(1094.822394854708, 608.5577136594005),
            49: QPointF(1094.7627944162882, 482.66094464689667),
            51: QPointF(1248.879417905056, 579.7231224733878),
            52: QPointF(1260.3986557915227, 499.7712171895548),
            50: QPointF(1011.4570600599757, 332.9507091138661),
            55: QPointF(1091.4544826719043, 306.39110867544645),
            54: QPointF(1164.1025403784438, 342.56098165652423),
            53: QPointF(1239.7050807568876, 411.61354053978187),
            71: QPointF(1290.5877666590675, 377.4821433316377),
            72: QPointF(1364.5948082142295, 331.29818724023596),
            64: QPointF(889.5743741577959, 490.0577136594005),
            63: QPointF(886.7468245269451, 372.95517328095667),
            65: QPointF(992.1698729810778, 430.35709706960336),
            59: QPointF(975.7327414166211, 54.82704406993628),
            60: QPointF(862.1039215965484, 29.63793320239165),
            61: QPointF(869.5295474387525, 144.77637196569776),
            62: QPointF(880.4551732809566, 253.85263290251282),
            73: QPointF(800.0, 775.0),
            74: QPointF(691.0769515458674, 826.3397459621557),
            75: QPointF(591.2160809182258, 879.3756443470179),
            76: QPointF(486.8911086754465, 932.6794919243114),
            77: QPointF(389.7263904705116, 978.3852632902515),
            78: QPointF(284.1334690353011, 1025.4929584448382),
            79: QPointF(360.7841041299122, 1108.2557528611264),
            80: QPointF(460.00395860617624, 1134.109581933606),
            82: QPointF(526.0180417165002, 1084.4493278957616),
            81: QPointF(540.6712541991826, 1171.8294364098701),
            89: QPointF(566.118695315925, 1259.905697346685),
            90: QPointF(671.0276606597338, 1365.6133554916441),
            91: QPointF(795.9077691738421, 1415.9120482927947),
            92: QPointF(925.1872240885258, 1367.8306325798367),
            93: QPointF(1025.1987298107783, 1265.0556418322435),
            94: QPointF(1055.6865334794734, 1175.8620667976083),
            95: QPointF(1067.5499814951863, 1082.4101615137754),
            96: QPointF(1133.7627944162884, 1133.094117605177),
            83: QPointF(616.3430139592795, 1006.8967690125039),
            106: QPointF(695.1776051452922, 939.4422863405996),
            98: QPointF(804.2372055837119, 1002.3390553531033),
            84: QPointF(643.120582094944, 1087.2768775266122),
            85: QPointF(706.6013442084773, 1137.2287828104452),
            97: QPointF(975.5429399400243, 1005.0492908861338),
            88: QPointF(958.5455173280958, 1087.6088913245535),
            87: QPointF(890.8974596215563, 1132.4390183434757),
            86: QPointF(793.2949192431124, 1163.3864594602182),
            107: QPointF(797.4122333409326, 1224.5178566683621),
            108: QPointF(800.4051917857707, 1311.701812759764),
            104: QPointF(900.4256258422041, 820.9422863405995),
            103: QPointF(1003.2531754730549, 877.0448267190433),
            105: QPointF(900.8301270189223, 939.6429029303966),
            99: QPointF(1234.2672585833789, 1113.1729559300634),
            100: QPointF(1312.8960784034516, 1027.3620667976081),
            101: QPointF(1209.4704525612476, 976.223628034302),
            102: QPointF(1109.5448267190434, 931.1473670974871),
            109: QPointF(446.89110867544645, 863.3974596215563),
            # 根据实际情况添加更多节点
        }
        
        
        
        
        
        
        self.edges = [
            (1, 2), (2, 3),(3, 4), (4, 5),(5, 6), (6, 7),(7, 8), (8, 9),
            (9, 10), (8, 10),(10, 25), (25, 24),(24,23), (23, 22),(22, 21), (21, 20),
            (20, 18), (20, 19),(19,18),(9,11),(11,13),(3,12),(12,13),(13,17),(17,18),
            (11,14),(14,15),(15,34),(34,33),(33,16),(30,32),(32,13),
            (16,17),(34,35),(35,36),(19,26),(26,27),(27,28),(28,29),(29,30),(30,31),(31,1),
            (4,111),(111,62),(62,61),(61,60),(60,59),(59,57),(57,56),(56,58),(58,57),(62,63),(63,64),(64,37),(37,38),(38,39),
            (39,40),(40,41),(41,42),(42,43),(43,44),(44,46),(46,45),(45,44),(39,48),(48,49),(49,65),
            (65,63),(46,47),(47,49),(49,50),(50,58),(47,51),(51,52),(52,53),(53,54),(54,55),(55,50),
            (53,71),(71,72),(56,70),(70,69),(69,68),(68,67),(67,66),(66,45),(40,110),(110,102),(29,109),(109,76),
            (73,74),(74,75),(75,76),(76,77),(77,78),(78,79),(79,80),(80,82),(82,81),(81,80),(73,104),
            (104,103),(103,102),(102,101),(101,100),(100,99),(99,96),(96,94),(94,95),(95,96),
            (94,93),(93,92),(92,91),(91,90),(90,89),(89,81),(82,83),(83,98),(98,97),(97,95),
            (75,106),(106,98),(98,105),(105,103),(83,84),(84,85),(85,86),(86,87),(87,88),(88,97),(86,107),(107,108)

            # 根据实际情况添加更多连接线
        ]
    def find_talents(self, character_index):
        from 角色修改 import load_bin_file, get_CharName, load_config,path0,trans_text,load_translation_file,resource_path
        bin_data = load_bin_file(path0(load_config()['output_path_1']))
        translation_data = load_translation_file(resource_path(load_config()["trans_path"]))
        character_name = trans_text(translation_data, get_CharName(bin_data, character_index), 'Ename')
        archetype_tree_data = bin_data['playerData']['m_ArchetypeTreeData']['m_UnlockedTreeData']
        for data in archetype_tree_data:
            if data['characterName'] == character_name:
                return data['unlockedNodes']
        return []
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 画所有节点和连接线
        pen = QPen(QColor(200, 200, 200), 2)
        painter.setPen(pen)
        for edge in self.edges:
            start_node = self.nodes[edge[0]]
            end_node = self.nodes[edge[1]]
            s1=QPointF(start_node.x()*0.66, start_node.y()*0.66)
            s2=QPointF(end_node.x()*0.66, end_node.y()*0.66)
            painter.drawLine(s1, s2)

        unlocked_nodes=self.find_talents(self.parent().character_index)
        # 画所有节点
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        
        for node, position in self.nodes.items():
            if any(self.node_key(self.getw_node(node))== self.node_key(unlocked_node) for unlocked_node in unlocked_nodes):
                painter.setBrush(QColor(0, 255, 0))  # 已解锁节点用绿色填充
            else:
                painter.setBrush(QColor(255, 255, 255))  # 未解锁节点用白色填充
            painter.drawEllipse(position*0.66, 10, 10)  # 画节点
    def getindex(self,node):
        if node ==109:
            index=31
        elif node==110:
            index=1
        elif node==111:
            index=28
        elif node in range(1,37):
            index=node+1
        elif node in range(37,73):
            if node<=66:
                index=node-36
            else:
                index=node-35
        else:
            if node<=99:
                index=node-72
            else:
                index=node-71
        return index
    def node_key(self,node):
        return (node["nodeId"],node["treeIndex"])
    def getw_node(self,node):
        w_node={
            "nodeId": str(node),
            "bIsNetworked": "False",
            "bIsNetworkUnlocked": "False",
            "treeType": "Support",
            "treeIndex": str(self.getindex(node))       
        }
        return w_node
    def mousePressEvent(self, event):
        for node, position in self.nodes.items():
            if QRectF(position.x()*0.66 - 10, position.y()*0.66 - 10, 20, 20).contains(event.pos()):
                self.node_clicked(node)
                break

    def node_clicked(self, node):
        if node in range(1,37):
            treeType="Offensive"
        elif node in range(37,73):
            treeType="Support"
        elif node in range(73,109):
            treeType="Defensive"
        elif node == 110:
            treeType="Offensive"
        elif node == 111:
            treeType="Defensive"
        elif node == 109:
            treeType="Support"
        new_node={
            "nodeId": str(node),
            "bIsNetworked": "False",
            "bIsNetworkUnlocked": "False",
            "treeType": treeType,
            "treeIndex": str(self.getindex(node))       
        }
        from 角色修改 import load_bin_file, load_config,path0
        self.bin_data = load_bin_file(path0(load_config()['output_path_1']))
        archetype_tree_data = self.bin_data['playerData']['m_ArchetypeTreeData']['m_UnlockedTreeData']
        for data in archetype_tree_data:
            if data['characterName'] == self.parent().character_name:
                data['unlockedNodes'].append(new_node)
                self.save_data()
                from PyQt5.QtWidgets import QCheckBox
                if self.show_message:
                    msg = QMessageBox()
                    msg.setWindowTitle('提示')
                    msg.setText('天赋已保存，请勿点击上一个界面中的保存\n以免修改丢失')
                    checkbox = QCheckBox("不再提醒")
                    checkbox.stateChanged.connect(lambda state: self.update_show_message_state(state))
                    msg.setCheckBox(checkbox)
                    msg.exec_()
                self.update()
                return
    def update_show_message_state(self, state):
        if state == Qt.Checked:
            self.show_message = False
    def save_data(self):
        from 角色修改 import load_config,path0
        with open(path0(load_config()['output_path_1']), 'w', encoding='utf-8') as bin_file:
            json.dump(self.bin_data, bin_file, ensure_ascii=False, indent=2)