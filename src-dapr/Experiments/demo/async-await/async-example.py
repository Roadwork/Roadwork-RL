import asyncio

from dapr.actor import ActorProxy, ActorId
from rw_actor_interface import RoadworkActorInterface


async def main():
    # Create proxy client
    proxy = ActorProxy.create('RoadworkActor', ActorId('1'), RoadworkActorInterface)

    # -----------------------------------------------
    # Actor invocation demo
    # -----------------------------------------------
    # non-remoting actor invocation
    print("call actor method via proxy.invoke()", flush=True)
    rtn_bytes = await proxy.invoke("GetMyData")
    print(rtn_bytes, flush=True)

    # RPC style using python duck-typing
    print("call actor method using rpc style", flush=True)
    rtn_obj = await proxy.GetMyData()
    print(rtn_obj, flush=True)

    # -----------------------------------------------
    # Actor sim environment demo
    # -----------------------------------------------
    await proxy.SimCreate({ 'env_id': 'CartPole-v1' })
    await proxy.SimMonitorStart()

    for episode in range(2):
        await proxy.SimReset()
        step = 0
        total_reward = 0

        while True:
            step += 1
            # await proxy.SimRender()

        # for i in range(5):
            action = await proxy.SimActionSample()
            print(f'Action taking: {action}', flush=True)

            obs, reward, done, info = await proxy.SimStep({ 'action': action })
            print(f'Received:', flush=True)
            print(f'- Obs: {obs}', flush=True)
            print(f'- Rewards: {reward}', flush=True)
            print(f'- Done: {done}', flush=True)
            print(f'- Info: {info}', flush=True)

            total_reward += reward

            if done:
                print("Episode: {0},\tSteps: {1},\tscore: {2}"
                    .format(episode, step, total_reward)
                )
                break
    
    await proxy.SimMonitorStop()

    # for i in range(10000):
    #     action, _states = model.predict(obs)
    #     obs, rewards, dones, info = env_local.step(action)
    #     env_local.render()

    # # -----------------------------------------------
    # # Actor state management demo
    # # -----------------------------------------------
    # # Invoke SetMyData actor method to save the state
    # print("call SetMyData actor method to save the state", flush=True)
    # await proxy.SetMyData({'data': 'new_data'})
    # # Invoke GetMyData actor method to get the state
    # print("call GetMyData actor method to get the state", flush=True)
    # rtn_obj = await proxy.GetMyData()
    # print(rtn_obj, flush=True)


asyncio.run(main())