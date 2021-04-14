import numpy as np

def distanceBetweenKeypoints(kpt_1, kpt_2):
    if kpt_1 == [] or kpt_2 == []:
        return -1
    #FIXME: causes error, to be fixed
    u = 0 #kpt_1[0] - kpt_2[0]
    v = 0 #kpt_1[1] - kpt_2[1]
    vect = (u, v)
    return np.linalg.norm(vect)

def elbowAngle(d_e_w, d_s_w, d_e_s):
    if d_e_w == -1 or d_s_w == -1 or d_e_s == -1:
        return -1
    theta = np.arccos((d_e_w*d_e_w+d_e_s*d_e_s-d_s_w*d_s_w)/(2*d_e_w*d_e_s))
    return theta*180/np.pi

def toDicitonary(keypoints):
    keypoints_data = {}
    
    for i in range(len(keypoints)):    
        if keypoints[i] != []:
            k = keypoints[i][0]
        else:
            k = []
        # Build a dictionary to save the keypoint data
        keypoints_data.update({'K_'+str(i):keypoints[i]})
    return keypoints_data

def getKeypointsData(keypoints):
    keypoints_data = toDicitonary(keypoints)
    # Compute the distance from the left elbow to the left shoulder
    keypoints_data.update({'d_le_ls': distanceBetweenKeypoints(keypoints_data['K_6'], keypoints_data['K_5'])})
    # Compute the distance from the right elbow to the right shoulder
    keypoints_data.update({'d_re_rs':distanceBetweenKeypoints(keypoints_data['K_3'], keypoints_data['K_2'])})
    # Compute the distance from the right elbow to the right wrist
    keypoints_data.update({'d_re_rw':distanceBetweenKeypoints(keypoints_data['K_3'],keypoints_data['K_4'])})
    # Compute the distance from the left elbow to the left wrist
    keypoints_data.update({'d_le_lw':distanceBetweenKeypoints(keypoints_data['K_6'],keypoints_data['K_7'])})
    # Compute the distance from the left shoulder to the left wrist
    keypoints_data.update({'d_ls_lw':distanceBetweenKeypoints(keypoints_data['K_5'],keypoints_data['K_7'])})
    # Compute the distance from the right shoulder to the right wrist
    keypoints_data.update({'d_rs_rw':distanceBetweenKeypoints(keypoints_data['K_2'],keypoints_data['K_4'])})
    # Compute the distance from the right shoulder to the left shoulder
    keypoints_data.update({'d_rs_ls':distanceBetweenKeypoints(keypoints_data['K_5'],keypoints_data['K_2'])})
    # Angle left elbow
    keypoints_data.update({'theta_le':elbowAngle(keypoints_data['d_le_lw'], keypoints_data['d_ls_lw'], keypoints_data['d_le_ls'])})
    # Angle right elbow 
    keypoints_data.update({'theta_re':elbowAngle(keypoints_data['d_re_rw'], keypoints_data['d_rs_rw'], keypoints_data['d_re_rs'])})

    return keypoints_data

