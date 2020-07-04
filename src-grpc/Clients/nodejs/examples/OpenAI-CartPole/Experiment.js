const CartPoleAgent = require('./Agent');
const MathUtil = require('../../RL-Utils/MathUtil');

class Experiment {
  constructor(simulatorClient, episodeCount = 1000, maxTimeSteps = 250) {
    this.env = null; // { instanceId: "" }
    this.actionSpaceInfo = null;
    this.agent = null;
    this.sim = simulatorClient;
    this.episodeCount = episodeCount;
    this.maxTimeSteps = maxTimeSteps;
  }

  async initialize() {
    // Our ActionSpace
    // For CartPole-v0 this returns: { info: { n: 2, name: 'Discrete' } }
    this.actionSpaceInfo = await this.sim.ActionSpaceInfo();
    this.actionSpaceInfo = this.actionSpaceInfo.result;

    // Our ObservationSpace
    // For CartPole-v0 this returns: { info: { high: [XXX], low: [XXX], name: 'Box', shape: [ 4 ] } }
    this.observationSpaceInfo = await this.sim.ObservationSpaceInfo();
    this.observationSpaceInfo = this.observationSpaceInfo.result;

    // Rebind our velocity and angular velocity parameters, the pole should stand still as much as possible
    this.observationSpaceInfo.box.dimensionDouble.high[1] = 0.5;
    this.observationSpaceInfo.box.dimensionDouble.low[1] = -0.5;
    this.observationSpaceInfo.box.dimensionDouble.high[3] = MathUtil.radians(50);
    this.observationSpaceInfo.box.dimensionDouble.low[3] = -MathUtil.radians(50);

    // Set our learning agent
    console.log('Action Space: ');
    console.log(this.actionSpaceInfo);
    console.log('Observation Space: ');
    console.log(this.observationSpaceInfo);

    this.agent = new CartPoleAgent(
      this.actionSpaceInfo.discrete.n,
      this.observationSpaceInfo.box.dimensions[0],
      this.observationSpaceInfo.box
    );
  }

  async run() {
    let oldObservation = [];

    await this.initialize();

    // Start Monitoring
    await this.sim.MonitorStart();

    // For every episode
    for (let episode = 0; episode < this.episodeCount; episode++) {
      // Reset the whole environment to start over
      let environment = {
        done: false,
        info: {},
        observation: await this.sim.Reset(),
        reward: 0
      };

      // Keep executing while we can:
      // if state.done = true, then that means the pole tipped to far, or we died
      // if t >= maxTimeSteps, then we did not solve it fast enough
      let t = 0;
      while (!environment.done && t < this.maxTimeSteps) {
        environment = await this.agent.act(
          this.sim,
          episode,
          environment.observation
        );
        t++;
      }

      console.log(`Episode ${episode} ended after ${t} timesteps`);
    }

    // Stop Monitoring
    await this.sim.MonitorStop();
    console.log(outDir);
  }
}

module.exports = Experiment;
