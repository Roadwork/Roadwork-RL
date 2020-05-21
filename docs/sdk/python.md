# SDKs - Python

## Example - OpenAI Cartpole - Random Agent

```python
import gym

env = gym.make('CartPole-v0')
env.reset()

for _ in range(1000):
    env.render()
    env.step(env.action_space.sample())
    
env.close()
```
