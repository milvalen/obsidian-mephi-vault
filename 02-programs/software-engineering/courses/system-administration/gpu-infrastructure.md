---
title: "Optional GPU infrastructure: nvidia-smi, MIG and Kubernetes"
type: lecture
status: draft
program: software-engineering
course: System Administration
created: 2026-10-26
updated: 2026-10-26
---
# Optional GPU infrastructure: nvidia-smi, MIG and Kubernetes

[System Administration](system-administration.md) · [Logs and metrics](service-logs-and-metrics.md) · [RAID](raid-and-mdadm.md) · [LVM](lvm-and-filesystem-growth.md)

## Context and evidence

The owner supplied this demonstration section on 2026-10-26.
The material describes it as ungraded and as the last section of the course, in Module 4.
It refers to earlier Sections 1.2, 1.4, and 3.6. Its own section number is unknown.
The vault retains an English summary, not the original text.
No GPU host, command output, or student execution was supplied.

## GPU and CPU architecture

A CPU has a small number of powerful general-purpose cores.
These cores operate well on sequential logic, branches, and frequent task changes.
A GPU has many simpler execution units.
These units apply the same operation to different data at the same time.

Graphics rendering applies one formula to many pixels.
Model training and inference mostly use large matrix multiplication.
Both workloads divide into many independent parallel operations.
A CPU can do this work, but it does fewer of these operations at the same time.

Agent note: GPU "cores" are not equivalent to CPU cores. Do not compare core counts directly.

## Observation with nvidia-smi

`nvidia-smi` shows the state of each installed NVIDIA GPU.
It shows utilization, used and total GPU memory, temperature, and power.
It also lists processes that use the GPU and their GPU memory.
Its purpose is similar to `top` and `free -h` for CPU and RAM.

Use it to find whether a GPU does work, is idle, or holds memory for an old process.

Agent check against the [nvidia-smi documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html), 2026-10-26:
GPU utilization is the percentage of the sample period in which one or more kernels executed.
It is not the percentage of execution units in use.
A value of 100% can occur while much of the GPU capacity is unused.

## MIG: one GPU for several workloads

A data-center GPU can be more than one workload needs.
MIG (Multi-Instance GPU) divides one physical GPU into several isolated instances.
Each instance has dedicated compute and memory resources.

Agent check against the [NVIDIA MIG user guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/introduction.html), 2026-10-26:

- MIG is available starting with the NVIDIA Ampere architecture, for example A100.
- One GPU can have a maximum of seven GPU instances.
- Each instance has its own streaming multiprocessors, L2 cache banks, and memory paths.
- NVIDIA states fault isolation between clients such as VMs, containers, and processes.

The source compares MIG with CPU and memory sharing (Section 1.2) and with RAID and LVM (Module 3).
The common principle is the division of one physical resource between independent users.
Difference: MIG divides hardware units. CPU time sharing gives all processes the same cores in turns.
Not every NVIDIA GPU supports MIG. Check the supported product list before you plan for it.

## Kubernetes and GPU workloads

Large training and inference workloads can use many GPUs on many servers.
Kubernetes schedules containers on cluster nodes.
Its scheduler can also take GPU availability into account.

A device plugin on each GPU node advertises GPU resources to the cluster.
With MIG, the plugin can advertise MIG instances instead of whole GPUs.
A container declares the GPU quantity that it needs.
The scheduler puts the container only on a node with that resource free.

Agent check against [Kubernetes GPU scheduling](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/), 2026-10-26:
The node needs the vendor driver and the vendor device plugin.
The cluster then exposes a resource such as `nvidia.com/gpu`.
Specify GPUs in `limits`. If you also specify `requests`, the two values must be equal.

```yaml
resources:
  limits:
    nvidia.com/gpu: 1
```

This example is not executed. It shows the resource syntax only.

MIG and Kubernetes together let several inference workloads share one physical GPU.
This can decrease idle capacity of an expensive GPU.

## Recall and learning targets

Minimum: explain the CPU and GPU difference and why GPUs suit model training and inference.
Core: explain the `nvidia-smi` output and the purpose of MIG.
Advanced: explain how a device plugin lets Kubernetes put GPU workloads on nodes.
These are supplied learning targets, not verified student achievements.

1. Why does matrix multiplication suit a GPU?
2. Which `nvidia-smi` data shows a process that holds GPU memory?
3. Why does 100% GPU utilization not prove full use of the GPU?
4. How does MIG isolation differ from CPU time sharing?
5. Which component tells Kubernetes how many GPUs a node has?
6. Where do you specify a GPU quantity in a container specification?

## Verification limits

The agent read the linked official references on 2026-10-26.
The agent did not run `nvidia-smi`, configure MIG, or deploy a Kubernetes cluster.
The note remains a draft.

## Open questions

- Which failures, for example a full GPU reset, affect all MIG instances?
- Which MIG device-plugin strategy applies in a given cluster?
