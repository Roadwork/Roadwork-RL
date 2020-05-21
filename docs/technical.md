# Documentation - Technical

From a technological point of view we are utilizing Dapr to create an easy to use Microservice through the gRPC transport layer. To put this into a diagram, we can think of this as the following:

![/assets/architecture-dapr.svg](/assets/architecture-dapr.svg)

The architecture exists out of a Server environment that is providing the Simulator integration while on the other side a Client is created through an SDK integration that allows us to write experiments easily. The entire gRPC layer is abstracted away from the end-user, such that the Subject Matter Expert (Data Scientist) is able to utilize this SDK in a way they are used to.

Find more information about the [sdk here](./sdk/index.md)

### Setting up DISPLAY

To have `pyglet` correctly render as required in some environments (e.g. OpenAI), it is required to have a Display Server that can handle this. For Windows we utilize the `XMing` Server that can be downloaded from the following link: [https://sourceforge.net/projects/xming/](https://sourceforge.net/projects/xming/).

Once this is installed, we have to configure an environment variable that lets our WSL 2 environment know where this Server is running. Since WSL 2 is a full native linux system, we thus have to configure it to connect to our windows system. 

For this fetch your local IP address and export it to the variable `DISPLAY`, e.g.: `export DISPLAY="192.168.1.4:0"`.