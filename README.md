# ITS - DevOps & AI Resources

## Introduction

This is a small document to help you get started with modern DevOps and AI practices and generic advices.

## Resources

- [DevOps Resources](./DEVOPS.md): A document on discussed DevOps topics (Git, Actions, Docker, K8S, Deployments).
- [AI & ML Resources](./AI_ML.md): A document on discussed AI & ML topics (Models, LLMs, ML.NET, Neural networks).

## Projects

### 2025
- [JParser](./projects/2025/jparser): A Node.js library for parsing and manipulating JSON data with advanced features.
- [PokeBattle](./projects/2025/pokebattle): API and UI in docker with example GitHub actions workflows and ML.NET examples.

### 2024

- [ITS SQL](./projects/2024/its-sql): A distributed No-SQL database engine similar to Cosmos DB with SQL-like query language.

### 2023

- [GitMess](./projects/2023/gitmess): A GitHub backend clone running in Docker for managing repositories.

## How to be a good engineer

- **Be curious**: Always be curious about how things work. Use *YouTube* (examples later), *Reddit*, *X*; follow people and projects.
- **Challenge yourself**: Build complex projects and solve complex problems.
- **Simplify**: Once you know how to build complex things, strive to simplify them.
    - Don't use the latest technology just because it's new. Use it because it's better.
    - You don't need NoSQL, Microservices, or Kubernetes if you don't have a problem that needs them.
    - [YouTube - Microservices](https://youtu.be/y8OnoxKotPQ?si=HBQx4jfZYX32jQNg)
- **Work iteratively**: Don't try to build everything at once. Build small parts and iterate on them.
- **Security**: Always think about security. Data leaks and downtime are expensive, very expensive.
- **Documentation**: Document your code, your projects, your decisions. It will help you and your team.
    - Code sometimes can self-document, but it's not always the case.
    - [YouTube - Don't write comments](https://youtu.be/Bf7vDBBOBUA?si=IV2hkPYpUwFZ3YOk)
- **Tooling**:
    - There's no perfect language, framework, or tool. Use the right tool for the job and skill-set.

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

HOWEVER, if you are also fast, it's better. If you are fast you won't experience those micro context switches that slow you down, and you can just type as the speed of thought.

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

- [Salvatore Sanfilippo](https://www.youtube.com/@antirez): AI, C, general discussion
- [MorroLinux](https://www.youtube.com/@morrolinux): Linux (ITA)
- [Matthew Coder](https://www.youtube.com/@MatthewCoder): Game DEV (ITA)
- [typecraft](https://www.youtube.com/@typecraft_dev): Generic development practices
- [DevOps Toolbox](https://www.youtube.com/@devopstoolbox): Generic DevOps practices, Linux, development
- [Primeagen](https://www.youtube.com/@ThePrimeagen): Generic programming tips, Vim, Tmux, and more
- YouTube will suggest you more channels based on your interests

### Generic advices

- **Take care of yourself**
    - Exercise and eat well, it's the only body you have.
    - **Good chair**: You will spend a lot of time on it.
    - **Standing desk**: It's better for your back.
    - **Alice/Split keyboard**: It's better for your wrists
- **Fight Scrum**: Agile is great, Scrum is not.
    - Don't spend all your time in meetings.
    - [YouTube - The Agile Paradoxon](https://youtu.be/Bez7wmAsxjE?si=pJVrgVTJ8qCUoPKs)
    - [YouTube - The Expert](https://youtu.be/BKorP55Aqvg?si=ryEfSgHU253hyVkK)
- [YouTube - La AI penalizza le assunzioni dei programmatori junior a favore dei senior?](https://youtu.be/dBt5u19GpKc?si=SdcMP17-O6AvejZZ)
- [YouTube - Quello da non fare mai quando si programma con l'AI](https://youtu.be/cc86dChauDE?si=tqc7paXyFZh0wi-A)