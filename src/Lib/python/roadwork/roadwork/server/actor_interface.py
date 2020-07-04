from dapr.actor import ActorInterface, actormethod

class RoadworkActorInterface(ActorInterface):
    """ Method to create a Sim Environment, returns True if created """
    @actormethod(name="SimCreate")
    def sim_create(self, data: object) -> None:
        ...
    
    """ Method to reset a Sim Environment"""
    @actormethod(name="SimReset")
    def sim_reset(self) -> object:
        ...

    """ Method to render a Sim Environment"""
    @actormethod(name="SimRender")
    def sim_render(self) -> None:
        ...

    """ Method to render a Sim Environment"""
    @actormethod(name="SimStep")
    def sim_step(self, data: object) -> object:
        ...

    """ Method to start the monitor on a Sim Environment"""
    @actormethod(name="SimMonitorStart")
    def sim_monitor_start(self, data: object) -> object:
        ...

    """ Method to stop the monitor on a Sim Environment"""
    @actormethod(name="SimMonitorStop")
    def sim_monitor_stop(self) -> object:
        ...

    @actormethod(name="SimActionSample")
    def sim_action_sample(self) -> object:
        ...

    @actormethod(name="SimActionSpace")
    def sim_action_space(self) -> object:
        ...

    @actormethod(name="SimObservationSpace")
    def sim_observation_space(self) -> object:
        ...

    @actormethod(name="SimGetState")
    async def sim_get_state(self, data: object) -> object:
        ...

    @actormethod(name="SimSetState")
    async def sim_set_state(self, data: object) -> None:
        ...

    @actormethod(name="SimCallMethod")
    async def sim_call_method(self, data: object) -> None:
        ...
