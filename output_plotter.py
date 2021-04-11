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
        """ Constructor of the logger class. It will log all the keypoints data into a time series. Presenting the data as to pandas dataframes, one for each image coordinate.

        Args:
            keypoint_list (list, optional): List of the keypoints to be ploted. Defaults to [].
            frame_size (tuple, optional): size of the image frame used by OpenPose, this is used to define the maximum values for the u and v coordinates. Defaults to (200,200).
        """

        # Initialize figures, axis and plotting lines for each keypoint
        self.keypoint_list = keypoint_list
        plt.ion()
        self.fig_list, self.ax_x_list , self.ax_y_list  = zip(*[ self.__init_figure(keypoint, frame_size) for keypoint in self.keypoint_list])
        self.line_x_list, _ = zip(*[ self.ax_x_list[i].plot(0, 0, 0.8) for i in range(len(self.keypoint_list))])
        self.line_x_fod_list, _ = zip(*[ self.ax_x_list[i].plot(0, 0, 0.8) for i in range(len(self.keypoint_list))])
        self.line_x_sod_list, _ = zip(*[ self.ax_x_list[i].plot(0, 0, 0.8) for i in range(len(self.keypoint_list))])
        self.line_y_list, _ = zip(*[ self.ax_y_list[i].plot(0, 0, 0.8) for i in range(len(self.keypoint_list))])

        # Containers for the time series data for the u and v coordinates of the keypoints
        self.t0 = time.time()
        self.kpt_uv_data = []

    def __updateAuxiliary(self, data_uv, kpts_data):
        """[summary]

        Args:
            data_uv (list): List containing the u and v coordinates data for the keypoints during one timestep
            kpts_data (list): keypoint data to be added to the lists
        """

        if kpts_data == []:
            point = [0, 0]
        else:
            point = [kpts_data[0][0], kpts_data[0][1]]
        
        data_uv.append(point[0])
        data_uv.append(point[1])


    def updateKeypointTimeSeries(self, detected_kpts):
        """Add keypoints data to the time series containers

        Args:
            detected_kpts (list): data for the detected keypoints
        """
        # Create list for the current keypoints data
        t = time.time() - self.t0 
        data_uv = [t] 
        [ self.__updateAuxiliary(data_uv, detected_kpts[i]) for i in range(len(detected_kpts))]

        # Add current data to the time series containers
        self.kpt_uv_data.append(data_uv)

    def __loggedDataToPandas(self):
        """Convert the time series containers to a pandas dataframe.

        Returns:
            tuple: pandas dataframe for the u and v coordinates data
        """
        # Convert data to pandas dataframe
        columns_names = ['t', 'K_0_u', 'K_0_v', 
                              'K_1_u', 'K_1_v',  
                              'K_2_u', 'K_2_v',
                              'K_3_u', 'K_3_v', 
                              'K_4_u', 'K_4_v',
                              'K_5_u', 'K_5_v',
                              'K_6_u', 'K_6_v', 
                              'K_7_u', 'K_7_v', 
                              'K_8_u', 'K_8_v', 
                              'K_9_u', 'K_9_v', 
                              'K_10_u', 'K_10_v', 
                              'K_11_u', 'K_11_v', 
                              'K_12_u', 'K_12_v', 
                              'K_13_u', 'K_13_v', 
                              'K_14_u', 'K_14_v', 
                              'K_15_u', 'K_15_v', 
                              'K_16_u', 'K_16_v', 
                              'K_17_u', 'K_17_v']
        uv_data = pd.DataFrame(self.kpt_uv_data, columns=columns_names)
        return uv_data

    def __updatePlot(self, uv_data, selected_kpt_index):
        """Auxiliary function to update the keypoints data plots

        Args:
            uv_data (pandas dataframe): Data for the u and v coordinates of all the keypoints
            selected_kpt_index (int): [description]
        """
        # u coordinate plot
        self.line_x_list[selected_kpt_index].set_data(uv_data['t'].tolist(), uv_data['K_'+str(selected_kpt_index)+'_u'].tolist())
        self.ax_x_list[selected_kpt_index].set_xlim(0, time.time() - self.t0)
        # v coordinate plot
        self.line_y_list[selected_kpt_index].set_data(uv_data['t'].tolist(), uv_data['K_'+str(selected_kpt_index)+'_v'].tolist())
        self.ax_y_list[selected_kpt_index].set_xlim(0, time.time() - self.t0)         

    def plot(self):   
        """Graph the data for the u and v coordinates of the selected keypoints
        """
        # Get u and v coordinates data for all the keypoints
        uv_data = self.__loggedDataToPandas()        
      
        # Update visualization        
        [self.__updatePlot(uv_data, i) for i in range(len(self.keypoint_list))]

        selected_kpt_index =  1
        uv_data['fod_K_'+str(selected_kpt_index)+'_u'] = uv_data['K_'+str(selected_kpt_index)+'_u'].diff()
        uv_data['sod_K_'+str(selected_kpt_index)+'_u'] = uv_data['K_'+str(selected_kpt_index)+'_u'] - 2*uv_data['K_'+str(selected_kpt_index)+'_u'].shift(1) + uv_data['K_'+str(selected_kpt_index)+'_u'].shift(2)
        uv_data['sod_K_'+str(selected_kpt_index)+'_u'] = uv_data['sod_K_'+str(selected_kpt_index)+'_u']*10
        self.line_x_fod_list[selected_kpt_index].set_data(uv_data['t'].tolist(), uv_data['fod_K_'+str(selected_kpt_index)+'_u'].tolist())
        self.line_x_sod_list[selected_kpt_index].set_data(uv_data['t'].tolist(), uv_data['sod_K_'+str(selected_kpt_index)+'_u'].tolist())


        plt.pause(0.001)
            
    def getData(self):
        """Withdraw the keypoints coordinates data

        Returns:
            u (pandas dataframe): Data for the u coordinate of all the keypoints
            v (pandas dataframe): Data for the v coordinate of all the keypoints
        """
        return self.__loggedDataToPandas()

    def saveData(self, u_data_filename):
        """Dump the keypoints coordinates data into a csv file

        Args:
            u_data_filename (str): Filename for the .csv file for the u coordinate data
            v_data_filename (str): Filename for the .csv file for the v coordinate data
        """
        uv = self.__loggedDataToPandas()   
        uv.to_csv(u_data_filename)
