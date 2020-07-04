import os
import sys
import gym
import traceback

from roadwork.server import Server

APP_PORT_GRPC    = os.getenv('APP_GRPC_PORT',  50050)
OUTPUT_DIRECTORY = os.getenv('ROADWORK_OUTPUT_DIR',  "")

print(f"============================================================")
print(f"APP_PORT_GRPC: {APP_PORT_GRPC}")
print(f"OUTPUT_DIRECTORY: {OUTPUT_DIRECTORY}")
print(f"============================================================")


# Our server methods
class OpenAI(Server):
    def __init__(self, sim_id, port):
        Server.__init__(self, sim_id, port)
        self.env = None

    def create(self, env_id, seed):
        try:
            self.env = gym.make(env_id)

            if seed:
                self.env.seed(seed)
        except gym.error.Error as e:
            print(e)
            raise Exception("Attempted to look up malformed environment ID '{}'".format(env_id))
        except Exception as e:
            print(e)
            raise Exception(e)
        except:
            print(sys.exc_info())
            traceback.print_tb(sys.exc_info()[2])
            raise

        return True

    def get_action_space_info(self):
        return self.env.action_space
        
    def get_observation_space_info(self):
        return self.env.observation_space

    def action_space_sample(self):
        action = self.env.action_space.sample()
        return action

    def reset(self):
        observation = self.env.reset()
        return observation

    def step(self, action, is_render):
        observation, reward, isDone, info = self.env.step(action, is_render)
        return observation, reward, isDone, info

    # def Render(self, request, context):
    #     return

    # def Close(self, request, context):
    #     return

    # def ActionSpaceSample(self, request, context): # ActionSpaceSampleResponse
    #     res = api_v1.ActionSpaceSampleResponse(actions=envs.get_action_space_sample(request.instanceId))
    #     return res

    # def ActionSpaceInfo(self, request, context): # ActionSpaceInfoResponse
    #     res = api_v1.ActionSpaceInfoResponse(result=envs.get_action_space_info(request.instanceId))
    #     return res

    # def ObservationSpaceInfo(self, request, context): # ObservationSpaceInfoResponse
    #     info = envs.get_observation_space_info(request.instanceId)
    #     res = api_v1.ObservationSpaceInfoResponse(result=info)
    #     return res

    # def MonitorStart(self, request, context): # BaseResponse
    #     envs.monitor_start(request.instanceId, OUTPUT_DIRECTORY, True, False, 10) # Log to local dir so we can reach it
    #     res = api_v1.BaseResponse()
    #     return res

    # def MonitorStop(self, request, context): # BaseResponse
    #     envs.monitor_close(request.instanceId)
    #     res = api_v1.BaseResponse()
    #     return res

    # print(f"[OnInvoke][{request.method}] Done @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

server = OpenAI("openai", APP_PORT_GRPC)
server.start()
