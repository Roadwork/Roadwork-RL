We need an X Server for rendering, so make sure to run:

```bash
xvfb -screen 0 1024x768x24 &
export DISPLAY=:0
```

This is only needed on the dev server, for Kubernetes we do this on init