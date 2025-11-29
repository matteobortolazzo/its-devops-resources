# ITS - AI & ML Resources

## Intro

AI/ML is not a single tool, it’s a **workflow**: data → model → evaluation → iteration → deployment → monitoring.

## What is a model

A model is a function that maps **inputs** to **outputs**.

- **Parameters**: learned "knobs" (weights) inside the model.
- **Training**: adjusting parameters using data (and a loss function).
- **Inference**: using a trained model to make predictions/outputs.
- **Generalization**: performing well on *new* data, not just training data.
- **Overfitting**: memorizing training data patterns that don’t transfer.

Common model families:
- **Classical ML**: trees, linear models, clustering, etc.
- **Neural networks**: deep learning models.
- **LLMs**: neural networks specialized for language (and more).

## LLMs and prompt engineering

**LLMs (Large Language Models)** generate text (and often code, images, or tool calls) by predicting the next token(s) given context.

Key concepts:
- **Tokens**: text is processed in chunks, not characters.
- **Context window**: the working memory for the current request.
- **System / developer / user instructions**: different "priority levels" of guidance.

Prompt engineering (practical):
- Be explicit about **goal**, **constraints**, and **format** (e.g., JSON output).
- Use **delimiters** for inputs to reduce mixing instructions with data.
- Provide **examples** (few-shot) when you need consistent structure.
- Ask for **checks**: "list assumptions", "flag missing info", "cite sources when using RAG".
- Prefer **tool use** (search, DB query, code) over "just guess".
- Defend against **prompt injection** when you include untrusted content.

## RAG (Retrieval-Augmented Generation)

RAG is generation of content where a context is injected from an external source (not only the model training).
Context can be added in the prompt upfront or via tools calls.

Typical pipeline:
- **Ingest** documents → **chunk** → **embed** → store in a **vector database**
- At query time: retrieve top-k chunks (often **hybrid** keyword + vector)
- Optionally **rerank**
- Provide retrieved context to the LLM and generate an answer (ideally with citations)

## MCP (Model Context Protocol)

**MCP** is a standard way for AI apps to connect to **tools** and **data sources** via a client/server protocol.

Mental model:
- **MCP Host**: the app running the LLM (chat app, IDE, agent runner)
- **MCP Client**: speaks the protocol
- **MCP Server(s)**: expose capabilities (tools/actions, resources, prompts)

Why it matters:
- Avoid "N models × M tools" custom integrations
- Standardizes how tools are discovered and invoked
- Encourages reusable "connectors" across apps and models

Security basics:
- Least privilege (expose only what’s needed)
- Allowlist tools and enforce argument validation
- Audit logs for tool calls + data access
- Treat retrieved text as untrusted input (prompt injection defenses)

Performance:
- Can be bad as MCP adds layers over tool callings

## Vectors, embeddings, and vector databases

### Vectors (the math object)

A **vector** is an ordered list of numbers (e.g., `[0.12, -0.03, 0.88, ...]`) that represents something in a space with **N dimensions**.

Key ideas:
- **Dimensions**: how many numbers are in the vector (e.g., 384, 768, 1536…).
- **Distance / similarity**: how "close" two vectors are.
    - **Cosine similarity**: compares angle (common for embeddings).
    - **Dot product**: similar vibe; often used when vectors are normalized.
    - **Euclidean distance**: straight-line distance (sometimes used, not always ideal).
- **Nearest neighbors**: "find the most similar items" = search for vectors that are closest.

Why vectors matter in ML:
- They let us do math on meaning: similar meaning → nearby vectors (in a good representation).

### Embeddings (vectors with meaning)

An **embedding** is a vector created by a model to represent the *meaning* of something:
- text (sentence, paragraph, document)
- image
- audio
- code
- even structured records (with the right model)

Common use-cases:
- **Semantic search**: search by meaning, not keywords.
- **Clustering**: group similar items.
- **Deduplication**: detect near-duplicates.
- **Recommendations**: "users/items like this".
- **RAG retrieval**: fetch relevant chunks before prompting the LLM.

Practical notes:
- **Embedding model choice matters** (domain + language + cost + latency).
- **Chunking** is part of embedding quality:
    - Too small → loses context
    - Too big → mixes topics and retrieval gets noisy
- Store **metadata** with embeddings:
    - documentId, tenantId, permissions, timestamps, source URL, chunk index, etc.
- Use **normalization** consistently if your similarity metric expects it.

### Vector databases (fast similarity search)

A **vector database** (or "vector index") stores embeddings and supports efficient **nearest-neighbor search**.

What it typically provides:
- **Upsert**: store vectors + metadata (and sometimes raw text)
- **Similarity search**: top-k most similar vectors to a query vector
- **Filtering**: restrict by metadata (tenant, date, type, permissions)
- **Indexing for speed**: approximate nearest neighbor (ANN) algorithms

Important internal concept:
- **ANN (Approximate Nearest Neighbor)**: faster searches with a small tradeoff in accuracy.
    - Typical goal: "good enough top-k" very quickly.

Common patterns:
- **Hybrid search**: combine keyword (BM25) + vector similarity (best of both worlds).
- **Reranking**: first retrieve candidates, then rerank with a stronger model (cross-encoder / LLM).
- **Namespace / partitioning**: separate data per customer/tenant for safety and performance.

## Semantic Kernel (SK)

[Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/overview/) is a lightweight SDK that helps you build **AI-powered apps/agents** by orchestrating:
- Model calls (OpenAI / Azure OpenAI / others)
- Plugins / functions (your tools)
- Prompt templates
- Memory connectors (including RAG patterns)
- Agent-like flows (planning / orchestration depending on approach)

