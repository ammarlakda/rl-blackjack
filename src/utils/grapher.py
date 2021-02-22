from mpl_toolkits import mplot3d 
import numpy as np 
import matplotlib.pyplot as plt 
  

def grapher(x, x_label, y_label, x_ticks=None, x_labels=None, title=None, save_file=None):
    '''
    Plots 2nd graph over given points x

    Args:
    - x (list): points to plot
    - x_label (str): label for x-axis
    - y_label (str): label for y_axis
    - x_ticks (list): location to plot x-axis labels
    - x_labels (list): labels for x-axis
    - title (str): title for plot
    - save_file (str): file to save plot to
    '''
    plt.clf()

    # Plot
    plt.plot(x)

    # Titling
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    if x_ticks is not None and x_labels is not None:
        plt.xticks(x_ticks, x_labels)
    if title is not None:
        plt.title(title)

    # Display
    if save_file is not None:
        plt.savefig(save_file)
  
def grapher3d(Z, title=None, save_file=None): 
    '''
    Plots a 3D graph over the points Z

    Args:
    - Z (np.ndarray): points to plot over
    - title (str): title of plot
    - save_file (str): file to save image to
    '''
    x = np.linspace(0,10,10)
    y = np.linspace(0,22, 22)
    X, Y = np.meshgrid(x, y) 

    fig = plt.figure() 
    ax = plt.axes(projection ='3d') 
    ax.plot_wireframe(X, Y, Z, color ='black') 
    ax.set_title(title)

    if save_file is not None:
        plt.savefig(save_file)