# GitOps repo layout

This directory is meant to be pushed to its own GitHub repo (the one named
in `.env` as `GITHUB_REPO`) so both ArgoCD and Flux can reconcile from it.

```
gitops/
├── clusters/
│   └── minikube/
│       ├── argocd/            # ArgoCD's own bootstrap objects
│       │   └── app-of-apps.yaml
│       └── flux-system/       # populated by `flux bootstrap` -- do not hand-edit
│           └── apps-source.yaml
└── apps/
    ├── argocd-managed/        # ArgoCD watches this path only
    │   └── sample-nginx/
    └── flux-managed/          # Flux watches this path only
        └── sample-nginx/
```

## Why two engines can coexist safely

ArgoCD and Flux are both reconciling the *same cluster*, so the rule that
keeps them from fighting is simple: **each engine is only ever pointed at
its own subtree of `apps/`, and each deploys into its own namespace**
(`argocd-managed-apps` vs `flux-managed-apps`). Neither tool is aware the
other exists, and neither needs to be -- this is purely a learning
convention, not something you'd run this way in production (in practice
you'd pick one GitOps engine per cluster).

## Bringing it up

1. `make minikube-start`
2. `make argocd-install` -- installs ArgoCD, then apply
   `clusters/minikube/argocd/app-of-apps.yaml` to start syncing
   `apps/argocd-managed/`
3. `make flux-bootstrap` -- installs Flux directly into this repo's
   `clusters/minikube/flux-system/` path, then commit + push
   `clusters/minikube/flux-system/apps-source.yaml` to start syncing
   `apps/flux-managed/`
4. `kubectl get pods -n argocd-managed-apps -n flux-managed-apps`
   -- both sample nginx deployments should be running, reconciled by two
   different engines, from two different subtrees of the same repo.
