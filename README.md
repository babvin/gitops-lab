# GitOps Repository Layout

This repository is intended to be pushed to its own GitHub repository (configured via `GITHUB_OWNER` and `GITHUB_REPO`). It serves as the GitOps source for the Cloud Native Lab and demonstrates GitOps workflows using **Argo CD** and **Flux**.

> **Current Status**
>
> * ✅ k3d-based Kubernetes cluster
> * ✅ Argo CD GitOps working
> * ✅ Sample NGINX application deployed
> * ✅ Sample FastAPI application deployed
> * 🚧 Flux integration will be re-enabled after the Argo CD workflow is finalized

---

## Repository Structure

```text
gitops-lab/
├── apps/
│   ├── argocd-managed/
│   │   ├── sample-nginx/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   ├── ingress.yaml
│   │   │   └── kustomization.yaml
│   │   │
│   │   ├── sample-fastapi/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   ├── ingress.yaml
│   │   │   └── kustomization.yaml
│   │   │
│   │   └── kustomization.yaml
│   │
│   └── flux-managed/
│       └── (reserved for Flux examples)
│
├── clusters/
│   └── local/
│       ├── argocd/
│       │   └── app-of-apps.yaml
│       └── flux-system/
│           └── (created by Flux bootstrap)
│
└── README.md
```

---

# GitOps Strategy

The repository is intentionally divided into separate areas for each GitOps engine.

## Argo CD

Argo CD watches:

```text
apps/argocd-managed/
```

The root application (`app-of-apps.yaml`) currently points to:

```text
apps/argocd-managed
```

Argo CD automatically detects the Kustomize application and deploys every workload defined in the parent `kustomization.yaml`.

Current applications:

* Sample NGINX
* Sample FastAPI

---

## Flux

Flux examples will live under:

```text
apps/flux-managed/
```

Flux will reconcile only this directory.

This separation allows both GitOps engines to coexist without managing the same Kubernetes resources.

---

# Why Separate Directories?

Argo CD and Flux both continuously reconcile Kubernetes resources.

To avoid conflicts:

* Argo CD manages only `apps/argocd-managed`
* Flux manages only `apps/flux-managed`

Each GitOps engine owns its own subtree of the repository.

This mirrors how multiple GitOps environments can coexist during evaluation or migration while keeping ownership boundaries clear.

---

# Local Development Workflow

## 1. Build the Toolbox

```bash
make build
```

---

## 2. Start the Development Environment

```bash
make up
```

---

## 3. Open the Toolbox

```bash
make shell
```

---

## 4. Create the Kubernetes Cluster

```bash
make k3d-start
```

Verify:

```bash
kubectl get nodes
```

---

## 5. Install Argo CD

```bash
make argocd-install
```

---

## 6. Register the Git Repository

```bash
argocd repo add https://github.com/<owner>/<repo>.git
```

Verify:

```bash
argocd repo list
```

Expected:

```text
STATUS: Successful
```

---

## 7. Deploy the Root Application

```bash
kubectl apply -f clusters/local/argocd/app-of-apps.yaml
```

---

## 8. Verify Synchronization

```bash
argocd app list
```

```bash
argocd app get app-of-apps
```

Expected:

```text
Sync Status: Synced
Health: Healthy
```

---

## 9. Verify Applications

```bash
kubectl get pods -A
```

Expected:

* sample-nginx
* sample-fastapi

---

# Accessing the Applications

Both applications are exposed through Traefik Ingress.

Example hosts:

```text
nginx.cnlab.local
fastapi.cnlab.local
```

Add to your local `/etc/hosts`:

```text
127.0.0.1 nginx.cnlab.local
127.0.0.1 fastapi.cnlab.local
```

Then browse to:

```text
http://nginx.cnlab.local
http://fastapi.cnlab.local
```

Alternatively, use port forwarding during development:

```bash
kubectl port-forward svc/sample-nginx 8080:80 -n argocd
```

```text
http://localhost:8080
```

```bash
kubectl port-forward svc/sample-fastapi 8081:80 -n argocd
```

```text
http://localhost:8081
```

---

# Current Demonstration

The repository currently demonstrates:

* k3d local Kubernetes cluster
* GitOps using Argo CD
* Kustomize-based application deployment
* Automatic reconciliation
* Multi-application deployment
* NGINX web application
* FastAPI REST application

---

# Roadmap

Planned additions include:

* Flux GitOps integration
* Harbor
* cert-manager
* External Secrets
* Prometheus
* Grafana
* Loki
* Tempo
* OpenTelemetry
* Istio
* Kyverno
* AI Platform
* Agent Marketplace
* Governance
* Analytics
* FinOps
* GreenOps

The long-term objective is to evolve this repository into a complete **Cloud Native Platform Engineering Lab**, demonstrating enterprise GitOps, Kubernetes platform engineering, observability, security, and AI workloads in a reproducible local environment.
