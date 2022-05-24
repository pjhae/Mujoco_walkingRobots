from gym.envs.registration import registry, register, make, spec


# Mujoco
# ----------------------------------------


register(
    id='Hexy-v4',
    entry_point='gym.envs.mujoco.hexy_v4:HexyEnv',
    max_episode_steps=3000,
)


register(
    id='MiniCheetah-v1',
    entry_point='gym.envs.mujoco.minicheetah_v1:MiniCheetahEnv',
    max_episode_steps=3000,
)

