import matplotlib.pyplot as plt
import numpy as np
import time

plt.style.use('ggplot')


class plotter:

    def __init_line(self, x_data, y_data, point_type, alpha, coordinate):
        if coordinate == 'x':
            line = self.ax_x.plot(x_data, y_data, alpha)
        else:
            line = self.ax_y.plot(x_data, y_data, alpha)
        return line[0]

    def __init__(self, keypoint, frame_size):
        self.keypoint = keypoint
        # Containers for the time series
        self.detected_keypoints_x_ts = [[0] for i in range(18+1)]
        self.detected_keypoints_y_ts = [[0] for i in range(18+1)]
        self.detected_keypoints_t_ts = []

        plt.ion()
        self.fig, (self.ax_x, self.ax_y) = plt.subplots(1, 2) 
        self.fig.suptitle('Keypoint: ' + str(self.keypoint), fontsize=16)
        
        
        self.t0 = time.time()
        self.detected_keypoints_t_ts.append(self.t0)
        self.line_x_list = [ self.__init_line(self.detected_keypoints_t_ts,  self.detected_keypoints_x_ts[keypoint],'-.', alpha=0.8, coordinate='x') for i in range(18+1)]
        self.line_y_list = [ self.__init_line(self.detected_keypoints_t_ts,  self.detected_keypoints_y_ts[keypoint],'-.', alpha=0.8, coordinate='y') for i in range(18+1)]

        self.ax_x.set_xlabel('time')
        self.ax_x.set_title('x')
        self.ax_x.set_ylim(0, frame_size[0])
        self.ax_y.set_xlabel('time')
        self.ax_y.set_title('y')
        self.ax_y.set_ylim(0, frame_size[1])
        plt.show()



    def plotKeypointsTimeSeries(self, detected_kpts):

        for j in range(len(detected_kpts)):
            if detected_kpts[j] == []:
                point = [0, 0]
            else:
                point = [detected_kpts[j][0][0], detected_kpts[j][0][1]]
            self.detected_keypoints_x_ts[j].append(point[0])
            self.detected_keypoints_y_ts[j].append(point[1])

        t = time.time() - self.t0 
        self.detected_keypoints_t_ts.append(t)
        self.line_x_list[self.keypoint].set_data(self.detected_keypoints_t_ts[1:], self.detected_keypoints_x_ts[self.keypoint][1:])
        self.ax_x.set_xlim(0, t)
        self.line_y_list[self.keypoint].set_data(self.detected_keypoints_t_ts[1:], self.detected_keypoints_y_ts[self.keypoint][1:])
        self.ax_y.set_xlim(0, t)
          
        
        
        plt.pause(0.001)
