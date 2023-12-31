import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.image as mpimg
import numpy as np
import torch

def mover(tensor_data):
    #sum up the columns and rows and take their mean
    Column_sum = list(torch.sum(tensor_data[0, 1, :, :], axis = 0))
    Row_sum = list(torch.sum(tensor_data[0, 1, :, :], axis = 1))

    n_column = len(Column_sum)
    n_row = len(Row_sum)
    #take the difference between the mean and the desired channel you want to center around
    indices_array_row = np.arange(0, n_row)
    indices_array_col = np.arange(0, n_column)
    
    #take the weighted average to get the mean
    Column_mean = np.average(indices_array_col, weights = Column_sum)
    Row_mean = np.average(indices_array_row, weights = Row_sum)

    #take the difference between the mean and the desired mean
    mean_diff_row = np.round(Row_mean - 80)
    mean_diff_col = np.round(Column_mean - 80)
    
    #Splice the beginning/end of the array onto the other end
    
    dist_col = int(np.average(indices_array_col, weights = Column_sum)) - 70
    x_col = Column_sum[:dist_col]
    Column_adjusted = Column_sum[dist_col:]
    Column_adjusted.extend(x_col)
    #Column_adjusted = np.roll(Column_sum, -(dist_col), axis = 0)
    #dist_col_adj = int(np.average(indices_array_col, weights = Column_adjusted))
    
    #Do the same w/ rows
    dist_row = int(np.average(indices_array_row, weights = Row_sum)) - 70
    x_row = Row_sum[:dist_row]
    Row_adjusted = Row_sum[dist_row:]
    Row_adjusted.extend(x_row)
    #dist_row = int(np.average(indices_array_row, weights = Row_adjusted))
    #Row_adjusted = np.roll(Row_sum, -(dist_row), axis = 1)
    #dist_row_adjusted = int(np.average(indices_array_row, weights = Row_adjusted))
    #print('dist row adjusted', dist_row_adjusted, dist_col_adj)
    
    return dist_row, dist_col
    #return Column_sum, Row_sum, Column_adjusted, Row_adjusted

def image_mover(tensor_data, iteration = None):
    data = (tensor_data[0, 1, :, :])
    dist_col, dist_row = mover(tensor_data)
    data = np.roll(data, -(dist_col), axis = 0)
    data = np.roll(data, -(dist_row), axis = 1)
    return data

def matrix_calc(tensor_data, iteration = None):
    Column_sum, Row_sum, Column_adjusted, Row_adjusted = mover(tensor_data)
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)
    ax1.plot(Column_sum, label = 'columns')
    ax1.plot(Row_sum, label = 'rows')
    ax2.plot(Column_adjusted, label = 'columns adjusted')
    ax2.plot(Row_adjusted, label = 'rows adjusted')
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_xlabel('Channel')
    ax2.set_xlabel('Channel')
    ax1.set_ylabel('Sum of each channel')
    fig.savefig(f'/fast_scratch/ipress/egamma/tensor-plots-validation/matrix_calc_{iteration}.png')
    plt.close()
    return Row_sum, Column_sum, Column_adjusted, Row_adjusted

def plotter_val(tensor_data, iteration, labels):
    data = image_mover(tensor_data)
    plt.imshow(data, cmap='viridis', interpolation='nearest')
    plt.colorbar(label = 'Charge')
    if labels[1] == 1:
        plt.title('Electron cherenkov ring')
    else:
        plt.title('Gamma cherenkov ring')
    plt.xlabel('Horizontal channels')
    plt.ylabel('Vertical channels')
    print('tensor_data size = ', tensor_data.size())
    print(f'saving figure {iteration}')
    plt.savefig(f'/fast_scratch/ipress/egamma/tensor-plots-validation/tensor_plot_{iteration}.png')
    plt.close()
    #matrix_calc(tensor_data, iteration)

