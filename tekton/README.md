# Tekton run

These resources require a Kubernetes cluster with Tekton Pipelines installed and a workspace PVC named `accounts-source` containing this repository. Set the `image` parameter to a writable registry image and configure Kaniko push credentials plus Kubernetes pull access before running the pipeline.

```bash
kubectl apply -f pipeline.yaml
kubectl apply -f pipelinerun.yaml
kubectl logs -f pipelinerun/accounts-ci-cd-run -c step-test
```

The pipeline builds and pushes the image with Kaniko, applies the Kubernetes resources, updates the deployment image, then waits for rollout completion. A registry and cluster credentials are required.
