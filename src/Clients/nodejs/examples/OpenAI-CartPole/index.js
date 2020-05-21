/**
 * For more information, check: https://gym.openai.com/docs/
 */
const Client = require('../../Client');
const Experiment = require('./Experiment');

const host = process.argv[2] || 'localhost:50051';

const start = async () => {
    const client = new Client('CartPole-v0', host);
    await client.init();

    // Create and run our experiment
    const episodeCount = 1000;
    const maxTimeSteps = 250;
    const experiment = new Experiment(client, episodeCount, maxTimeSteps);
    await experiment.run();
}

start();

