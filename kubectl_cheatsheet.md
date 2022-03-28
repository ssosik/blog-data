---
title: kubectl cheatsheet
description: ""
lead: ""
date: "2021-11-23T11:23:25-05:00"
lastmod: "2021-11-23T11:23:25-05:00"
tags:
  - kubernetes
  - k8s
  - kubectl
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

[Official Cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

[k9s](https://k9scli.io/)

# ${HOME}/.kube/config

From the Rancher UI select the cluster, then ->
Cluster then hit the Kubeconfig File link. Save that to ~/.kube/config.
Remove the `certificate-authority-data` and add `insecure-skip-tls-verify: true`
to disable verifying the servers cert.

## Following some of the K8s docs

- https://kubernetes.io/docs/tasks/manage-kubernetes-objects/imperative-command/
- https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/
- https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
- https://kubernetes.io/docs/reference/kubernetes-api/

# Basics

Get all pods

    kubectl get po
    kubectl get po -A

## Create a deployment

    kubectl create deployment nginx --image nginx

## Delete a deployment

    kubectl delete deployment nginx

## List namespaces

    kubectl get namespace

## List All Objects within and without namespaces

    # In a namespace
    kubectl api-resources --namespaced=true
    
    # Not in a namespace
    kubectl api-resources --namespaced=false

## Forward local port into a specific container

```bash
kubectl port-forward --namespace cattle-monitoring-system  9090:9090
```

## List directory in a container

```bash
kubectl exec --stdin --tty sleep-74f674fb96-8pkk4 --namespace test123 -- /bin/ls -latrH /var/run/secrets/..data
```

## Follow logs for a container

```bash
kubectl logs --namespace csi-provider-kmi --timestamps=true -f -l app=secrets-store-csi-driver-provider-kmi
```
