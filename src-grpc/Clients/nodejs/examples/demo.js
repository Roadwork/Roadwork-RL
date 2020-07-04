const Client = require('../Client');

const host = process.argv[2] || 'localhost:50051';

const start = async () => {
    console.log(`Connecting to: ${host}`);
    const client = new Client('CartPole-v0', host);
    await client.init();

    try { 
        // ObservationSpace Info
        const resObservationSpace = await client.ObservationSpaceInfo();

        console.log('\nObservation Space')
        console.log(resObservationSpace)

        // ActionSpace Info
        const resActionSpace = await client.ActionSpaceInfo();

        console.log('\nAction Space')
        console.log(resActionSpace)

        let actionSpaceSample = await client.ActionSpaceSample();
        console.log('\nActionSpace Sample');
        console.log(actionSpaceSample);

        // Step
        await client.MonitorStart();

        // Reset
        const resReset = await client.Reset();
        console.log('\nReset')
        console.log(resReset);

        let isDone = false;
        let i = 1;

        while (!isDone) {
            console.log(`Iteration: ${i}`);
            // await client.Render({ instanceId: res.instanceId });

            actionSpaceSample = await client.ActionSpaceSample();
            console.log(actionSpaceSample.action);

            console.log('Taking Step');
            const resStep = await client.Step({
                action: actionSpaceSample.action
            });
            console.log(resStep);

            isDone = resStep.isDone;
            i++;
        }
        
        await client.MonitorStop();
    } catch (e) {
        console.log(e);
    }
}

start();