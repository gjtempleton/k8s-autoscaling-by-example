# k8s-autoscaling-by-example

A basic walkthrough of kubernetes autoscaling in all its forms

## What is this repo

This repo is intended to give a hands-on overview of autoscaling in Kubernetes (k8s), allowing users to see the role each component plays and how they can impact the scaling of their workloads and/or clusters.

It will make use of a local Kind Cluster to walk users through deploying and scaling workloads.

## Creating a local Kind Cluster

If you have access to a test cluster of some other type you may skip this step, just ensure your command line and context are set up against the cluster you intend to use, though depending on how this is set up some of the below components may already be set up for you.

If you don't already have a test cluster, then follow the [latest instructions](https://github.com/kubernetes-sigs/kind#installation-and-usage) for setting up and running a Kind Cluster.

Once you have this set up you should successfully be able to run commands like

```bash
$ kubectl get nodes
NAME                 STATUS   ROLES    AGE   VERSION
kind-control-plane   Ready    master   39m   v1.17.0
```

## API Aggregation

Kubernetes does its job by making use of a wide range of APIs, allowing for API versioning and many other clever pieces of work. Most of the time these are opaque to Cluster users until they run into a deprecated API for instance. Their `kubectl top node` commands hiding the API behind it making requests to `/apis/metrics.k8s.io/v1beta1/nodes` and interpreting the response for the user. In most cases these APIs are served by the API server.

If you run

```bash
kubectl get apiservices.apiregistration.k8s.io
```

you will see a table of all of the APIs known by the k8s APIServer, whether they are available, when k8s first knew about them and which service is responsible for that API. Here `local` means that the cluster's APIServer will route the request via itself.

Kubernetes provides three core metrics APIs:

* `resource` - these are the memory and CPU utilisation metrics you see when running `kubectl top` against either Nodes or Pods. They're served under the `/apis/metrics.k8s.io/` API path
* `custom` - these are metrics that correspond to a kubernetes object but are not a resource metric. These can be arbitrary metrics as long as they correspond in a 1:1 mapping to a kubernetes object (like Pods in a scale target or a connected Ingress object)
* `external` - these are metrics that are entirely external to a kubernetes object but may neverless be a metric you want to scale on. They're served under the `apis/external.metrics.k8s.io/` API path

These APIs are referred to collectively as the metrics apis. To begin with a cluster will by default have no components to serve any of these metrics. This means that when you run

```bash
kubectl get apiservices.apiregistration.k8s.io
```

you won't see any components serving any of `metrics.k8s.io`, `custom.metrics.k8s.io` or `external.metrics.k8s.io`.

## Demos

This repo is intended to provide hands on demonstrations of each component of autoscaling in Kubernetes: horizontal, vertical and (eventually) cluster.

To follow the demos, change your working directory into each of the sub-directories in order and follow the hands on experiments in their README.md.

All feedback welcome!
