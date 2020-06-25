from dapr.actor import ActorInterface, actormethod

class RoadworkActorInterface(ActorInterface):
    """ Method to create a Sim Environment, returns True if created """
    @actormethod(name="SimCreate")
    async def sim_create(self, data: object) -> None:
        ...
    
    """ Method to reset a Sim Environment"""
    @actormethod(name="SimReset")
    async def sim_reset(self) -> object:
        ...

    """ Method to render a Sim Environment"""
    @actormethod(name="SimRender")
    async def sim_render(self) -> None:
        ...

    """ Method to render a Sim Environment"""
    @actormethod(name="SimStep")
    async def sim_step(self, data: object) -> object:
        ...

    """ Method to start the monitor on a Sim Environment"""
    @actormethod(name="SimMonitorStart")
    async def sim_monitor_start(self, data: object) -> object:
        ...

    """ Method to stop the monitor on a Sim Environment"""
    @actormethod(name="SimMonitorStop")
    async def sim_monitor_stop(self) -> object:
        ...

    @actormethod(name="SimActionSample")
    async def sim_action_sample(self) -> object:
        ...
    
    @actormethod(name="GetMyData")
    async def get_my_data(self) -> object:
        ...

    @actormethod(name="SetMyData")
    async def set_my_data(self, data: object) -> None:
        ...
