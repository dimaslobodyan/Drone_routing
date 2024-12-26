import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
from ACO_TPS_Class import *
from Input_Type import *
import numpy as np
from scipy import spatial

# # вычисление длины пути
# def cal_total_distance(routine):
#     num_points, = routine.shape
#     return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points-1)])

# вычисление длины пути
def cal_total_distance(routine,num_points):
    num_points=num_points
    s=sum([distance_matrix[routine[i], routine[i + 1]] for i in range(num_points)])
    return s

def cal_distance(i,j):
    return distance_matrix[i, j]

def main(start_time,points_coordinate, distance, distance_matrix, num_points, size_pop=40, max_iter=20, check=0, feroboost=False, NN=None, NLTWX=None, rho=0.1):
    # создание объекта алгоритма муравьиной колонии
    aca = ACO_TSP(points_coordinate, func=cal_total_distance, func_dis=cal_distance, n_dim=num_points, distance=distance,
                  size_pop=size_pop,  # количество муравьёв
                  max_iter=max_iter, distance_matrix=distance_matrix, feroboost=feroboost, NN=NN, NLTWX=NLTWX, rho=rho)
    best_x, best_y, best_len= aca.run()

    time_exec=abs(time.time() - start_time)
    print("time of execution(",check,"): %s seconds" % time_exec)  # вычисление времени выполнения

    #===================== Вывод результатов на экран ===================
    best_points_=[]
    for i in range(len(best_x)):
        if i!=0 and best_x[i]==0:
            continue
        best_points_.append(best_x[i])
    best_points_coordinate = points_coordinate[best_points_, :]
    # for index in range(num_points):
    #     plt.annotate(index, (points_coordinate[index, 0], points_coordinate[index, 1]))
    #     plt.plot(points_coordinate[index, 0], points_coordinate[index, 1], 'o-r')
    # plt.plot(best_points_coordinate[:, 0],
    #            best_points_coordinate[:, 1], 'o-r')
    # # изменение размера графиков
    # # plt.rcParams['figure.figsize'] = [20, 10]
    # # plt.annotate("flight length: %.4f km" % best_y, (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')
    # # plt.annotate("time of execution: %.4f seconds" % time_exec, (0, 0), (150, -20), xycoords='axes fraction', textcoords='offset points', va='top')
    # plt.annotate("Best:", (0, 0), (0, -20), xycoords='axes fraction',
    #              textcoords='offset points', va='top')
    # plt.annotate("flight length: %.4f km" % best_y, (0, 0), (50, -20), xycoords='axes fraction',
    #              textcoords='offset points', va='top')
    # plt.annotate("visited num: %2d" % (best_len-2), (0, 0), (200, -20), xycoords='axes fraction',
    #              textcoords='offset points', va='top')
    # plt.show()

    # Create a new figure
    fig = Figure()

    # Add a subplot to the figure
    ax = fig.add_subplot(1, 1, 1)

    # Iterate through points to plot and annotate
    for index in range(num_points):
        ax.annotate(index, (points_coordinate[index, 1], points_coordinate[index, 0]))
        ax.plot(points_coordinate[index, 1], points_coordinate[index, 0], 'o-r')

    # Plot the best points
    ax.plot(best_points_coordinate[:, 1], best_points_coordinate[:, 0], 'o-r')

    # Annotate additional information
    ax.annotate("Best:", (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')
    ax.annotate("flight length: %.4f km" % best_y, (0, 0), (50, -20), xycoords='axes fraction',
                textcoords='offset points', va='top')
    ax.annotate("visited num: %2d" % (best_len - 2), (0, 0), (200, -20), xycoords='axes fraction',
                textcoords='offset points', va='top')

    # Display the figure
    # canvas = FigureCanvas(fig)
    # canvas.print_figure("output.png")  # You can also save the figure to a file

    return best_points_coordinate, best_y, best_len, fig

def find_route(type, coordinate_targets, drones):
    if type==1:
        points_coordinate, distance, distance_matrix, num_points, speed = from_text_file()
    else:
        points_coordinate, distance, distance_matrix, num_points, speed = from_db(coordinate_targets, drones)
    start_time = time.time()  # сохранение времени начала выполнения
    x, y, length, fig = main(start_time,points_coordinate, distance, distance_matrix, num_points,30, 100)  # выполнение кода
    print("distance: ", y, " km\n", "time: ", y / speed * 60, " min\n", "target: ", length - 2, "\n", sep='')
    return x, y, length, speed, fig

if __name__ == "__main__":

    # #читання з файлу Вадима###############################################
    # with open("results-write-big.txt", "r") as file:
    #     contents = file.readlines()
    #     contents.append("----------\n")
    #     contents.pop(0)
    #     indices = [i for i, x in enumerate(contents) if x == "----------\n"]
    #     # indices.pop(-1)
    #     # indices.pop(0)
    #
    # # with open("results.txt", "r") as file:
    # #     contents_res = file.readlines()
    # #     indices_res = [i for i, x in enumerate(contents_res) if x == "----------\n"]
    # #     indices_res.pop(-1)
    # #     indices_res.pop(0)
    #
    # k=1
    #
    # time_to_fly = float(contents[3])
    # speed = 10
    # start = np.asfarray(contents[1].split(' '))
    # points_coordinate = np.array([start])
    # end = np.array([np.asfarray(contents[2].split(' '))])
    # num_points = int(np.asfarray(contents[0].split(' '))[0])
    # for i in range(num_points):
    #     points_coordinate = np.append(points_coordinate, np.array([np.asfarray(contents[4 + i].split(' '))]),
    #                                   axis=0)
    # points_coordinate = np.append(points_coordinate, end, axis=0)
    #
    # # resNN_points_coordinate = np.array([]).astype(int)
    # # targetNN = int(contents[num_points + 6]) + 2
    # # for i in range(targetNN):
    # #     s, m = np.where(np.isclose(points_coordinate, np.asfarray(contents_res[3 + i].split(' '))))
    # #     resNN_points_coordinate = np.append(resNN_points_coordinate,s[list(m).index(1)])
    #
    # # resNLTWX_points_coordinate = np.array([]).astype(int)
    # # targetNLTWX = int(contents[num_points + 9]) + 2
    # # for i in range(targetNLTWX):
    # #     s, m = np.where(np.isclose(points_coordinate, np.asfarray(contents_res[4 + targetNN + i].split(' '))))
    # #     resNLTWX_points_coordinate = np.append(resNLTWX_points_coordinate, s[list(m).index(1)])
    #
    # num_points += 2
    # distance = time_to_fly * speed
    # # print("Координаты вершин:\n", points_coordinate, "\n")
    # # вычисление матрицы расстояний между вершин
    # distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    #
    # start_time = time.time()  # сохранение времени начала выполнения
    # x, y, target = main(40, 150, i+1)  # выполнение кода
    # # start_time = time.time()  # сохранение времени начала выполнения
    # # fx, fy, ftarget = main(30, 100, i + 1, feroboost=True, NN=resNN_points_coordinate, NLTWX=resNLTWX_points_coordinate)  # выполнение кода
    # print("№: ", k," length: ", y, "target:", target, "\n")
    #
    # f = open("rez_write_big.txt", "w")
    # f.writelines("----------\n")
    # f.writelines(contents[:indices[0]])
    # f.writelines(['AntColony\n', str(y/speed*60)+'\n', str(target-2)+'\n'])
    # # f.writelines(['AntColony-feroboost\n', str(fy / speed * 60) + '\n', str(ftarget - 2) + '\n'])
    #
    # k=2
    # for index in indices:
    #     time_to_fly = float(contents[index+4])
    #     speed = 10
    #     start = np.asfarray(contents[index+2].split(' '))
    #
    #     points_coordinate = np.array([start])
    #
    #     end = np.array([np.asfarray(contents[index+3].split(' '))])
    #
    #     num_points = int(np.asfarray(contents[index+1].split(' '))[0])
    #     for i in range(num_points):
    #         points_coordinate = np.append(points_coordinate, np.array([np.asfarray(contents[index + 5 + i].split(' '))]),
    #                                       axis=0)
    #     points_coordinate = np.append(points_coordinate, end, axis=0)
    #
    #     # resNN_points_coordinate = np.array([]).astype(int)
    #     # targetNN = int(contents[index+num_points + 7]) + 2
    #     # for i in range(targetNN):
    #     #     s, m = np.where(np.isclose(points_coordinate, np.asfarray(contents_res[indices_res[k-2] + 3 + i].split(' '))))
    #     #     resNN_points_coordinate = np.append(resNN_points_coordinate, s[list(m).index(1)])
    #     #
    #     # resNLTWX_points_coordinate = np.array([]).astype(int)
    #     # targetNLTWX = int(contents[index+num_points + 10]) + 2
    #     # for i in range(targetNLTWX):
    #     #     s, m = np.where(np.isclose(points_coordinate, np.asfarray(contents_res[indices_res[k-2] + 4 + targetNN + i].split(' '))))
    #     #     resNLTWX_points_coordinate = np.append(resNLTWX_points_coordinate, s[list(m).index(1)])
    #
    #     num_points += 2
    #
    #     distance = time_to_fly * speed
    #
    #     # print("Координаты вершин:\n", points_coordinate, "\n")
    #
    #     # вычисление матрицы расстояний между вершин
    #     distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    #
    #     start_time = time.time()  # сохранение времени начала выполнения
    #     x, y, target = main(40, 150, i+1)  # выполнение кода
    #     # start_time = time.time()  # сохранение времени начала выполнения
    #     # fx, fy, ftarget = main(30, 100, i + 1, feroboost=True, NN=resNN_points_coordinate,
    #     #                        NLTWX=resNLTWX_points_coordinate)  # выполнение кода
    #     print("№: ", k,"length: ", y, "target:", target, "\n")
    #     k+=1
    #     f.writelines(contents[indices[indices.index(index)]:indices[indices.index(index)+1]])
    #     f.writelines(['AntColony\n', str(y / speed * 60) + '\n', str(target-2) + '\n'])
    #     # f.writelines(['AntColony-feroboost\n', str(fy / speed * 60) + '\n', str(ftarget - 2) + '\n'])
    # f.writelines("----------\n")
    # f.close()
    # #######################################################################
    points_coordinate, distance, distance_matrix, num_points, speed = from_text_file()
    for i in range(1):
        start_time = time.time()  # сохранение времени начала выполнения
        x,y,length,plt=main(start_time,points_coordinate, distance, distance_matrix, num_points,30,100,i)  # выполнение кода
        print("distance: ",y," km\n","time: ",y/speed*60,  " min\n", "target: ", length-2, "\n", sep='')

    # # ---------------------------------результати в залежності від ітерацій-------------------------
    # iter = [5,15,50]
    # with open("write-new.txt", "r") as file:
    #     contents = file.readlines()
    #     indices = [i for i, x in enumerate(contents) if x == "----------\n"]
    #     # indices.pop(-1)
    #
    # k = 1
    #
    # time_to_fly = float(contents[3])
    # speed = 10
    # start = np.asfarray(contents[1].split(' '))
    # points_coordinate = np.array([start])
    # end = np.array([np.asfarray(contents[2].split(' '))])
    # num_points = int(np.asfarray(contents[0].split(' '))[0])
    # for i in range(num_points):
    #     points_coordinate = np.append(points_coordinate, np.array([np.asfarray(contents[4 + i].split(' '))]),
    #                                   axis=0)
    # points_coordinate = np.append(points_coordinate, end, axis=0)
    #
    # num_points += 2
    # distance = time_to_fly * speed
    # # print("Координаты вершин:\n", points_coordinate, "\n")
    # # вычисление матрицы расстояний между вершин
    # distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    #
    # f = open("rez_iter_change.txt", "w")
    # f.writelines("----------\n")
    # for iterations in iter:
    #     start_time = time.time()  # сохранение времени начала выполнения
    #     x, y, target = main(30, iterations, k)  # выполнение кода
    #     print("№: ", k, " iter:", iterations, " length: ", y, "target:", target, "\n")
    #     f.writelines(['AC'+str(iterations)+'\n', str(y / speed * 60) + '\n', str(target - 2) + '\n'])
    #
    #
    # k = 2
    # for index in indices:
    #     time_to_fly = float(contents[index + 4])
    #     speed = 10
    #     start = np.asfarray(contents[index + 2].split(' '))
    #
    #     points_coordinate = np.array([start])
    #
    #     end = np.array([np.asfarray(contents[index + 3].split(' '))])
    #
    #     num_points = int(np.asfarray(contents[index + 1].split(' '))[0])
    #     for i in range(num_points):
    #         points_coordinate = np.append(points_coordinate,
    #                                       np.array([np.asfarray(contents[index + 5 + i].split(' '))]),
    #                                       axis=0)
    #     points_coordinate = np.append(points_coordinate, end, axis=0)
    #
    #     num_points += 2
    #
    #     distance = time_to_fly * speed
    #
    #     # print("Координаты вершин:\n", points_coordinate, "\n")
    #
    #     # вычисление матрицы расстояний между вершин
    #     distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    #
    #     f.writelines("----------\n")
    #     for iterations in iter:
    #         start_time = time.time()  # сохранение времени начала выполнения
    #         x, y, target = main(30, iterations, k)  # выполнение кода
    #         print("№: ", k, " iter:", iterations, " length: ", y, "target:", target, "\n")
    #         f.writelines(['AC' + str(iterations) + '\n', str(y / speed * 60) + '\n', str(target - 2) + '\n'])
    #
    #     # start_time = time.time()  # сохранение времени начала выполнения
    #     # x, y, target = main(30, 100, i + 1)  # выполнение кода
    #     # start_time = time.time()  # сохранение времени начала выполнения
    #     # fx, fy, ftarget = main(30, 100, i + 1)  # выполнение кода
    #     # print("№: ", k, "length: ", y, "target:", target, "\n")
    #     k += 1
    #     # f.writelines(contents[indices[indices.index(index)]:indices[indices.index(index) + 1]])
    #     # f.writelines(['AntColony\n', str(y / speed * 60) + '\n', str(target - 2) + '\n'])
    #     # f.writelines(['AntColony-feroboost\n', str(fy / speed * 60) + '\n', str(ftarget - 2) + '\n'])
    # f.writelines("----------\n")
    # f.close()
    # #---------------------------------------------------------------------------------------

    # # ---------------------------------результати в залежності від випаровування феромону-------------------------
    # rho = [0, 0.1, 0.5, 0.9]
    # with open("write-new.txt", "r") as file:
    #     contents = file.readlines()
    #     indices = [i for i, x in enumerate(contents) if x == "----------\n"]
    #     # indices.pop(-1)
    #
    # k = 1
    #
    # time_to_fly = float(contents[3])
    # speed = 10
    # start = np.asfarray(contents[1].split(' '))
    # points_coordinate = np.array([start])
    # end = np.array([np.asfarray(contents[2].split(' '))])
    # num_points = int(np.asfarray(contents[0].split(' '))[0])
    # for i in range(num_points):
    #     points_coordinate = np.append(points_coordinate, np.array([np.asfarray(contents[4 + i].split(' '))]),
    #                                   axis=0)
    # points_coordinate = np.append(points_coordinate, end, axis=0)
    #
    # num_points += 2
    # distance = time_to_fly * speed
    # # print("Координаты вершин:\n", points_coordinate, "\n")
    # # вычисление матрицы расстояний между вершин
    # distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    #
    # f = open("rez_rho_change.txt", "w")
    # f.writelines("----------\n")
    # for ro in rho:
    #     start_time = time.time()  # сохранение времени начала выполнения
    #     x, y, target = main(30, 50, k,rho=ro)  # выполнение кода
    #     print("№: ", k, " iter:", ro, " length: ", y, "target:", target, "\n")
    #     f.writelines(['AC' + str(ro) + '\n', str(y / speed * 60) + '\n', str(target - 2) + '\n'])
    #
    # k = 2
    # for index in indices:
    #     time_to_fly = float(contents[index + 4])
    #     speed = 10
    #     start = np.asfarray(contents[index + 2].split(' '))
    #
    #     points_coordinate = np.array([start])
    #
    #     end = np.array([np.asfarray(contents[index + 3].split(' '))])
    #
    #     num_points = int(np.asfarray(contents[index + 1].split(' '))[0])
    #     for i in range(num_points):
    #         points_coordinate = np.append(points_coordinate,
    #                                       np.array([np.asfarray(contents[index + 5 + i].split(' '))]),
    #                                       axis=0)
    #     points_coordinate = np.append(points_coordinate, end, axis=0)
    #
    #     num_points += 2
    #
    #     distance = time_to_fly * speed
    #
    #     # print("Координаты вершин:\n", points_coordinate, "\n")
    #
    #     # вычисление матрицы расстояний между вершин
    #     distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    #
    #     f.writelines("----------\n")
    #     for ro in rho:
    #         start_time = time.time()  # сохранение времени начала выполнения
    #         x, y, target = main(30, 50, k, rho=ro)  # выполнение кода
    #         print("№: ", k, " iter:", ro, " length: ", y, "target:", target, "\n")
    #         f.writelines(['AC' + str(ro) + '\n', str(y / speed * 60) + '\n', str(target - 2) + '\n'])
    #
    #     # start_time = time.time()  # сохранение времени начала выполнения
    #     # x, y, target = main(30, 100, i + 1)  # выполнение кода
    #     # start_time = time.time()  # сохранение времени начала выполнения
    #     # fx, fy, ftarget = main(30, 100, i + 1)  # выполнение кода
    #     # print("№: ", k, "length: ", y, "target:", target, "\n")
    #     k += 1
    #     # f.writelines(contents[indices[indices.index(index)]:indices[indices.index(index) + 1]])
    #     # f.writelines(['AntColony\n', str(y / speed * 60) + '\n', str(target - 2) + '\n'])
    #     # f.writelines(['AntColony-feroboost\n', str(fy / speed * 60) + '\n', str(ftarget - 2) + '\n'])
    # f.writelines("----------\n")
    # f.close()
    # # ---------------------------------------------------------------------------------------

    # #-------------------- залежність результату від кількості ітерацій -------------------
    # rho=[0,0.1,0.5,0.9]
    # tar=[]
    # leng=[]
    # for i in rho:
    #     start_time = time.time()  # сохранение времени начала выполнения
    #     x,y,length=main(30,100,i,rho=i)  # выполнение кода
    #     tar.append(length)
    #     leng.append(y)
    #     print("length: ",y,"target:", length, "\n")
    #
    # plt.subplot(1, 2, 1)
    # plt.title("Route length")
    # plt.plot(leng, label='Iter')
    # # plt.legend(loc="upper left")
    #
    # plt.subplot(1, 2, 2)
    # plt.title("Research targets")
    # plt.plot(tar, label='Iter')
    # # plt.legend(loc="upper left")
    # plt.show()
    # #-------------------------------------------------------------------------------------


    # #=================== визначення опт критеріїв ітерацій і мурах =====================
    # x_len=[]
    # y_len=[]
    # for i in range(1,31):
    #     start_time = time.time()  # сохранение времени начала выполнения
    #     x, y ,l= main(i,15,i) # выполнение кода
    #     x_len.append(x)
    #     y_len.append(y)
    #
    # plt.subplot(1,2,1)
    # plt.plot(x_len)
    # plt.subplot(1, 2, 2)
    # plt.plot(y_len)
    # plt.show()


