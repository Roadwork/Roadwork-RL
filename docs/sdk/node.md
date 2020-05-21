# SDKs - NodeJS

## Example - OpenAI Cartpole - Random Agent

```javascript
const client = new Client('CartPole-v0');
await client.init();
await client.MonitorStart();
await client.Reset();

for (let i = 0; i < 1000; i++) {
  actionSpaceSample = await client.ActionSpaceSample();
  const resStep = await client.Step(actionSpaceSample.action);  
}

await client.MonitorStop();
```

## Example - OpenAI Cartpole - Q-Learning

Currently a Node.js Cartpole agent that is utilizing Q-Learning has been implemented at `src/SDKs/nodejs/examples/OpenAI-CartPole`. To run this, do the following:

1. Install the OpenAI Gym (see `Simulators - OpenAI`)
2. Install Node.js
3. Run `python server.py` under `src/SimulatorIntegrations/OpenAI-Gym`
4. Run `node index.js` under `src/SDKs/nodejs/examples/OpenAI-CartPole`
