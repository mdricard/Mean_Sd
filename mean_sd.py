import numpy as np
import matplotlib.pyplot as plt
import math
from BiomechTools import max_min
import os.path              # needed to check if file exists


def plot_heart_rate(x, hr, min_pt=0, max_pt=0):
    """
    plots point number vs heart rate
    :param x: point number
    :param hr: heart rate
    :return:
    """
    plt.scatter(x, hr)
    plt.scatter(min_pt, hr[min_pt], color='red')
    plt.scatter(max_pt, hr[max_pt], color='red')
    plt.hlines(y=heart_rate_mean, xmin=0, xmax=len(hr), color='red')
    plt.vlines(x=min_pt, ymin=0, ymax=hr[min_pt], color='blue')
    plt.vlines(x=max_pt, ymin=0, ymax=hr[max_pt], color='blue')
    plt.xlabel('pt number')
    plt.ylabel('Heart Rate (bpm)')
    plt.grid(True)
    plt.legend(['Heart Rate'])
    plt.show()

def save_stats_long(stat_file_path, hr):
    fn = stat_file_path + 'Heart Rate Stats.csv'
    if not os.path.isfile(fn):                      # if the file does not exist, write the header
        open(fn, 'w').write('pt,hr\n')
    with open(fn, 'a') as stat_file:
        for i in range(len(hr)):
            stat_file.write(
                str(i) + ',' + str(hr[i]) + '\n')
    stat_file.close()

def find_endpoints(x, hr, threshold):
    """
    finds the first hr >= threshold and
    the last hr >= threshold and
    first_pt is first point >= threshold
    last_pt is last point >= threshold
    :param x: point number
    :param hr: heart rate
    :return: first_pt, last_pt
    """
    max, min, max_pt, min_pt = max_min(curve=hr, first_pt=0, last_pt=len(hr))
    if threshold >= min and threshold <= max:   # check if threshold is within the range of hr
        i = 0
        while hr[i] <= threshold and i < len(x) - 1:
            i += 1  # i = i +` 1
        first_pt = i

        i = first_pt + 1
        while hr[i] >= threshold and i < len(x) - 1:
            i += 1
        last_pt = i - 1     # back up one point
    else:
        print("threshold is not within the range of heart rate")
        first_pt = 0
        last_pt = 0
    return first_pt, last_pt

def compute_mean_sd(curve, first_pt, last_pt):
    sum = 0.0
    cntr = 0
    for i in range (first_pt, last_pt):
        sum += curve[i]
        cntr += 1
    mean = sum / cntr
    # compute sd
    sum = 0.0
    cntr = 0
    for i in range (first_pt, last_pt):
        sum += (curve[i] - mean)**2
        cntr += 1
    sd = math.sqrt(sum / (cntr - 1))
    return mean, sd
try:
    file_name = 'D:/Biological Python Data/Heart Rate Data.csv'
    data = np.genfromtxt(file_name, delimiter=',', skip_header=1)
    pt_num = data[:, 0]     # take all rows from column 0
    heart_rate = data[:, 1] # take all rows from column 1
except FileNotFoundError:
    print("The file was not found: ", file_name)
    exit(1)


fp, lp = find_endpoints(x=pt_num, hr=heart_rate,threshold=80)
print("first pt is: ", fp)
print("last pt is: ", lp)

heart_rate_mean , heart_rate_sd = compute_mean_sd(curve=heart_rate, first_pt=0, last_pt=len(heart_rate))
plot_heart_rate(x=pt_num, hr=heart_rate, min_pt=fp, max_pt=lp)
print("mean heart rate is: ", format(heart_rate_mean, '.3f'))
print("sd heart rate is: ", format(heart_rate_sd, '.3f'))
save_stats_long(stat_file_path='D:/', hr=heart_rate)