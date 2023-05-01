import pygame
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from queue import PriorityQueue

from const import *
from map import Map


class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        loadUi('src/nguyendudesign.ui', self)
        self.setWindowTitle('Nguyen Du District Map')
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.startPoint = self.comboBox.currentIndex()
        self.endPoint = self.comboBox_2.currentIndex()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Nguyen Du Distrct Map')
        self.map = Map()
        self.mainloop()

    # set the default drawing color
    draw_color = BLACK

    # set the default drawing size
    draw_size = 5

    path = []

    startPoint = 0
    endPoint = 0

    des_points = [
        (240, 203), (218, 206), (173, 100), (256, 130),
        (508, 199), (608, 220), (824, 267), (932, 459),
        (844, 564), (755, 564), (772, 658), (737, 628),
        (835, 468), (646, 456), (116, 444), (223, 437),
        (938, 322), (391, 279), (402, 384), (112, 316),
        (112, 390)
    ]
    turn_points = [
        (0, 0), (127, 87), (246, 126), (125, 161), (224, 200),
        (127, 216), (213, 227), (124, 277), (200, 276), (124, 344),
        (122, 409), (123, 427), (352, 422), (366, 348), (390, 276),
        (404, 228), (419, 179), (737, 251), (767, 254), (754, 283),
        (699, 458), (847, 467), (932, 475), (854, 349), (745, 321),
        (935, 293), (782, 467), (727, 649), (842, 661), (927, 665),
        (357, 406), (228, 172), (425, 453), (426, 441), (442, 441)
    ]

    def heuristic(self, point1, point2):
        return (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2

    def costBetween(point1, point2):
        return (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2

    graph = {
        des_points[0]: {turn_points[1]: costBetween(des_points[0], turn_points[1]),
                        turn_points[15]: costBetween(des_points[0], turn_points[15]), },
        des_points[1]: {turn_points[4]: costBetween(des_points[1], turn_points[4]),
                        turn_points[6]: costBetween(des_points[1], turn_points[6])},
        des_points[2]: {turn_points[1]: costBetween(des_points[2], turn_points[1]),
                        turn_points[2]: costBetween(des_points[2], turn_points[2])},
        des_points[3]: {turn_points[2]: costBetween(des_points[3], turn_points[2]),
                        turn_points[16]: costBetween(des_points[3], turn_points[16])},
        des_points[4]: {des_points[5]: costBetween(des_points[4], des_points[5]),
                        turn_points[16]: costBetween(des_points[4], turn_points[16])},
        des_points[5]: {des_points[4]: costBetween(des_points[5], des_points[4]),
                        turn_points[17]: costBetween(des_points[5], turn_points[17])},
        des_points[6]: {turn_points[18]: costBetween(des_points[6], turn_points[18]),
                        turn_points[25]: costBetween(des_points[6], turn_points[25])},
        des_points[7]: {des_points[16]: costBetween(des_points[7], des_points[16]),
                        turn_points[22]: costBetween(des_points[7], turn_points[22])},
        des_points[8]: {turn_points[21]: costBetween(des_points[8], turn_points[21]),
                        turn_points[28]: costBetween(des_points[8], turn_points[28])},
        des_points[9]: {turn_points[26]: costBetween(des_points[9], turn_points[26]),
                        des_points[11]: costBetween(des_points[9], des_points[11])},
        des_points[10]: {turn_points[27]: costBetween(des_points[10], turn_points[27]),
                         turn_points[28]: costBetween(des_points[10], turn_points[28])},
        des_points[11]: {turn_points[27]: costBetween(des_points[11], turn_points[27]),
                         des_points[9]: costBetween(des_points[11], des_points[9])},
        des_points[12]: {turn_points[21]: costBetween(des_points[12], turn_points[21]),
                         turn_points[26]: costBetween(des_points[12], turn_points[26])},
        des_points[13]: {turn_points[12]: costBetween(des_points[13], turn_points[12]),
                         turn_points[20]: costBetween(des_points[13], turn_points[20])},
        des_points[14]: {turn_points[11]: costBetween(des_points[14], turn_points[11])},
        des_points[15]: {turn_points[32]: costBetween(des_points[15], turn_points[32])},
        des_points[16]: {turn_points[25]: costBetween(des_points[16], turn_points[25]),
                         des_points[7]: costBetween(des_points[16], des_points[7])},
        des_points[17]: {turn_points[14]: costBetween(des_points[17], turn_points[1]),
                         turn_points[15]: costBetween(des_points[17], turn_points[15])},
        des_points[18]: {turn_points[30]: costBetween(des_points[18], turn_points[30])},
        des_points[19]: {turn_points[7]: costBetween(des_points[19], turn_points[7])},
        des_points[20]: {turn_points[9]: costBetween(des_points[20], turn_points[9])},
        turn_points[1]: {des_points[2]: costBetween(turn_points[1], des_points[2]),
                         turn_points[3]: costBetween(turn_points[1], turn_points[3])},
        turn_points[2]: {turn_points[31]: costBetween(turn_points[2], turn_points[31]),
                         des_points[2]: costBetween(turn_points[2], des_points[2]),
                         des_points[3]: costBetween(turn_points[2], des_points[3])},
        turn_points[3]: {turn_points[5]: costBetween(turn_points[3], turn_points[5]),
                         turn_points[31]: costBetween(turn_points[3], turn_points[31])},
        turn_points[4]: {turn_points[31]: costBetween(turn_points[4], turn_points[31]),
                         des_points[0]: costBetween(turn_points[4], des_points[0])},
        turn_points[5]: {turn_points[6]: costBetween(turn_points[5], turn_points[6]),
                         turn_points[7]: costBetween(turn_points[5], turn_points[7])},
        turn_points[6]: {turn_points[5]: costBetween(turn_points[6], turn_points[5]),
                         des_points[1]: costBetween(turn_points[6], des_points[1])},
        turn_points[7]: {des_points[19]: costBetween(turn_points[7], des_points[19]),
                         turn_points[8]: costBetween(turn_points[7], turn_points[8])},
        turn_points[8]: {turn_points[7]: costBetween(turn_points[8], turn_points[7]),
                         turn_points[6]: costBetween(turn_points[8], turn_points[6]),
                         turn_points[14]: costBetween(turn_points[8], turn_points[14])},
        turn_points[9]: {des_points[20]: costBetween(turn_points[9], des_points[20]),
                         turn_points[13]: costBetween(turn_points[9], turn_points[13])},
        turn_points[10]: {turn_points[11]: costBetween(turn_points[10], turn_points[11])},
        turn_points[11]: {des_points[15]: costBetween(turn_points[11], des_points[15]),
                          des_points[14]: costBetween(turn_points[11], des_points[14])},
        turn_points[12]: {turn_points[33]: costBetween(turn_points[12], turn_points[33]),
                          turn_points[30]: costBetween(turn_points[12], turn_points[30]),
                          turn_points[10]: costBetween(turn_points[12], turn_points[10])},
        turn_points[13]: {turn_points[30]: costBetween(turn_points[13], turn_points[30]),
                          turn_points[14]: costBetween(turn_points[13], turn_points[14])},
        turn_points[14]: {turn_points[13]: costBetween(turn_points[14], turn_points[13]),
                          turn_points[15]: costBetween(turn_points[14], turn_points[15])},
        turn_points[15]: {turn_points[14]: costBetween(turn_points[15], turn_points[14]),
                          des_points[0]: costBetween(turn_points[15], des_points[0]),
                          turn_points[16]: costBetween(turn_points[15], turn_points[16])},
        turn_points[16]: {turn_points[15]: costBetween(turn_points[16], turn_points[15]),
                          des_points[4]: costBetween(turn_points[16], des_points[4]),
                          des_points[3]: costBetween(turn_points[16], des_points[3])},
        turn_points[17]: {des_points[5]: costBetween(turn_points[17], des_points[5]),
                          turn_points[18]: costBetween(turn_points[17], turn_points[18])},
        turn_points[18]: {turn_points[19]: costBetween(turn_points[18], turn_points[19]),
                          turn_points[17]: costBetween(turn_points[18], turn_points[17]),
                          des_points[6]: costBetween(turn_points[18], des_points[6])},
        turn_points[19]: {turn_points[17]: costBetween(turn_points[19], turn_points[17]),
                          turn_points[24]: costBetween(turn_points[19], turn_points[24])},
        turn_points[20]: {turn_points[24]: costBetween(turn_points[20], turn_points[24]),
                          turn_points[26]: costBetween(turn_points[20], turn_points[26]),
                          des_points[13]: costBetween(turn_points[20], des_points[13])},
        turn_points[21]: {turn_points[23]: costBetween(turn_points[21], turn_points[23]),
                          des_points[12]: costBetween(turn_points[21], des_points[12]),
                          turn_points[28]: costBetween(turn_points[21], turn_points[28]),
                          turn_points[22]: costBetween(turn_points[21], turn_points[22])},
        turn_points[22]: {turn_points[21]: costBetween(turn_points[22], turn_points[21]),
                          turn_points[29]: costBetween(turn_points[22], turn_points[29]),
                          des_points[7]: costBetween(turn_points[22], des_points[7])},
        turn_points[23]: {turn_points[21]: costBetween(turn_points[23], turn_points[21]),
                          turn_points[24]: costBetween(turn_points[23], turn_points[24]),
                          turn_points[25]: costBetween(turn_points[23], turn_points[25])},
        turn_points[24]: {turn_points[19]: costBetween(turn_points[24], turn_points[19]),
                          turn_points[20]: costBetween(turn_points[24], turn_points[20]),
                          turn_points[23]: costBetween(turn_points[24], turn_points[23])},
        turn_points[25]: {des_points[6]: costBetween(turn_points[25], des_points[6]),
                          turn_points[23]: costBetween(turn_points[25], turn_points[23]),
                          des_points[16]: costBetween(turn_points[25], des_points[16])},
        turn_points[26]: {turn_points[20]: costBetween(turn_points[26], turn_points[20]),
                          des_points[12]: costBetween(turn_points[26], des_points[12]),
                          des_points[9]: costBetween(turn_points[26], des_points[9])},
        turn_points[27]: {des_points[10]: costBetween(turn_points[27], des_points[10]),
                          des_points[11]: costBetween(turn_points[27], des_points[11])},
        turn_points[28]: {des_points[11]: costBetween(turn_points[28], des_points[11]),
                          turn_points[29]: costBetween(turn_points[28], turn_points[29])},
        turn_points[29]: {turn_points[22]: costBetween(turn_points[29], turn_points[22]),
                          turn_points[28]: costBetween(turn_points[29], turn_points[28])},
        turn_points[30]: {turn_points[12]: costBetween(turn_points[30], turn_points[12]),
                          des_points[18]: costBetween(turn_points[30], des_points[18])},
        turn_points[31]: {turn_points[2]: costBetween(turn_points[31], turn_points[2]),
                          turn_points[3]: costBetween(turn_points[31], turn_points[3])},
        turn_points[32]: {turn_points[33]: costBetween(turn_points[32], turn_points[33]),
                          turn_points[34]: costBetween(turn_points[32], turn_points[34])},
        turn_points[33]: {turn_points[12]: costBetween(turn_points[33], turn_points[12]),
                          turn_points[34]: costBetween(turn_points[33], turn_points[34]),
                          turn_points[32]: costBetween(turn_points[33], turn_points[32])},
        turn_points[34]: {des_points[13]: costBetween(turn_points[34], des_points[13]),
                          turn_points[33]: costBetween(turn_points[34], turn_points[33])},
    }

    # def find_shortest(self, start_point, end_point):
    #     if start_point[0] == end_point[0] and start_point[1] == end_point[1]:
    #         return
    #     else:
    #         min_num = float('inf')
    #         get_point = (0, 0)
    #         for arround_point in self.graph.get(start_point):
    #             if self.heuristic(start_point, arround_point) < min_num and arround_point not in self.path:
    #                 min_num = self.heuristic(start_point, arround_point)
    #                 get_point = arround_point
    #         if get_point[0] != 0 or get_point[1] != 0:
    #             self.path.append(get_point)
    #             self.find_shortest(get_point, end_point)
    #         else:
    #             print("Could not find")
    #             return

    def shortest_path(self, graph, start, goal):
        open_list = PriorityQueue()
        open_list.put((0, start))
        came_from = {}
        g_score = {node: float('inf') for node in graph}
        g_score[start] = 0
        f_score = {node: float('inf') for node in graph}
        f_score[start] = self.heuristic(start, goal)

        while not open_list.empty():
            _, current_node = open_list.get()
            print(current_node)

            if current_node == goal:
                # Reached the goal, construct the path
                path = [current_node]
                while current_node in came_from:
                    current_node = came_from[current_node]
                    path.append(current_node)
                path.reverse()
                return path

            for neighbor in graph[current_node]:
                tentative_g_score = g_score[current_node] + \
                    graph[current_node][neighbor]
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + \
                        self.heuristic(neighbor, goal)
                    open_list.put((f_score[neighbor], neighbor))

        return None  # No path found

    # define a function to draw the points
    def draw_points(self):
        for point in self.points:
            pygame.draw.circle(self.screen, self.draw_color,
                               point, self.draw_size)

    # define variables to store the start and end points of the line
    start_pos = None
    end_pos = None

    # define a function to draw the line
    def draw_line(self):
        if self.start_pos is not None and self.end_pos is not None:
            pygame.draw.line(self.screen, self.draw_color,
                             self.start_pos, self.end_pos, self.draw_size)

    def draw_lines(self):
        for line in self.lines:
            if line[0] is not None and line[1] is not None:
                pygame.draw.line(self.screen, self.draw_color,
                                 line[0], line[1], self.draw_size)

    # def test_result(self):
    #     # sys.setrecursionlimit(10000000)
    #     # print(self.graph.get(self.des_points[2]))
    #     # self.path.append(self.des_points[2])
    #     shortest_path = self.shortest_path(
    #         self.graph, self.des_points[2], self.des_points[18])
    #     if shortest_path:
    #         print("Shortest path:", shortest_path)
    #     else:
    #         print("No path found.")

    def mainloop(self):
        shortest_path = self.shortest_path(
            self.graph, self.des_points[self.startPoint], self.des_points[self.endPoint])
        if shortest_path:
            print("Shortest path:", shortest_path)
        else:
            print("No path found.")
        while True:
            self.map.show_bg(self.screen)
            # for des_point in self.des_points:
            #     pygame.draw.circle(self.screen, self.draw_color,
            #                        des_point, self.draw_size)
            pygame.draw.circle(self.screen, BLACK,
                               self.des_points[self.startPoint], self.draw_size)
            pygame.draw.circle(self.screen, RED,
                               self.des_points[self.endPoint], self.draw_size)
            # for turn_point in self.turn_points:
            #     pygame.draw.circle(self.screen, RED,
            #                        turn_point, self.draw_size)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     # add the clicked point to the list
                #     self.points.append(event.pos)
                #     self.start_pos = event.pos
                #     self.end_pos = None
                #     print(self.points)
                # elif event.type == pygame.MOUSEMOTION:
                #     # update the end point of the line
                #     if self.start_pos is not None:
                #         self.end_pos = event.pos
                # elif event.type == pygame.MOUSEBUTTONUP:
                #     # draw the final line and reset the start and end points
                #     if self.start_pos is not None and self.end_pos is not None:
                #         self.draw_line()
                #         self.points.append(event.pos)
                #         self.lines.append([self.start_pos, self.end_pos])
                #         self.start_pos = None
                #         self.end_pos = None
                #         print(self.lines)
            # self.draw_points()
            # self.draw_lines()
            # self.draw_line()
            if shortest_path is not None:
                for x in range(len(shortest_path) - 1):
                    pygame.draw.line(self.screen, BLUE,
                                     shortest_path[x], shortest_path[x + 1], self.draw_size + 1)
            pygame.display.flip()


app = QApplication(sys.argv)
main = Main()
main.show()
# main.mainloop()
# main.test_result()
sys.exit(app.exec_())
