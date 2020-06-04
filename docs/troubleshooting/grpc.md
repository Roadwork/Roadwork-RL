# TroubleShooting - gRPC

pip install git+git://github.com/openai/gym.git

## General

## Specific Errors

**Failed to serialize response:**

* Is a response being returned correctly?

**"Exception calling application: True has type <class 'bool'>, but expected one of: (<class 'bytes'>, <class 'str'>):**

* Are you serializing wrong? E.g. is the `.proto` file expecting bytes class where bool is being sent?
* Check if it's on the server or client (add `print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")` and compare on client and server)
    * Best to print entire response on the server before sending it if it gets stuck there
    * E.g. `.proto` was expecting `map<str, str>` but python was providing `{ "Test": True }` which is a boolean

**"Exception calling application: EventLoop.run() must be called from the same thread that imports pyglet.app**

* Is there already an instance running?

**Exception calling application: b'invalid operation':**

* Check if it's on the server or client (add `print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")` and compare on client and server)
* If running on Windows, try executing: `$Env:LIBGL_ALWAYS_INDIRECT=0`


import traceback


os.environ["PYGLET_DEBUG_GL"] = "1"
os.environ["PYGLET_DEBUG_GL_TRACE"] = "1"

import sys

def my_except_hook(exctype, value, traceback):
    print(exctype)
    print(value)
    print(traceback)

sys.excepthook = my_except_hook




        try:
            print("1.1")
            env = self._lookup_env(instance_id)
            if isinstance(action, six.integer_types):
                nice_action = action
            else:
                nice_action = np.array(action)
            if render:
                env.render()

            print("1.2")
            
            [observation, reward, done, info] = env.step(nice_action)
            
            print("1.3")
            obs_jsonable = env.observation_space.to_jsonable(observation)
            print("1.4")
            return [obs_jsonable, reward, done, info]
        except:
            print(sys.exc_info())
            traceback.print_tb(sys.exc_info()[2])
            raise