# ITS - Modern DevOps Resources

## Introduction

This is a small document to help you get started with modern DevOps practices and generic advices.

## How to be a good engineer

- **Be curious**: Always be curious about how things work. Use *YouTube* and *Twitter* and follow people and projects.
- **Challenge yourself**: Build complex projects and solve complex problems.
- **Simplify**: Once you know how to build complex things, strive to simplify them.
- **Be nice**: Be nice to your colleagues, they are your best allies.
- **Be humble**: You don't know everything, and that's fine.
- **Exercise**: Take care of your body, it's the only one you have.

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

HOWEVER, if you are also fast, it's better. Here are some tools that can help you be faster:
- **Keyboard**: Minimize the use of the mouse, they keyboard is faster, and you can do more with it.
  - **Mechanical keyboard**
      - **Split keyboard**: It's better for your wrists
  - **Touch typing**: It's faster than looking at the keyboard
- **Linux**: It's faster than Windows if you know what you need to do
  - You can tailor it to your needs
  - Use tiling window managers like i3, Sway, Hyprland or PopOS
  - Distributions examples:
      - Debian, Ubuntu, PopOS: stable releases (release every 6 months)
      - ArchLinux: rolling release (release every day)
      - NixOS: the whole OS is defined in a single file with predictable results
  - [Arch Linux per Comuni Mortali (Udemy)](https://www.udemy.com/course/arch-linux-per-comuni-mortali/?couponCode=CBD4F77FEB3117AC599E)
- **The terminal**: It's faster than any GUI if you know what you need to do
  - `Oh my Posh`: themes, git info and more for bash and powershell
  - ZSH: A better shell, with autocompletion and more (Oh my ZSH)
- **Vim** motions (installable on any IDE)
  - [Vim motions YT playlist](https://www.youtube.com/watch?v=X6AR2RMB5tE&list=PLm323Lc7iSW_wuxqmKx_xxNtJC_hJbQ7R)
- **NeoVim** (When you mastered Vim motions). 
  - From IDE to PDE (Personal Development Environment), you can make it work exactly as you want.
  - [NeoVim Kickstart YT](https://www.youtube.com/watch?v=m8C0Cq9Uv9o)
- **Tmux** (Multiple terminal "windows" in one terminal)
  - [Tmux explained](https://youtu.be/niuOc02Rvrc?si=MOBA-YV9tC8yhN8z)

### YouTube channels

- [Primeagen](https://www.youtube.com/@ThePrimeagen): Generic programming tips, Vim, Tmux, and more
- [Theo](https://www.youtube.com/@t3dotgg): Javascript, React, Node, and more
- [MorroLinux](https://www.youtube.com/@morrolinux): Linux (ITA)
- [DevOps Toolbox](https://www.youtube.com/@devopstoolbox): Generic DevOps practices, Linux, development
- [typecraft](https://www.youtube.com/@typecraft_dev): Generic development practices
