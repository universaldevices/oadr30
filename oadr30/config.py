#Universal Devices
#MIT License


class OADR3Config:

    '''
        Use oadr3_scale to scale up/down the durations. i.e. 
        Scale=1/5, changes the duration to duration /= 5
        scale=5, changes the duration to duration *= 5
        Mostly used for test purposes
    '''
    duration_scale:float=1.0