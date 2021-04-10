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

    def __init_line(self, x_data, y_data, point_type, alpha, coordinate, keypoint):
        if coordinate == 'x':
            line = self.ax_x_list[keypoint].plot(x_data, y_data, alpha)
        else:
            line = self.ax_y_list[keypoint].plot(x_data, y_data, alpha)
        return line[0]
    
    def __init_figure(self):
        pass

    def __init__(self, keypoint_list, frame_size):
        self.keypoint_list = keypoint_list
        plt.ion()

        # Initialize figures for each keypoint
        self.fig_list = []
        self.ax_x_list = []
        self.ax_y_list = []

        for keypoint in self.keypoint_list:
            fig = plt.figure('Keypoint: ' + str(keypoint))
            ax_x = plt.subplot(1, 2, 1)
            ax_y = plt.subplot(1, 2, 2)
            ax_x.set_xlabel('time')
            ax_x.set_title('u')
            ax_x.set_ylim(0, frame_size[0])
            ax_y.set_xlabel('time')
            ax_y.set_title('v')
            ax_y.set_ylim(0, frame_size[1])
            self.fig_list.append(fig)
            self.ax_x_list.append(ax_x)
            self.ax_y_list.append(ax_y)
                      
        self.t0 = time.time()

        data = [self.t0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 0]
        self.kpt_u = [data]
        self.kpt_v = [data]
     
        u = pd.DataFrame(self.kpt_u, columns=['t', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_10', 'K_11', 'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_17'])
        v = pd.DataFrame(self.kpt_v, columns=['t', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_10', 'K_11', 'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_17'])
       
        self.line_x_list = [ self.__init_line(u['t'].tolist(), u['K_'+str(i)].tolist(),'-.', alpha=0.8, coordinate='x',keypoint=i) for i in range(len(self.keypoint_list))]
        self.line_y_list = [ self.__init_line(v['t'].tolist(), v['K_'+str(i)].tolist(),'-.', alpha=0.8, coordinate='y',keypoint=i) for i in range(len(self.keypoint_list))]
     
        plt.show()

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

        print('Data u' + str(len(data_u)))
        print(data_u)
        self.kpt_u.append(data_u)
        print('Data kpt_u' + str(len(self.kpt_u)))
        print(self.kpt_u)
        self.kpt_v.append(data_v)

    def plot(self):       

        # Add time to time series
        t = time.time() - self.t0 

        u = pd.DataFrame(self.kpt_u, columns=['t', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_10', 'K_11', 'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_17'])
        v = pd.DataFrame(self.kpt_v, columns=['t', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_10', 'K_11', 'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_17'])

        # Update visualization
        x_axis_data = u['t'].tolist()[1:]

        for i in range(len(self.keypoint_list)):
            # Keypoint x coordinate data
            y_axis_data = u['K_'+str(i)].tolist()[1:]
            self.line_x_list[i].set_data(x_axis_data, y_axis_data)
            self.ax_x_list[i].set_xlim(0, t)
            # Keypoint y coordinate data
            y_axis_data = v['K_'+str(i)].tolist()[1:]
            self.line_y_list[i].set_data(x_axis_data,y_axis_data)
            self.ax_y_list[i].set_xlim(0, t)            
        plt.pause(0.001)
        self.saveData()

    def saveData(self):
        print("Saving data")
        #column_values =  [pd.Series(u) for u in self.detected_keypoints_u_ts]
        #column_values.to_csv('test.csv')
        #    
