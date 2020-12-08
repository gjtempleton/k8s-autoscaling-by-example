# Vertical Pod Autoscaling

What if instead of scaling our workloads horizontally by adding more replicas, we wanted instead to scale vertically, by giving our pods more resources when needed?

First we'll install the components of the VPA:

```bash
helm repo add cowboysysop https://cowboysysop.github.io/charts/
helm install vpa cowboysysop/vertical-pod-autoscaler
```

Install a couple of stress deployments again:

```bash
kubectl apply -f stress-deploy.yaml
```

And now install a VPA object to tell the recommender of the VPA to watch the deployment:

```bash
kubectl apply -f stress-vpa.yaml
```

Now if we watch the logs of the recommender we can see it beginning to watch the pods in the deployment:

```bash
kubectl logs -f -l app.kubernetes.io/component=recommender
```

It'll take roughly 5 minutes before the VPA has enough data to start changing the pod resource requests, but you can also examine the VPA object you've created:

```bash
kubectl describe verticalpodautoscalers.autoscaling.k8s.io stress-cpu-vpa
```

Now, we're only running one pod at the moment, so lets scale the deployment and see what happens

```bash
kubectl scale deployment cpu-stress-app --replicas 2
kubectl describe pod -l app=cpu-stress-app
```

Take a close look at the new resource requests and limits.
