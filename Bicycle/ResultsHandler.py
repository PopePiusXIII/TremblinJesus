class Result:
    def __init__(self, car):
        self.local = {'slip_fy': [],
                      'steer_fy': [],
                      'yaw_fy': [],
                      'fyf': [],
                      'fyr': [],
                      'mz1': [],
                      'mz2': [],
                      'mz3': [],
                      'steer': [],
                      'theta': [],
                      'beta': [],
                      'omega': [],
                      'alpha': [],
                      'saf': [],
                      'sar': [],
                      'time': [],
                      'vx': [],
                      'vy': [],
                      'ax': [],
                      'ay': [],
                      'rax': [],
                      'ray': [],
                      'x': [],
                      'y': []}
        self.world = {
            'time': [],
            'ax': [],
            'ay': [],
            'vx': [],
            'vy': [],
            'x': [],
            'y': [],
            'theta': []}

        self.car = car

    def write_local(self, t):
        """
        used to log internal states before changing to world for integration
        :param t: current time
        :param s_dot: current state
        :return:
        """
        self.local['theta'].append(self.car.frame_a.theta[2])
        self.local['beta'].append(self.car.RearAxle.sa)
        self.local['omega'].append(self.car.frame_a.omega[2])
        self.local['alpha'].append(self.car.frame_a.alpha)
        self.local['steer'].append(self.car.FrontAxle.delta)
        self.local['time'].append(t)
        self.local['x'].append(self.car.frame_a.r[0, 0])
        self.local['y'].append(self.car.frame_a.r[1, 0])
        self.local['vx'].append(self.car.frame_a.v[0, 0])
        self.local['vy'].append(self.car.frame_a.v[1, 0])
        self.local['ax'].append(self.car.frame_a.a[0, 0])
        self.local['ay'].append(self.car.frame_a.a[1, 0])
        self.local['fyf'].append(self.car.FrontAxle.fy()[1])
        self.local['fyr'].append(self.car.RearAxle.fy()[1])
        self.local['saf'].append(self.car.FrontAxle.sa)
        self.local['sar'].append(self.car.RearAxle.sa)

    def write_world(self, t):
        self.world['time'].append(t)
        self.world['x'].append(self.car.frame_ag.r[0, 0])
        self.world['y'].append(self.car.frame_ag.r[1, 0])
        self.world['ax'].append(self.car.frame_ag.a[0, 0])
        self.world['ay'].append(self.car.frame_ag.a[1, 0])
        self.world['vx'].append(self.car.frame_ag.v[0, 0])
        self.world['vy'].append(self.car.frame_ag.v[1, 0])
        self.world['theta'].append(self.car.frame_ag.theta)
