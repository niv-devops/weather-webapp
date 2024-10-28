# Kubernetes Manifests for Weather WebApp

This repository contains the declarative Kubernetes manifests for deploying the Weather WebApp using ArgoCD and GitOps principles.

## Repository Structure

```
manifests/
├── application-manifest.yaml  # ArgoCD application definition
├── deployment.yaml            # Deployment manifest for the weather webapp
├── service.yaml               # Service manifest for the weather webapp
└── kustomization.yaml         # Optional Kustomize configuration
```

## Getting Started

### Prerequisites

- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/)
- Access to a Kubernetes cluster

### Clone the Repository

```bash
git clone https://github.com/niv-devops/webapp-argocd.git
cd webapp-argocd
```

## Deployment with ArgoCD

To deploy the Weather Web App using ArgoCD, follow these steps:

1. **Create an ArgoCD Application**:
   In the ArgoCD UI, create a new application pointing to this repository and the path to the manifests.

2. **Sync the Application**:
   After creation, you can sync the application to deploy the resources defined in the manifests.

## Updating the Application

To update the web app's Docker image version:

1. **Modify the Image Version**:
   Edit the `deployment.yaml` file to specify the new image version.

2. **Commit Changes**:
   Commit your changes to the repository. ArgoCD will automatically detect changes and can sync them to the cluster.

```bash
git add deployment.yaml
git commit -m "Update image version to <new_version>"
git push origin main 
```
