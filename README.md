# ITS - Modern DevOps Resources

## Introduction

This is a small document to help you get started with modern DevOps practices and generic advices.

## How to be a good engineer

- **Be curious**: Always be curious about how things work. Use *YouTube* and *Twitter* and follow people and projects.
- **Challenge yourself**: Build complex projects and solve complex problems.
- **Simplify**: Once you know how to build complex things, strive to simplify them.
  - Don't use the latest technology just because it's new. Use it because it's better.
  - You don't need NoSQL, Microservices, or Kubernetes if you don't have a problem that needs them.
  - [YouTube - Microservices](https://youtu.be/y8OnoxKotPQ?si=HBQx4jfZYX32jQNg)
- **Work iteratively**: Don't try to build everything at once. Build small parts and iterate on them.
- **Security**: Always think about security. Data leaks and downtime are expesive, very.
- **Documentation**: Document your code, your projects, your decisions. It will help you and your team.
  - Code sometimes can self-document, but it's not always the case.
  - [YouTube - Don't write comments](https://youtu.be/Bf7vDBBOBUA?si=IV2hkPYpUwFZ3YOk)
- **Be nice**:
  - Your colleques are your best allies.
  - Be humble, you don't know everything, but still tell your opinion.
  - There's no perfect language, framework, or tool. Use the right tool for the job and skillset.

### Example projects

- **Write a language**: It's not magic, someone wrote it. Same goes for IDEs, with custom highlights and autocompletion. This also include frameworks like Angular or Svelte.
    - Write the compiler
    - Write the VS Code plugin for syntax highlighting
    - Write the VS Code plugin for autocompletion (*LSP* - Language Server Protocol)
- **Write a database**: Again, you can do a simple implementation of a DB like Cosmos
    - Think about the data structure
    - Write the storage engine
    - Write the query engine
    - Add indexing
- **Write a web server**: You can write a simple web server like *Express*, or *ASP.NET*. They are "just" libraries on top of *Node* and *.NET*. You can also write a simple version of Kestrel.
    - Write the HTTP parser
    - Write the routing engine
    - Write the middleware engine
- **Write an ORM**: You can write a simple ORM like *Entity Framework* or *TypeORM*. They are just libraries to write on SQL.
    - Write the query builder
    - Write the change tracker
    - Write the migration engine
- **Write a CI/CD pipeline**: You can write a simple version of GitHub Actions, or *Azure DevOps*. They are just scripts that run on a server.
- **Write a container engine**: You can write a simple version of Docker. It's just a process running in a namespace.
- **Write version control like Git**: It's just a graph of commits. You can write a simple version of it.

### Tools

Be a good engineer doesn't mean to be fast. Your brain is more important than your hands.

HOWEVER, if you are also fast, it's better. If you are fast you won't experience those micro context switches that slow you down and you can just type as the speed of thought.

Here are some tools that can help you be faster:
- **Keyboard**: Minimize the use of the mouse, they keyboard is faster, and you can do more with it.
  - **Mechanical keyboards**: They are more comfortable and better feedback [Great price/quality](https://www.keychron.com/)
  - **Touch typing**: It's faster than looking at the keyboard
- **Linux**: It's faster than Windows if you know what you need to do (or MacOS at least)
  - You can tailor it to your needs
  - Use tiling window managers like i3, Sway, Hyprland or PopOS
  - Distributions examples:
      - Debian, Ubuntu, PopOS: stable releases (release every 6 months)
      - ArchLinux: rolling release (release every day)
      - NixOS: the whole OS is defined in a single file with predictable results
  - [Udemy - Arch Linux per Comuni Mortali (Udemy)](https://www.udemy.com/course/arch-linux-per-comuni-mortali/?couponCode=CBD4F77FEB3117AC599E)
- **The terminal**: It's faster than any GUI if you know what you need to do
  - *oh-my-posh*: themes, *Git* info and more for *Bash* and *Powershell*
  - *zsh*: A better shell, with autocompletion and more (Oh my ZSH)
- **Shortcuts**: Learn the shortcuts of your IDE, OS and tools they are faster than the mouse
- **Vim** motions (installable on any IDE)
  - You will be able to edit text much faster in any IDE
  - It is frustrating at the beginning, but it's worth it. Start with just a few motions
  - [YouTube - Vim motions playlist](https://www.youtube.com/watch?v=X6AR2RMB5tE&list=PLm323Lc7iSW_wuxqmKx_xxNtJC_hJbQ7R)
- **NeoVim** (When you mastered Vim motions)
  - From IDE to PDE (Personal Development Environment), you can make it work exactly as you want.
  - [YouTube - NeoVim Kickstart](https://www.youtube.com/watch?v=m8C0Cq9Uv9o)
  > This is not perfect for every situation, it can replate easily VS Code, but not IntelliJ or Visual Studio for specific workflows.
- **Tmux** (Multiple terminal "windows" in one terminal)
  - You can have multiple terminals in one terminal, create sessions, windows, panels, and more.
  - [YouTube - Tmux explained](https://youtu.be/niuOc02Rvrc?si=MOBA-YV9tC8yhN8z)

### YouTube channels

- [Primeagen](https://www.youtube.com/@ThePrimeagen): Generic programming tips, Vim, Tmux, and more
- [Theo](https://www.youtube.com/@t3dotgg): Javascript, React, Node, and more
- [MorroLinux](https://www.youtube.com/@morrolinux): Linux (ITA)
- [DevOps Toolbox](https://www.youtube.com/@devopstoolbox): Generic DevOps practices, Linux, development
- [typecraft](https://www.youtube.com/@typecraft_dev): Generic development practices
- YouTube will suggest you more channels based on your interests

### Generic advices

- **Take care of your body** 
  - Exercise and eat well, it's the only body you have.
  - **Good chair**: You will spend a lot of time on it.
  - **Standing desk**: It's better for your back. 
  - **Alice/Split keyboard**: It's better for your wrists
- **Fight Scrum**: Agile is great, Scrum is not. 
  - Scrum is a tool, not a goal. 
  - Scrum is not the only way to be Agile.
  - Scrum is not the only way to be productive.
  - Don't spend all your time in meetings.
  - Run away from [SAFe](https://scaledagileframework.com/)
  - [YouTube - The Agile Paradoxon](https://youtu.be/Bez7wmAsxjE?si=pJVrgVTJ8qCUoPKs)
  - [YouTube - The Expert](https://youtu.be/BKorP55Aqvg?si=ryEfSgHU253hyVkK)
- **Challenge the status quo.**

## DevOps

DevOps is not a tool, it's a mindset. It's about breaking the silos between development and operations.

Here's a few concepts of DevOps. For actual guide check the official documentation of each tool, YouTube and blogs.

A DevOps team should not be a team that does everything, but a team that helps other teams to do everything.

[YouTube - DevOps is Terrible](https://youtu.be/qVEEpUvl0Kw?si=L_midxVRkJUN2JjX)

### Git

Git is a **distributed** version control system. It's the most used version control system in the world.

#### Concepts

- Branching
- Merge, Fast Forward, Rebase
- Squash
- Cherry-pick
- Stash
- Tag
- Amend (change the last commit)
- Bisect (find the commit that broke the code)
- Hooks (pre-commit, pre-push, post-commit, post-push)

- Pull request
- Code review
- Pair programming
- Fork

#### Services
- **GitHub**
- **Azure Repos**
- **GitLab**
- **BitBucket**

### CI/CD

CI/CD is the practice of automating the integration and deployment of code to production.

- **CI**: Continuous Integration
- **CD**: Continuous Deployment

#### Pipelines 

Usually in CI/CD we use pipeline. Pipeline are a series of steps that are executed in order (or in parallel) after a trigger.

They can be used to:
- Build the code
- Lint the code 
- Test the code (TDD, BDD)
  - Unit tests [YouTube - Why I Don't Unit Test](https://youtu.be/ZGKGb109-I4?si=FQ41FGUuwLVZyht_)
  - Mutation Tests
  - Integration Tests
  - End-to-End tests
  - Smoke Tests
  - Performance Tests
  - Regression Tests
  - Code Coverage ([YouTube - You should NOT focus on Code Coverage](https://youtu.be/WxoSoxVgyUw?si=nS73DZmbcw7SS5xx))
- Check vulnerabilities
- Check code quality
- Check outdated dependencies
- Version the code (SemVer, standard version)
- Tag the code
- Generate the documentation
- Package the code (Nuget, NPM, Docker, etc)
- Deploy the code
- Notify the team
- Anything else you can think of

#### Tools

- **GitHub Actions**
- **Azure Pipelines**
- **Jenkins**

### Deployment Techniques

APIs/UIs:
- **Blue-Green Deployment**: Deploy a new version of the code in a new environment*, and switch the traffic when it's ready.
  - It can be a new server, a new container, a new region, etc.
  - It can be done with DNS, Load Balancer, or a Proxy.
- **Canary Deployment**: Deploy a new version of the code to a subset of users, and increase the traffic when it's ready.
- **A/B Testing**: Deploy a new version of the code to a subset of users, and compare the results with the old version.
- **Rolling Deployment**: Deploy a new version of the code to a subset of servers, and increase the traffic when it's ready.
- **Feature Flags**: Deploy a new version of the code to all users, but enable the new features only for a subset of users.
- **Dark Launch**: Deploy a new version of the code to all users, but don't enable the new features yet.

Packages:
- **Nightly Build**: Deploy a new version of the code every nighty
  - Not all test can be done on every commit. Nightly builds are useful to run long tests.

Chaos Engineering:
- Invented by Netflix, it's the practice of introducing chaos in the system to test its resilience. 
- Introduces latency, errors, and other issues to see how the system reacts.
- It can kill servers, introduce network issues, etc.
- It can be done with tools like Gremlin, or manually.

### Docker 

Docker is a tool to create, deploy, and run applications by using containers.
Containers are made by isolating a process in a namespace, and adding a filesystem on top of it.
They have layers, and they can be shared and reused.
They are faster than VMs, and they are more portable.
They just share the kernel with the host.

#### Concepts

- **Image**: A read-only template with instructions for creating a Docker container
- **Container**: A runnable instance of an image
- **Volume**: A way to persist data
- **Network**: A way to connect containers
- **Dockerfile**: A file with instructions to create an image
- **Docker Composer**: A way to define and run multi-container Docker applications
- **Registry**: A place to store and share images (Docker Hub, Azure Container Registry, GitHub Container Registry)
- **ENV**: A way to pass environment variables to the container

### Infrastructure as Code

Infrastructure as Code is the practice of managing infrastructure using code.
Instead of clicking on buttons in a GUI or running commands in a terminal, you write code that defines your infrastructure.

On Azure we can use *ARM* templates or *Bicep*, on *AWS* we can use *CloudFormation*, on *Google Cloud* we can use *Deployment Manager*.
More generic tools are *Terraform* and *Pulumi*.

*Bicep* example:

```bicep
resource name_resource 'Microsoft.Web/staticSites@2021-01-15' = {
  name: name
  location: location
  tags: resourceTags
  properties: {
    repositoryUrl: repositoryUrl
    branch: branch
    repositoryToken: repositoryToken
    buildProperties: {
      appLocation: appLocation
      apiLocation: apiLocation
      appArtifactLocation: appArtifactLocation
    }
  }
  sku: {
    tier: sku
    name: skucode
  }
}resource name_appsettings 'Microsoft.Web/staticSites/config@2021-01-15' = {
  parent: name_resource
  name: 'appsettings'
  properties: appSettings
}
```

With the code above we can create a static website on Azure. The result is reproducible and can be versioned. A second parameter file can be used to change the values.

### Monitoring and Alerting

- **Monitoring**: is the practice of observing the system to check its health and performance.
- **Alerting**: is the practice of sending notifications when something goes wrong.

Ideally, you need to find the problem before the user does.

Log things like:
- Errors
- Warnings
- Request timing
- Dependencies timing

Create queries on logs to:
- Find errors
- Find slow requests
- Find the most used features
- Create dashboards
- Create alerts
- Create reports

You can use tools like *Prometheus*, *Grafana*, *Azure Monitor*, *AWS CloudWatch* to create dashboards and alerts.

#### Resource
- [OpenTelemetry](https://opentelemetry.io/): A standard for collecting telemetry data
- [Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/overview)
  - [Alerts](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview)
  - [Dashboard](https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/tutorial-logs-dashboards)
- [Analyze anomalies with KQL](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/kql-machine-learning-azure-monitor)

## Azure App Security

Security must be considered from the beginning. It's not something you can add later. A security breach can be very expensive or even fatal for a company.

## Azure KeyVault

**NEVER STORE KEYS IN THE REPOSITORY**

Azure KeyVault is a way to store secrets, certificates, and keys. It's a secure way to store sensitive information.

For example:
- Connection strings
- API keys
- Signing Certificates
- SSH keys

> Remember secrets should be rotated, and they should have a limited scope.

## Azure Entra ID

It's a way to manage access to resources. Both users and services can have an identity. It was called *Azure Active Directory* before.

If a service like a WebApp needs to access a database, it can use its identity to authenticate instead of a connection string. It is more secure and easier to manage.

### Concepts

- **Managed Identity**: A way to identify a user or a service. [List of available services](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/managed-identities-status)
- **Role-based access control (RBAC)**: A way to manage access to resources based on roles. [What is RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview)
- **Azure Policy**: A way to enforce rules and standards on resources. [What is Azure Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview)
- [Using Managed Service Identity (MSI) to authenticate on Azure SQL DB](https://techcommunity.microsoft.com/t5/azure-database-support-blog/using-managed-service-identity-msi-to-authenticate-on-azure-sql/ba-p/1288248)

## Kubernetes

It's a container orchestration platform. It's used to deploy, scale, and manage containers. It let us abstract the distribution of the containers, failover, scaling, and more.

It works well with Microservices, but it's not the only way to do it.

Everything is defined in a YAML file, and it's declarative. Most concepts are similar to [Docker Compose](https://docs.docker.com/compose/), but they are more complex.

> Most companies don't need Kubernetes, but it's a good tool to know.

### Basic Concepts

- **Node**: A server that runs containers
- **Cluster**: A set of nodes that run containerized applications
- **Pod**: A group of one or more containers, smallest deployable unit
- **Service**: A way to abstract a set of pods, load balance them, and more
- **Deployment**: A way to deploy a pod, and manage its replicas
- **Ingress**: A way to expose a service to the outside world. It can be used to route traffic, add SSL, and more
- **Namespace**: A way to isolate resources, used to separate environments or tenants
- **ConfigMap**: A way to store configuration
- **Secret**: A way to store sensitive information
- **Volume**: A way to persist data

### Example

[Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

## Helm

Helm is a package manager for *Kubernetes*. It's used to define, install, and upgrade *Kubernetes* applications.

It's like *Nuget* or *NPM* for Kubernetes.

### Concepts

- **Chart**: A package of pre-configured Kubernetes resources
- **Repository**: A place to store and share charts
- **Release**: A specific version of a chart
- **Values**: A way to customize a chart
