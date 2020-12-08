# Instructions

To walk through these demos you'll need at minimum the following:

* kubectl
* a working kubernetes cluster (see below for how to set up a local cluster using kind)
* helm (v3)

This step isn't necessary if you already have a kubernetes cluster available.

[Follow the installation instructions for kind here.](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

Next, create a kind cluster:

```bash
kind create cluster -f cluster.yaml
```

If you don't already have helm installed locally, or have v2 installed you'll need to ensure you have v3 installed to follow these demos. [Follow the installation instructions here.](https://helm.sh/docs/intro/install/)
