# Custom Metrics Scaling

## Credit to the [Prometheus Adapter's Walkthrough](https://github.com/DirectXMan12/k8s-prometheus-adapter/blob/master/docs/walkthrough.md) on which this section is based

What if we have a workload which doesn't scale its ability to do work with its resource usage (whether CPU or Memory) but instead on a metric that the workload knows about itself?

This is where custom metrics autoscaling comes in.

There's a [number of different projects](https://github.com/kubernetes/metrics/blob/master/IMPLEMENTATIONS.md#custom-metrics-api) capable of serving custom metrics within a cluster, for this demo we'll usee the [prometheus-adapter](https://github.com/DirectXMan12/k8s-prometheus-adapter).

First lets make sure we have a Prometheus installed in the cluster and port-forward to make sure its successfully scraping metrics. We'll lower its scrape interval from the default to get a faster feedback loop.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus --set server.global.scrape_interval=30s
kubectl port-forward service/prometheus-server 9090:80
```

And visit the [Prometheus](http://localhost:9090) in the browser.

Next lets install an application with Prometheus metrics for Prometheus to scrape:

```bash
kubectl apply -f sample-app-deploy.yaml
```

Port-forward to Prometheus again and check the metrics are successfully being scraped from the workload we've just deployed by running the query: `http_requests_total`

We can also port-forward to our deployed pod to cause requests:

```bash
kubectl port-forward service/sample-app 8080:80
```

Now if we visit [the app](http://localhost:8080) and [its metrics page](http://localhost/metrics) we can see its counter of total requests ever served ever increasing.

Next we need something to transform these metrics into API requests Kubernetes' controller manager can understand, that's where the Prometheus-adapter comes in:

```bash
helm install prometheus-adapter prometheus-community/prometheus-adapter --values prometheus-adapter-values.yaml
```

Wait some time for the pod to become ready, and you should see a new metrics API being served:

```bash
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1/namespaces/default/pods/*/http_requests_per_second?selector=app%3Dsample-app" | jq
```

Now we can deploy an HPA making use of that metric, and if we trigger load against the service, we should see scaling due to the increase in requests per second:

```bash
kubectl apply -f sample-app-hpa.yaml
kubectl apply -f sample-app-load-generator.yaml
kubectl get hpa -w
```
