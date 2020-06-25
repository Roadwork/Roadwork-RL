Running

```bash
# 1. Install Roadwork PIP
cd src/Lib/python/roadwork
pip install -e .

# 2. Install Stable Baselines
pip install stable_baselines

# 3. Start Server
cd src/
./Scripts/linux/run-server.sh OpenAI ../output-server/

# 4. Train
cd src/
./Scripts/linux/experiment-train.sh python baselines/cartpole

# 5. Infer
cd src/
./Scripts/linux/experiment-infer.sh python baselines/cartpole
```