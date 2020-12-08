# Resource metric horizontal scaling

First lets make sure we can access the metrics API

```bash
kubectl top nodes
```

If you receive an error instead of statistics showing the resource usage of the nodes in your cluster you'll need to set up the [metrics-server](https://github.com/kubernetes-sigs/metrics-server) to scrape and serve the resource metrics in the cluster:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install metrics-server bitnami/metrics-server --set apiService.create=true --set extraArgs.kubelet-insecure-tls=true --set extraArgs.kubelet-preferred-address-types=InternalIP
```

Now you should be able to successfully run `kubectl top` against both nodes and pods:

```bash
kubectl top nodes
kubectl top pods -n kube-system
```

Lets install some workloads which will stress their resource quotas:

```bash
kubectl apply -f stress-deploy.yaml
```

We'll have to wait a bit for the containers to be created, the metrics to be scraped etc., but eventually:

```bash
kubectl top pods
```

You can see that the pods are already bumping up against their resource limits. Lets say we decide we want to give the CPU workload more capacity to do work, we can set it to scale to a target CPU usage, within some limits:

```bash
kubectl apply -f stress-hpa.yaml
kubectl get hpa -w
```

You can now see the HPA scaling the pods to try and achieve the target utilisation acording to an algorithm and some tunable parameters. In this case we'll never reach the target utilisation as we're just stressing the CPU, so lets delete the deployments for now:

```bash
kubectl delete -f stress-hpa.yaml
kubectl delete -f stress-deploy.yaml

```
