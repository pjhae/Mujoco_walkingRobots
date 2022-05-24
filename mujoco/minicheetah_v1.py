import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env


DEFAULT_CAMERA_CONFIG = {
    'distance': 1.5,
}


class MiniCheetahEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self, xml_file='mini_cheetah/minicheetah-v1.xml',):
        utils.EzPickle.__init__(**locals())
        self._obs_buffer1 = np.zeros(12)
        self._obs_buffer2 = np.zeros(12)
        self._obs_buffer3 = np.zeros(12)
        self._act_buffer1 = np.zeros(12)
        self._act_buffer2 = np.zeros(12)
        self._act_buffer3 = np.zeros(12)
        mujoco_env.MujocoEnv.__init__(self, xml_file, 5)

    @property
    def is_healthy(self):
        # if cheetah tilted / changed position too much, reset environments
        is_healthy =  ( (np.abs(self.state_vector()[3:6]) < 0.8).all() and  (np.abs(self.state_vector()[2]) < 0.11) and (np.abs(self.state_vector()[3]) < 0.3 ) )
        # initially 0.11
        return is_healthy

    @property
    def done(self):
        done = not self.is_healthy
        return done

    def step(self, action):
        x_init = self.state_vector()[0]
        self.do_simulation(action, self.frame_skip)

        # update action and observation history
        self._act_buffer3 = self._act_buffer2
        self._act_buffer2 = self._act_buffer1
        self._act_buffer1 = action[:]
        self._obs_buffer3 = self._obs_buffer2
        self._obs_buffer2 = self._obs_buffer1
        self._obs_buffer1 = self.state_vector()[6:18]

        # calculate rewards and costs
        x_del = self.state_vector()[0] - x_init
        x_vel = x_del/self.dt
        
        y_err = np.abs(self.state_vector()[1])
        z_err = np.abs(self.state_vector()[2])
        
        pitch = np.abs(self.state_vector()[4])
        yaw = np.abs(self.state_vector()[5])
        
        ctrl = np.sum(np.square(self._act_buffer1 - self._act_buffer2))
        torque_rms = np.sqrt(np.mean(np.square(self.sim.data.actuator_force[:])))
        torque_ms = np.mean(np.square(self.sim.data.actuator_force[:]))
        
        #reward = x_vel/((torque_rms+1.5)*(z_err+0.15)*(pitch+yaw+0.4))+0.1
        #print(torque_rms)
        reward = 0.7* np.exp(-np.square(x_vel-4)) + 0.2* np.exp(-np.square(pitch)) + 0.1*np.exp(-np.square(torque_rms))
        


        done = self.done
        observation = self._get_obs()
        info = {
            'x_delta' : x_del,
            'y_error' : y_err,
            'control_norm' : ctrl,
            'total' : reward
        }

        return observation, reward, done, info

    def _get_obs(self):
        # take account of history
        return np.concatenate([self._obs_buffer1, self._obs_buffer2, self._obs_buffer3,
                               self._act_buffer1, self._act_buffer2, self._act_buffer3
                               ])

    def reset_model(self):
        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos, qvel)

        observation = self._get_obs()

        return observation

    def viewer_setup(self):
        for key, value in DEFAULT_CAMERA_CONFIG.items():
            if isinstance(value, np.ndarray):
                getattr(self.viewer.cam, key)[:] = value
            else:
                setattr(self.viewer.cam, key, value)
