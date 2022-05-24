import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize


date = "1213"
trial = "B"
steps = "48000000"


env = make_vec_env("MiniCheetah-v1", n_envs=1)
#env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=10.)


save_path='./save_model_'+date+'/'+trial+'/'

model = PPO.load(save_path+"cheetah_model_"+date+trial+"_"+steps+"_steps")

obs = env.reset()



while True:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()



#for i in range(12000):
#    action, _states = model.predict(obs)
#    line = []
#    line.append(str(action[0][0]))
#    for i in range(1, 12):
#        line.append(',')
#        line.append(str(action[0][i]))
#    line.append('\n')
#    line = ''.join(line)
#    obs, rewards, dones, info = env.step(action)
#    env.render()


