import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env


DEFAULT_CAMERA_CONFIG = {
    'distance': 1.5,
}


class HexyEnv(mujoco_env.MujocoEnv, utils.EzPickle):
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
        # if hexy was tilted or changed position too much, reset environments
        is_healthy = np.abs(self.state_vector()[1]) < 0.5\
                     and (np.abs(self.state_vector()[3:6]) < 0.7).all()
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
        y_err = np.abs(self.state_vector()[1])
        yaw = np.abs(self.state_vector()[1])
        #ctrl = np.sum(np.square(self._act_buffer1 - self._act_buffer2))
        torque_rms = np.sqrt(np.mean(np.square(self.sim.data.actuator_force[:])))
        reward = x_del / (torque_rms + 1) / (y_err + 0.1)

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
