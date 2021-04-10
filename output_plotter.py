import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import copy

plt.style.use('ggplot')

# Image plane: The reference frame for the pixel values is situated on the top-left corner
#        u
#    o------> 
#    |   ________
#  v |  |        |
#    |  | __()__ | 
#    v  |   ||   |
#       |   /\   | 
#       |________|

class openPoseOutputLogger:
   
    def __init_figure(self, keypoint, frame_size):
        fig = plt.figure('Keypoint: ' + str(keypoint))
        ax_x = plt.subplot(1, 2, 1)
        ax_y = plt.subplot(1, 2, 2)
        ax_x.set_xlabel('time')
        ax_x.set_title('u')
        ax_x.set_ylim(0, frame_size[0])
        ax_y.set_xlabel('time')
        ax_y.set_title('v')
        ax_y.set_ylim(0, frame_size[1])

        return [fig, ax_x, ax_y]

    def __init__(self, keypoint_list = [], frame_size = (200,200)):      

        # Initialize figures, axis and plotting lines for each keypoint
        self.keypoint_list = keypoint_list
        plt.ion()
        self.fig_list, self.ax_x_list , self.ax_y_list  = zip(*[ self.__init_figure(keypoint, frame_size) for keypoint in self.keypoint_list])
        self.line_x_list, _ = zip(*[ self.ax_x_list[i].plot(0, 0, 0.8) for i in range(len(self.keypoint_list))])
        self.line_y_list, _ = zip(*[ self.ax_y_list[i].plot(0, 0, 0.8) for i in range(len(self.keypoint_list))])

        # Data containers
        self.t0 = time.time()
        self.kpt_u = []
        self.kpt_v = []

    def __updateAuxiliary(self, data_u, data_v, kpts_data):

        if kpts_data == []:
            point = [0, 0]
        else:
            point = [kpts_data[0][0], kpts_data[0][1]]
        
        data_u.append(point[0])
        data_v.append(point[1])


    def updateKeypointTimeSeries(self, detected_kpts):
        # Add detected keypoint to time series
        t = time.time() - self.t0 
        data_u = [t] 
        data_v = [t] 
        [ self.__updateAuxiliary(data_u, data_v, detected_kpts[i]) for i in range(len(detected_kpts))]

        self.kpt_u.append(data_u)
        self.kpt_v.append(data_v)

    def __loggedDataToPandas(self):
        # Convert data to pandas dataframe
        u = pd.DataFrame(self.kpt_u, columns=['t', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_10', 'K_11', 'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_17'])
        v = pd.DataFrame(self.kpt_v, columns=['t', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_10', 'K_11', 'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_17'])
        return u,v

    def __updatePlot(self):
        pass
    def plot(self):     

        u,v = self.__loggedDataToPandas()        
      
        # Update visualization
        x_axis_data = u['t'].tolist()

        for i in range(len(self.keypoint_list)):
            # Keypoint x coordinate data
            y_axis_data = u['K_'+str(i)].tolist()
            self.line_x_list[i].set_data(x_axis_data, y_axis_data)
            self.ax_x_list[i].set_xlim(0, time.time() - self.t0)
            # Keypoint y coordinate data
            y_axis_data = v['K_'+str(i)].tolist()
            self.line_y_list[i].set_data(x_axis_data,y_axis_data)
            self.ax_y_list[i].set_xlim(0, time.time() - self.t0)            
        plt.pause(0.001)
        
        self.saveData()

    def saveData(self):
        pass
