"""
DevOps/SRE Agent - Site Reliability Engineer Expert

Expert en infrastructure et reliability:
- Kubernetes 1.30-1.32 orchestration
- GitOps: ArgoCD 2.10+, FluxCD 2.2+
- IaC: Terraform 1.7+, Pulumi 3.100+, OpenTofu
- CI/CD: GitHub Actions (OIDC), GitLab CI
- Observability: Prometheus, Grafana 11+, Loki, Tempo
- SRE Methodology: SLI/SLO/SLA, error budgets
- Security: Kyverno, OPA, Falco

Focus: Reliability-first, automation, SLO-driven development
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

class DevOpsSREAgent:
    """Agent expert DevOps/SRE"""

    def __init__(self, name: str, brain=None):
        self.name = name
        self.brain = brain
        self.running = False
        self.expertise_domains = [
            "kubernetes",
            "gitops",
            "terraform",
            "ci_cd",
            "observability",
            "sre_methodology",
            "security_policy"
        ]

        self.knowledge_base = {
            "kubernetes_perf": {
                "hpa_reaction": "15-30 seconds scale up",
                "node_autoscaling": "2-5 minutes new nodes",
                "pod_startup": "<30s with image cached",
                "resource_limits": "Always set requests+limits"
            },
            "gitops_2025": {
                "argocd": "UI-driven, canary/blue-green deploys, 3min sync",
                "fluxcd": "Pull-based, security-focused, GitOps Toolkit",
                "benefits": "Declarative, versioned, auto-reconciled, auditable"
            },
            "sre_framework": {
                "sli": "Service Level Indicator (raw metrics: latency, errors)",
                "slo": "Service Level Objective (internal targets: 99.9% uptime)",
                "sla": "Service Level Agreement (customer contracts)",
                "error_budget": "100% - SLO (if depleted -> freeze features)"
            },
            "observability_stack": {
                "metrics": "Prometheus (time-series, 2M series/node)",
                "logs": "Loki (log aggregation, LogQL)",
                "traces": "Tempo (distributed tracing)",
                "dashboards": "Grafana 11+ (AI anomaly detection)",
                "otel": "OpenTelemetry (unified instrumentation)"
            }
        }

    async def start(self):
        """Demarre l'agent DevOps/SRE"""
        self.running = True
        if self.brain:
            self.brain.working_memory[f"{self.name}_status"] = {
                "type": "agent_status",
                "agent": self.name,
                "status": "running",
                "expertise": self.expertise_domains,
                "timestamp": datetime.now().isoformat()
            }

    async def stop(self):
        """Arrete l'agent"""
        self.running = False

    async def design_k8s_infrastructure(self, requirements: Dict[str, Any]) -> str:
        """Conçoit une infrastructure Kubernetes production-grade"""

        app_name = requirements.get("app_name", "myapp")
        replicas = requirements.get("replicas", 3)
        slo_target = requirements.get("slo_uptime", 99.9)

        design = f"""
# Kubernetes Production Infrastructure

## Application: {app_name}
## Target SLO: {slo_target}% uptime

### 1. Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  namespace: production
  labels:
    app: {app_name}
spec:
  replicas: {replicas}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: myregistry/{app_name}:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 2. HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {app_name}-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {app_name}
  minReplicas: {replicas}
  maxReplicas: {replicas * 3}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 3. GitOps avec ArgoCD

```yaml
# argocd-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {app_name}
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/company/{app_name}
    targetRevision: main
    path: k8s/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### 4. SLI/SLO Definition

**SLI (Service Level Indicators)**:
- Availability: Successful requests / Total requests
- Latency: P95 response time < 200ms
- Error Rate: 4xx/5xx errors < 0.1%

**SLO (Service Level Objectives)**:
- Uptime: {slo_target}% ({(100 - slo_target) * 365 * 24 / 100:.1f}h downtime/year)
- P95 Latency: <200ms
- Error Rate: <0.1%

**Error Budget**: {100 - slo_target}% = {(100 - slo_target) * 365 * 24 / 100:.1f}h/year

### 5. Observability: Prometheus + Grafana

```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {app_name}
spec:
  selector:
    matchLabels:
      app: {app_name}
  endpoints:
  - port: metrics
    interval: 30s
```

**Key Metrics**:
- `http_requests_total` (counter)
- `http_request_duration_seconds` (histogram)
- `http_requests_in_progress` (gauge)

**Grafana Dashboard**:
- Request rate (QPS)
- Error rate (%)
- Latency P50/P95/P99
- Pod CPU/Memory usage
- HPA scaling events

### 6. CI/CD Pipeline (GitHub Actions)

```yaml
name: Deploy to Kubernetes
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # OIDC
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/GithubActionsRole
          aws-region: us-east-1

      - name: Build and push image
        run: |
          docker build -t $ECR_REGISTRY/{app_name}:$GITHUB_SHA .
          docker push $ECR_REGISTRY/{app_name}:$GITHUB_SHA

      - name: Update GitOps repo
        run: |
          # ArgoCD auto-sync will deploy
          git commit -m "Update image to $GITHUB_SHA"
          git push
```

### Performance Benchmarks
- HPA scale-up: 15-30 seconds
- Rolling update: ~2 min for {replicas} pods
- ArgoCD sync: ~3 minutes
- Image pull (cached): <10 seconds

### Security Checklist
- [ ] RBAC configured (least privilege)
- [ ] Network Policies (restrict pod-to-pod)
- [ ] Pod Security Standards (restricted)
- [ ] Image scanning (Trivy/Grype)
- [ ] Secrets management (Sealed Secrets / External Secrets)
- [ ] OIDC auth (no static secrets in CI/CD)
"""

        return design

    async def consult(self, query: str) -> str:
        """Consultation DevOps/SRE experte"""
        if not self.brain:
            return "DevOps/SRE: Brain not connected"

        context = f"""You are an Expert Site Reliability Engineer with deep knowledge of:

Infrastructure & Orchestration:
- Kubernetes 1.30-1.32 (HPA, node autoscaling, RBAC, network policies)
- GitOps: ArgoCD 2.10+ (canary/blue-green), FluxCD 2.2+
- IaC: Terraform 1.7+ (3000+ providers), Pulumi 3.100+ (Python/TS)
- CI/CD: GitHub Actions (OIDC, no secrets!), GitLab CI

Observability Stack 2025:
- Prometheus (metrics, 2M series/node)
- Grafana 11+ (AI anomaly detection, visualization)
- Loki (logs, LogQL)
- Tempo (distributed tracing)
- OpenTelemetry (unified instrumentation)

SRE Methodology:
- SLI/SLO/SLA framework
- Error budgets (100% - SLO)
- Incident response & blameless postmortems
- Toil reduction (automate repetitive tasks)

Security:
- Kyverno (policy enforcement)
- OPA (Open Policy Agent)
- Falco (runtime security)

Always provide:
1. Production-ready Kubernetes manifests
2. SLI/SLO definitions with error budgets
3. Observability setup (Prometheus/Grafana)
4. GitOps workflow
5. Performance benchmarks

User query: {query}

Provide detailed SRE-focused guidance."""

        response = await self.brain.think(context)

        if self.brain:
            self.brain.working_memory[f"devops_consult_{datetime.now().timestamp()}"] = {
                "type": "expert_consultation",
                "agent": self.name,
                "query": query,
                "response_preview": response[:200],
                "timestamp": datetime.now().isoformat()
            }

        return response
