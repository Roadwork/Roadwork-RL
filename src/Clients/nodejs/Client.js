const GRPCHelper = require('grpc-helper').GRPCHelper;

const grpcLoader = require('@grpc/proto-loader');
const grpc = require('grpc');
const Path = require('path');
const grpcPromise = require('grpc-promise');

class Client {
    constructor(envId, grpcServerUrl='localhost:50051') {
        this.envId = envId;
        this.instanceId = null;
        this.grpcServerUrl = grpcServerUrl;
    }

    async init() {
        const client = new GRPCHelper({
            packageName: 'roadwork.simulator',
            serviceName: 'Simulator',
            protoPath: 'service.proto',
            sdUri: `static://${this.grpcServerUrl}`,
            grpcProtoLoaderOpts: {
                // Note: we need to include all paths
                includeDirs: [ 
                    `${__dirname}/../../protobuf-definitions/`, 
                    `${__dirname}/../../protobuf-definitions/system`,
                    `${__dirname}/../../protobuf-definitions/services/simulator` 
                ]
            }
        });
        await client.waitForReady();

        this.client = client;

        // Create the envrionment
        const res = await client.Create({ envId: this.envId });

        this.instanceId = res.instanceId;
    
        return client;
    }

    async Reset() {
        return this.client.Reset({ instanceId: this.instanceId });
    }

    async ActionSpaceSample() {
        return this.client.ActionSpaceSample({ instanceId: this.instanceId });
    }

    async ObservationSpaceInfo() {
        return this.client.ObservationSpaceInfo({ instanceId: this.instanceId });
    }
    
    async ActionSpaceInfo() {
        return this.client.ActionSpaceInfo({ instanceId: this.instanceId });
    }

    async Step(action) {
        return this.client.Step({
            instanceId: this.instanceId,
            action
        });
    }

    async MonitorStart() {
        return this.client.MonitorStart({ instanceId: this.instanceId });
    }

    async MonitorStop() {
        return this.client.MonitorStop({ instanceId: this.instanceId });
    }
}

module.exports = Client;
