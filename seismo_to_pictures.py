import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import os

#Параметры эксперимента
source_pos =         24     # Количество положений источника возмущений
time_steps =      10000     # Количество шагов по времени, 1 шаг - 10e-5 с
y_size     =        100     # Размер области пород по оси y, м
z_size     =        235     # Размер области пород по оси z, м
z_anomaly  =        150     # Z-координата границы породы и аномалии, м
velocity   =       4000     # Скорость волны в породе, м/с
z_receiver =         30     # Z-координата приемника, м
y_receiver =         42     # Y-координата приемника, м
y_source   = y_receiver     # Y-координата источника возмущений, м
source_dt  =    0.00734     # Задержка по времени источника, с
#Расстояния от приемника до источника в эксперименте, м
dists      = [20 + 2*i for i in range(source_pos)]
#Координаты источников в эксперименте, м
z_source   = [z_receiver + d for d in dists]

path       = "results/seismogramms/"
img_path   = "images/"

def read_seismogramm(seismo, anomaly):
    """
    Получает из сейсмортасс, сохраненых в txt сейсмограмму
    seismo - numpy массив, сейсмограмма
    anomaly - флаг, показывающий наличие геологической особенности
    """
    for iz, z in enumerate(z_source):
        if anomaly:
            file = os.path.join(path, f'seismogramm2_{z}.txt')
        else:
            file = os.path.join(path, f'without_{z}.txt')
        with open(file, 'r') as seism_file:
            it = 0
            line = seism_file.readline()
            while line:
                seismo[iz][it] = float(line.split()[1])
                line = seism_file.readline()
                it += 1

def norm_seismo(seismo, time_threshold):
    """
    Нормирует сейсмограмму на среднеквадратичную амплитуду
    для каждого момента врремени
    seismo - numpy массив, сейсмограмма
    """
    for it in range(time_steps):
        g_t = 0    # Коэффициент нормировки для фиксированного момента времени t
        for iz in range(source_pos):
            g_t += seismo[iz][it]**2
        g_t = g_t / source_pos
        g_t = g_t ** 0.5
        for iz in range(source_pos):
            if g_t == 0 or it < time_threshold:
                seismo[iz][it] = 0
            else:
                seismo[iz][it] /= g_t

def get_reflect_time(time_reflect, seismo_diffrnc):
    """
    Получает массив моментов времени регистрации
    первых пиков отраженной волны на сейсмограмме
    time_reflect - numpy массив, содержит время регистрации отраженных волн
    seismo_diffrnc - разность сейсмограмм, содержит картину отраженных волн
    """
    threshold = 1e-23
    for iz in range(source_pos):
        for it in range(time_steps):
            if np.abs(seismo_diffrnc[iz][it]) > threshold:
                time_reflect[iz] = it
                break

def t_r(x, y, z, v_refl):    # Вспомогательная функция для суммирования по сейсмограмме
    x_r = z_receiver
    y_r = y_receiver
    t = 0
    t += np.sqrt((x - z)**2 + (y - y_r)**2)
    t += np.sqrt((x - x_r)**2 + (y - y_r)**2)
    t /= v_refl
    t = int(round((t + source_dt) * 1e5))
    return min(t, time_steps - 1)


if __name__ == '__main__':
    seismo_anomaly = np.zeros((source_pos, time_steps))    # Сейсмограмма эксперимента с геологической особенностью
    seismo_without = np.zeros((source_pos, time_steps))    # Сейсмограмма эксперимента без особенности
    seismo_diffrnc = np.zeros((source_pos, time_steps))    # Разность сейсмограмм, содержит картину только отраженных от границы раздела сред волн

    read_seismogramm(seismo_anomaly, True)
    read_seismogramm(seismo_without, False)
    seismo_diffrnc = seismo_anomaly - seismo_without
    norm_seismo(seismo_anomaly, 1930)
    norm_seismo(seismo_without, 1930)
    norm_seismo(seismo_diffrnc, 5270)

    time_reflect = np.zeros(source_pos)    # Момент времени регистрации отраженной волны
                                           # на сейсмограмме для каждого положения источника

    get_reflect_time(time_reflect, seismo_diffrnc)

    # Среднее значение скорости отраженной волны, м
    v_refl = ((z_anomaly - z_receiver) / (time_reflect * 1e-5 - source_dt - (z_anomaly - np.array(z_source)) / velocity)).mean()

    # Итоговое изображение
    geol_image = np.zeros((z_size, y_size))

    for x in range(z_size):
        for y in range(y_size):
            #(x, y) - координаты пикселя на изображении
            s = 0
            for iz, z in enumerate(z_source):
                it = t_r(x, y, z, v_refl)
                s += seismo_diffrnc[iz][it]
            geol_image[x][y] = s

    # Выделение туннеля на итоговом изображении 
    for x in range(z_size):
        for y in range(y_size):
            if x <= 100 and (y == 44 or y == 56) or x == 100 and 44 < y < 56:
                geol_image[x][y] = -30

    plt.imshow(cv.resize(seismo_anomaly.T, (576, 1000)), cmap='gray')
    plt.savefig(os.path.join(img_path, 'anomaly_img.jpg'))

    plt.imshow(cv.resize(seismo_without.T, (576, 1000)), cmap='gray')
    plt.savefig(os.path.join(img_path, 'without_img.jpg'))

    plt.imshow(cv.resize(geol_image.T, (z_size, y_size)), cmap='gray')
    plt.axvline(x=150,color='red', linestyle='dashed', alpha=0.7)
    plt.axvline(x=160,color='red', linestyle='dashed', alpha=0.7)
    plt.savefig(os.path.join(img_path,'imagesfinal_img.jpg'))
