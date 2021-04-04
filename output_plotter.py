import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

class plotter:

    def __init__(self):
        # Containers for the time series
        self.detected_keypoints_x_ts = [[0] for i in range(18+1)]
        self.detected_keypoints_y_ts = [[0] for i in range(18+1)]
        self.detected_keypoints_t_ts = []

        plt.ion()
        self.fig = plt.figure(figsize=(13, 6))
        self.ax = self.fig.add_subplot(111)
        self.t0 = 0
        self.detected_keypoints_t_ts.append(self.t0)
        self.line1, = self.ax.plot(self.detected_keypoints_t_ts,  self.detected_keypoints_x_ts[17], '-o', alpha=0.8)
        plt.ylabel('Y Label')
        plt.title('Title: ')
        plt.show()

    def plotKeypointsTimeSeries(self, detected_kpts):

        for j in range(len(detected_kpts)):
            if detected_kpts[j] == []:
                point = [0, 0]
            else:
                point = [detected_kpts[j][0][0], detected_kpts[j][0][1]]
            self.detected_keypoints_x_ts[j].append(point[0])
            self.detected_keypoints_y_ts[j].append(point[1])

        self.t0 = self.t0 + 0.1
        self.detected_keypoints_t_ts.append(self.t0)
        self.line1.set_data(self.detected_keypoints_t_ts, self.detected_keypoints_y_ts[14])
        
        y1_data = self.detected_keypoints_y_ts[14]
        if np.min(y1_data) <= self.line1.axes.get_ylim()[0] or np.max(y1_data) >= self.line1.axes.get_ylim()[1]:
            plt.ylim([np.min(y1_data)-np.std(y1_data), np.max(y1_data)+np.std(y1_data)])
        
        x1_data = self.detected_keypoints_t_ts
        if np.min(x1_data) <= self.line1.axes.get_xlim()[0] or np.max(x1_data) >= self.line1.axes.get_xlim()[1]:
            plt.xlim([np.min(x1_data)-np.std(x1_data), np.max(x1_data)+np.std(x1_data)])
        
        plt.pause(0.001)