## Machine Learning

Machine Learning (ML) is the practice of building systems that "learn" patterns from data to make predictions or decisions, instead of being explicitly programmed with rules.

A useful mental model:
- You choose a **model** (a function with parameters)
- You define a **goal** as a measurable score
- You use data to adjust the model’s parameters so it performs better on that score

### Core concepts

- **Training data / validation data / test data**
  - **Training**: used to learn parameters
  - **Validation**: used to tune choices (model type, hyperparameters)
  - **Test**: final check; should not influence decisions

- **Features**
  - The input signals the model uses (columns, pixel values, tokens, etc.)

- **Labels (targets)**
  - The "correct answer" for supervised learning (class or numeric value)

- **Loss function**
  - A function that measures "how wrong" the model is.
  - Training tries to **minimize loss**.
  - Examples:
    - **MSE (Mean Squared Error)** for regression
    - **Cross-entropy** for classification

- **Optimization**
  - The procedure that updates model parameters to reduce loss (e.g., gradient descent).

- **Hyperparameters**
  - Settings you choose that are not learned directly (learning rate, tree depth, number of layers, regularization strength).

- **Overfitting vs generalization**
  - **Overfitting**: does great on training data, fails on new data
  - **Generalization**: performs well on unseen data (the real goal)

### Main categories of ML problems

**Supervised learning** (labeled data):
- **Classification** (spam/not spam)
- **Regression** (price prediction)

**Unsupervised learning** (no labels):
- **Clustering** (group customers)
- **Dimensionality reduction** (compress/visualize)
- **Anomaly detection** (detect weird behavior)

**Semi-supervised / self-supervised learning**:
- Uses lots of unlabeled data plus structure/objectives (common in modern deep learning and LLM pretraining)

**Reinforcement learning**:
- Learn actions via rewards (policies, agents)

## ML.NET

[ML.NET](https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet) is the .NET ecosystem’s framework for adding machine learning to applications.

Typical workflow:
- Load data (IDataView)
- Build a pipeline: transforms** → trainer
- Evaluate metrics
- Save the model
- Run inference in your app/service

Helpful tooling:
- AutoML for automatic multi-model evaluations
- CLI tooling

## Reinforcement Learning (RL)

**Reinforcement Learning** is a paradigm where an **agent** learns to make decisions by interacting with an **environment**, receiving **rewards** or **penalties** for its actions, and aiming to maximize cumulative reward over time.

### Core concepts

- **Agent**: the learner/decision-maker
- **Environment**: the world the agent interacts with
- **State (s)**: the current situation the agent observes
- **Action (a)**: what the agent can do
- **Reward (r)**: feedback signal (positive or negative)
- **Policy (π)**: the strategy mapping states to actions
- **Value function (V)**: expected cumulative reward from a state
- **Q-function (Q)**: expected cumulative reward from a state-action pair

### The RL loop

1. Agent observes **state** from environment
2. Agent takes **action** according to its policy
3. Environment returns **reward** and next **state**
4. Agent updates its policy/value estimates based on the reward signal
5. Repeat until episode ends or convergence

### Common applications

- Game AI (Atari, Go, game playing)
- Robotics (control, manipulation)
- Autonomous systems (navigation, resource allocation)
- Recommendation systems (sequential decision-making)

## Neural Networks

A **neural network** is basically a **configurable calculator**: you feed numbers in, it runs them through a bunch of simple math steps, and it outputs numbers.

The "magic" is that it can **learn the settings** of that calculator from examples.

### The simple picture

Think of a network as layers stacked like this:

**input → layer → layer → layer → output**

Each layer does:
1. **mix** the inputs (weighted sums)
2. pass them through a **non-linearity** (activation) so the model can learn complex patterns

### Neurons (one tiny unit)

A single neuron is:

`output = activation(w1*x1 + w2*x2 + ... + b)`

- `w` = weights (how much we care about each input)
- `b` = bias (a baseline offset)
- `activation` = a squish/curve (e.g., ReLU) that makes the network more than "just a line"

### How learning works (training)

Training is "turning the knobs" (weights) to reduce mistakes:

1. Make a prediction
2. Compute **loss** (how wrong it was)
3. Update weights to reduce loss

Most modern training uses:
- **Backpropagation**: efficiently computes how each weight contributed to the error
- **Optimizers**: the rule for updating weights (e.g., **SGD**, **Adam**)

## Neuroevolution (evolving neural networks)

Instead of training with gradients/backprop, **neuroevolution** uses **evolutionary algorithms**:
- create many candidate networks
- test them ("fitness")
- keep the best
- mutate/crossover to produce new networks
- repeat

### Why do this?

Neuroevolution is useful when:
- you don’t have a clean differentiable loss function
- the environment is noisy or reward-based (games, robotics)
- you want to evolve **architecture** and weights (not just weights)

### Basic loop (intuition)

1. Start with a population of random networks
2. Run each one on a task and assign a **fitness score**
3. Select the top performers
4. Create the next generation by:
   - **mutation**: slightly change weights (or structure)
   - **crossover**: combine parts of two "parents" (optional)
5. Iterate until good enough

## PyTorch

PyTorch is a popular deep learning framework.

Core concepts:
- **Tensor** (multi-dimensional array)
- **Autograd** (automatic differentiation)
- **nn.Module** (model building blocks)
- **Optimizers** (Adam, SGD)
- **DataLoader** (batching and shuffling)

Typical loop:
- forward pass → loss → backward() → optimizer.step()

Where it’s used:
- Research/prototyping
- Training custom neural networks
- Powering many LLM and vision stacks 
