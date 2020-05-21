const Bucket = require('../../RL-DataStructures/Bucket');
const ArrayUtil = require('../../RL-Utils/ArrayUtil');
const episodeCount = 1000;
const maxTimeSteps = 250;
const outDir = "/tmp/random-agent/results";
const numTrials = 3;

// Parameter to enable debug
const PRINT_DEBUG = true;

// Our Agent in charge of learning based on the observation and reward
class Agent {
  constructor(numberOfActions, numberOfObservations, observationSpaceInfo) {
    this.numberOfActions = numberOfActions;
    this.numberOfObservations = numberOfObservations;
    this.observationSpaceInfo = observationSpaceInfo;

    this.gamma = 1.0; // Discount factor
    this.minEpsilon = 0.1; // Exploration factor
    this.minAlpha = 0.1; // Learning Rate
    this.adaDivisor = 25;

    // Create buckets and states, for the CartPole we know that it's x, v, theta, alpha (position, velocity, angle, angular velocity)
    this.bucketArrays = this.initializeBuckets([1, 1, 8, 10]);
    this.states = this.initializeStates(this.bucketArrays);
    this.q = this.initializeQTable(this.states.length, this.numberOfActions);

    if (PRINT_DEBUG) {
      this.printDebug();
    }
  }

  initializeStates(buckets) {
    let bucketIndexes = [];
    buckets.forEach(bucket => {
      bucketIndexes.push(bucket.bucketIndexes);
    });

    let states = ArrayUtil.cartesianProduct(...bucketIndexes);

    return states;
  }

  /**
   *
   * We have an amount of observations, but to limit the states we can have we specify ranges or "buckets" for the values
   * In our initialization method, we define the amount of "steps" for each observation bucket
   * Example: 1, 1, 6, 12 means that for observation #0 we set 1 bucket, #2 also 1, #3 6 buckets and #4 12 buckets
   *          which represents that we will create 12 different steps for observation #4
   * @param {Array} buckets
   */
  initializeBuckets(bucketSizes) {
    let buckets = [];

    for (let i = 0; i < this.numberOfObservations; i++) {
      const bucketSize = bucketSizes[i];
      const upperBound = this.observationSpaceInfo.dimensionDouble.high[i];
      const lowerBound = this.observationSpaceInfo.dimensionDouble.low[i];
      buckets.push(new Bucket(bucketSize, lowerBound, upperBound));
    }

    return buckets;
  }

  /**
   * Since the amount of spaces that we can have is huge, we need to limit this
   *
   * This limiting is done through using "buckets", or we also say that we put everything that is between X and Y in bucket Z
   *
   *
   * For every feature we specify a range between where the values can be
   * TODO: Our Q-Table is [state<tuple>][action] so we need to define the tuple which is our number of observations
   * Therefore we need to "compact" them or write a "range" so that we do not overextend
   *
   * Note: this is also called "discretization"
   */
  initializeQTable(stateCount, actionCount) {
    let q = []; // Our Q-Table

    for (let stateIdx = 0; stateIdx < stateCount; stateIdx++) {
      q[stateIdx] = [];

      for (let actionIdx = 0; actionIdx < actionCount; actionIdx++) {
        q[stateIdx][actionIdx] = 0;
      }
    }

    return q;
  }

  /**
   * Convert our observation to a state index based on the buckets
   * @param {*} states
   * @param {*} bucketArrays
   * @param {*} observations
   */
  observationToStateIndex(states, bucketArrays, observations) {
    let observationBucketIndexes = [];

    for (let i = 0; i < observations.length; i++) {
      observationBucketIndexes.push(
        bucketArrays[i].getBucketIdxForValue(observations[i])
      );
    }

    let stateIndex = states
      .map(i => i.toString())
      .indexOf(observationBucketIndexes.toString());
    return stateIndex;
  }

