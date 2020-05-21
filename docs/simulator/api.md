# API

We have 2 API types, one for the RPC server and one for the SDK. The difference being that the SDK abstracts management of instances, ... away to make it easier to call the methods. Another difference is that the SDK also implements an `init` method to set-up the connection to the RPC Server.


## Server API

* **Create:** Create a new environment
  * `@returns`: instanceId (string - represents the spawned instance that we can interact with)
* **Step:** Execute one timestep within the environment
  * `@returns`: reward (the reward received)
  * `@returns`: observation (the next observation)
  * `@returns`: isDone (bool - is the instance finished? if yes we need to call reset())
* **Reset:** Reset the environment for the next use
* **MonitorStart:** Start monitoring the environment, the result is being saved as a video
* **MonitorStop:** Stop monitoring the environment
* **Seed:** Sets the seed for this environment's random number generated

## SDK API

* **Constructor:** 
    * `@param`: envId (the environment to create)
* **Init:** Initialize the connection to the environment
* **Reset:** See Server API
* **ActionSpaceSample:**  See Server API
* **ObservationSpaceInfo:** See Server API
* **ActionSpaceInfo:** See Server API
* **Step:** See Server API
    * `@param`: action (the action to execute)
* **MonitorStart:** See Server API
* **MonitorStop:** See Server API

For more information about the SDKs, see the [SDKs](./sdks.md) documentation
