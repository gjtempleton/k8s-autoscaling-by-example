# External metrics scaling

First, lets install a rabbitmq setup into the cluster to make use of as a message queue and ensure we're scraping metrics from it (if you've deleted the Prometheus helm deploy from the cluster, you'll need to redeploy it to scrape the metrics)

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install rabbitmq bitnami/rabbitmq --set metrics.enabled=true
```

Now, lets deploy a workload which will publish some messages to that rabbit queue

```bash
kubectl apply -f rabbit-message-publisher.yaml
```

Assuming that we've kept the prometheus adapter from previous steps lets add some new rules to it for external metrics:

```bash
helm upgrade prometheus-adapter prometheus-community/prometheus-adapter --values prometheus-adapter-external-metrics-values.yaml
```

We'll need to wait some time for the new Prometheus-adapter instance to come to life and scrape metrics from Prometheus:

```bash
kubectl get apiservices.apiregistration.k8s.io
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1"
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1/namespaces/default/rabbitmq_queue_messages" | jq .
```

Lets read some messages off that queue as well to simulate the app doing work by pull messages off the queue and processing them:

```bash
kubectl apply -f rabbit-message-consumer.yaml
```

Now, we can see that the queue length is ever growing as we have more producers than consumers

```bash
kubectl apply -f rabbit-message-consumer-external-metrics-hpa.yaml
kubectl get hpa -w
```
