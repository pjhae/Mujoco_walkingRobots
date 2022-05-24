import gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from typing import Callable
from stable_baselines3.common.callbacks import EveryNTimesteps, CheckpointCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize

def lin_schedule(initial_value: float, final_value: float) -> Callable[[float], float]:
    def func(progress_remaining: float) -> float:
        return progress_remaining * (initial_value - final_value) + final_value
    return func

date = "1215"
trial = "A"

checkpoint_on_event = CheckpointCallback(
    save_freq=1,
    save_path='./save_model_'+date+'/'+trial,
    verbose=2,
    name_prefix='cheetah_model_'+date+trial
)

event_callback = EveryNTimesteps(
    n_steps=int(1e5),  # every n_steps, save the model
    callback=checkpoint_on_event
)


env = make_vec_env("MiniCheetah-v1", n_envs=4)
#env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=10.)
model = PPO("MlpPolicy", env=env, verbose=2, tensorboard_log='./cheetah_tb_log_'+ date,
            learning_rate=lin_schedule(3e-4, 3e-6), clip_range=lin_schedule(0.3, 0.1),
            n_epochs=10, ent_coef=1e-4, batch_size=256*4, n_steps=256)

model.learn(total_timesteps=50000000,
		callback=event_callback,  # every n_steps, save the model.
		tb_log_name='cheetah_tb_'+date+trial
		# ,reset_num_timesteps=False   # if you need to continue learning by loading existing model, use this option.
		
		)


model.save("cheetah_first")
del model # remove to demonstrate saving and loading
model = PPO.load("cheetah_first")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