  /**
   *
   * @param {Array} observation array of observations (e.g. [1, 6, 9, 2.3])
   * @param {number} reward The reward we got from taking the previous action
   */
  async act(client, episode, observation) {
    // ========================================================
    // 1. Map the current observation to a state
    // ========================================================
    // We get a number of values back, convert these to states
    let stateIndex = this.observationToStateIndex(
      this.states,
      this.bucketArrays,
      observation.observation
    );

    // Learning discount factor and learning rate
    const epsilon = this.getEpsilon(episode);
    const alpha = this.getAlpha(episode);

    // ========================================================
    // 2. Based on our observation, choose and take an action and view the change in environment
    // ========================================================
    // Choose an action
    const action = this.chooseAction(stateIndex, epsilon);
    let newEnvironment = await client.Step(action); // returns { isDone, info, observationBox, reward }

    // ========================================================
    // 3. Based on result of the action, update our Q value
    // ========================================================
    let newStateIndex = this.observationToStateIndex(
      this.states,
      this.bucketArrays,
      newEnvironment.observation.box
    );

    this.updateQ(
      stateIndex,
      action,
      newEnvironment.reward,
      newStateIndex,
      alpha
    );

    return {
        done: newEnvironment.isDone,
        info: {},
        observation: newEnvironment.observation.box,
        reward: newEnvironment.reward
    };
  }

  /**
   * Update our Q-Table based on the Bellman Equation for Action-Value
   * @param {number} oldStateIdx
   * @param {number} action
   * @param {number} reward
   * @param {number} newStateIdx
   * @param {number} alpha
   */
  updateQ(oldStateIdx, action, reward, newStateIdx, alpha) {
    this.q[oldStateIdx][action] +=
      alpha *
      (reward +
        this.gamma * ArrayUtil.getMaxValue(this.q[newStateIdx]) -
        this.q[oldStateIdx][action]);
  }

  /**
   * For exploration, return random action if Math.random <= explorationFactor (epsilon), else max Q value for the current state
   * @param {int} state
   */
  chooseAction(stateIndex, epsilon) {
    let random = Math.random();
    let isRandom = Math.random() <= epsilon;

    // If we want to explore (depending on epsilon), take a random action
    if (isRandom) {
      return Math.floor(Math.random() * this.numberOfActions);
    }

    return ArrayUtil.getIndexOfMaxValue(this.q[stateIndex]);
  }

  /**
   * Our exploration factor
   *
   * We use a dynamic parameter dependent on the episode, to be able to reduce exploration over our timeframe
   * @param {*} t
   */
  getEpsilon(t) {
    return Math.max(
      this.minEpsilon,
      Math.min(1.0, 1.0 - Math.log10((t + 1) / this.adaDivisor))
    );
  }

  /**
   * Our Learning factor
   *
   * We use a dynamic parameter dependent on the episode, to be able to reduce learning over our timeframe
   * @param {*} t
   */
  getAlpha(t) {
    return Math.max(
      this.minAlpha,
      Math.min(0.5, 1.0 - Math.log10((t + 1) / this.adaDivisor))
    );
  }

  /**
   * We get an observation (e.g.) [1, 6, 9, 2.3] which defines our "state" or what we currently see.
   * To get our state we need to look at each feature value (1, 6, ...) and define in which bucket these fit. Then we can resolve this to a state idx
   *
   * Our bucket id is then
   *
   * In this method we define this to a unique entry for our Q-Table
   *
   * @param {*} observation
   */
  convertObservationToBucketIndexes(observation) {
    let bucketIndexes = [];

    for (let i = 0; i < observation.length; i++) {
      let bucketIndex = Math.floor(
        (observation[i] - this.bucketArrays[i].lowerBound) /
          this.bucketArrays[i].bucketSize
      );
      bucketIndexes.push(bucketIndex);
    }

    return bucketIndexes;
  }

  /**
   * Help method to view some details about our algorithm
   */
  printDebug() {
    console.log("=======================================");
    console.log("Buckets");
    console.log("=======================================");
    console.table(this.bucketArrays);

    console.log("=======================================");
    console.log("Possible States");
    console.log("=======================================");
    console.table(this.states);

    console.log("=======================================");
    console.log("Initial Q-Table");
    console.log("=======================================");
    console.table(this.q);
  }
}

module.exports = Agent;