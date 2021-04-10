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
        """Each keypoint's data will be ploted in a different figure. This functions takes care of initializing said figure

        Args:
            keypoint (int): Used to define the title of the fire to identify which keypoints is representing
            frame_size ([type]): size of the image frame used by OpenPose, this is used to define the maximum values for the u and v coordinates

        Returns:
            tuple: list containing the figure and axis objects used for plotting the keypoint data.
        """
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
        """ Constructor of the logger class

        Args:
            keypoint_list (list, optional): List of the keypoints to be ploted. Defaults to [].
            frame_size (tuple, optional): size of the image frame used by OpenPose, this is used to define the maximum values for the u and v coordinates. Defaults to (200,200).
        """

        # Initialize figures, axis and plotting lines for each keypoint
        self.keypoint_list = keypoint_list
        plt.ion()
        self.fig_list, self.ax_x_list , self.ax_y_list  = zip(*[ self.__init_figure(keypoint, frame_size) for keypoint in self.keypoint_list])
        self.line_x_list, _ = zip(*[ self.ax_x_list[i].plot(0, 0, 0.8) for i in range(len(self.keypoint_list))])
        self.line_y_list, _ = zip(*[ self.ax_y_list[i].plot(0, 0, 0.8) for i in range(len(self.keypoint_list))])

        # Containers for the time series data for the u and v coordinates of the keypoints
        self.t0 = time.time()
        self.kpt_u = []
        self.kpt_v = []

    def __updateAuxiliary(self, data_u, data_v, kpts_data):
        """[summary]

        Args:
            data_u (list): List containing the u coordinate data for the keypoints during one timestep
            data_v (list): List containing the v coordinate data for the keypoints during one timestep
            kpts_data (list): keypoint data to be added to the lists
        """

        if kpts_data == []:
            point = [0, 0]
        else:
            point = [kpts_data[0][0], kpts_data[0][1]]
        
        data_u.append(point[0])
        data_v.append(point[1])


    def updateKeypointTimeSeries(self, detected_kpts):
        """Add keypoints data to the time series containers

        Args:
            detected_kpts (list): data for the detected keypoints
        """
        # Create list for the current keypoints data
        t = time.time() - self.t0 
        data_u = [t] 
        data_v = [t] 
        [ self.__updateAuxiliary(data_u, data_v, detected_kpts[i]) for i in range(len(detected_kpts))]

        # Add current data to the time series containers
        self.kpt_u.append(data_u)
        self.kpt_v.append(data_v)

    def __loggedDataToPandas(self):
        """Convert the time series containers to a pandas dataframe.

        Returns:
            tuple: pandas dataframe for the u and v coordinates data
        """
        # Convert data to pandas dataframe
        u = pd.DataFrame(self.kpt_u, columns=['t', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_10', 'K_11', 'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_17'])
        v = pd.DataFrame(self.kpt_v, columns=['t', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8', 'K_9', 'K_10', 'K_11', 'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_17'])
        return u,v

    def __updatePlot(self, u, v, selected_kpt_index):
        """Auxiliary function to update the keypoints data plots

        Args:
            u (pandas dataframe): Data for the u coordinate of all the keypoints
            v (pandas dataframe): Data for the v coordinate of all the keypoints
            selected_kpt_index (int): [description]
        """
        # u coordinate plot
        self.line_x_list[selected_kpt_index].set_data(u['t'].tolist(), u['K_'+str(selected_kpt_index)].tolist())
        self.ax_x_list[selected_kpt_index].set_xlim(0, time.time() - self.t0)
        # v coordinate plot
        self.line_y_list[selected_kpt_index].set_data(u['t'].tolist(), v['K_'+str(selected_kpt_index)].tolist())
        self.ax_y_list[selected_kpt_index].set_xlim(0, time.time() - self.t0)         

    def plot(self):   
        """Graph the data for the u and v coordinates of the selected keypoints
        """
        # Get u and v coordinates data for all the keypoints
        u,v = self.__loggedDataToPandas()        
      
        # Update visualization        
        [self.__updatePlot(u, v, i) for i in range(len(self.keypoint_list))]
        plt.pause(0.001)
        
        self.saveData()
    
    def getData():
        """Withdraw the keypoints coordinates data

        Returns:
            u (pandas dataframe): Data for the u coordinate of all the keypoints
            v (pandas dataframe): Data for the v coordinate of all the keypoints
        """
        return self.__loggedDataToPandas()

    def saveData(self, u_data_filename, v_data_filename):
        """Dump the keypoints coordinates data into a csv file

        Args:
            u_data_filename (str): Filename for the .csv file for the u coordinate data
            v_data_filename (str): Filename for the .csv file for the v coordinate data
        """
        u,v = self.__loggedDataToPandas()   
        u.to_csv(u_data_filename)
        v.to_csv(v_data_filename)
