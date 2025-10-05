<div align="center">

# Sisyphus

### *An intelligent agent system for tackling complex problems*

<img src="asset/sisyphus.png" alt="Sisyphus" width="300">

---

</div>

## Overview

Sisyphus is an intelligent agent system designed to help solve problems expressed in natural human language. It employs a sophisticated approach:

- **Simple Problems**: Processed directly for immediate solutions
- **Complex Problems**: Automatically decomposed into manageable, actionable tasks and executed step-by-step

## Installation

> **Note**: Conda installation is highly recommended for optimal environment management.

### Prerequisites

- Python 3.12 or higher
- Conda (recommended) or pip
- Git

### Setup Instructions

#### 1. Environment Setup

Create and activate a dedicated conda environment:

```bash
conda create -n sisyphus python=3.12
conda activate sisyphus
```

#### 2. Repository Clone

```bash
git clone https://github.com/theo1893/sisyphus.git
cd sisyphus
```

#### 3. Dependencies Installation

```bash
pip install -r requirements.txt
```

#### 4. Configuration

Configure your environment by editing the `.env` file with your specific settings.

##### Required Configuration

- **Model Configuration**: Essential for core functionality

##### Optional Configuration

For enhanced performance, consider integrating these services:

| Service | Purpose | Description |
|---------|---------|-------------|
| [**Tavily**](https://www.tavily.com/) | Web Search | Powerful search engine integration for comprehensive web queries |
| [**RapidAPI**](https://rapidapi.com/) | API Platform | Access to LinkedIn, Twitter, and other social media APIs for real-time data |

> **RapidAPI Note**: Ensure your account has active subscriptions to the required API providers.

## Quick Start

Get started with Sisyphus in one simple command:

```bash
python sisyphus.py 'What is the weather today?'
```

### Example Usage

```bash
# Simple query
python sisyphus.py 'Tell me about Python programming'

# Complex task
python sisyphus.py 'Plan a week-long vacation to Tokyo including flights, hotels, and activities'
```

## Acknowledgments

Sisyphus is built upon the excellent work of several open-source projects:

- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Provides the foundational framework for building stateful, multi-actor applications with LLMs
- **[Suna](https://github.com/kortix-ai/suna)**: A major source of inspiration for Sisyphus's architecture and design patterns. Many of the core design concepts in Sisyphus are directly influenced by Suna's innovative approach to agent systems

We deeply appreciate these projects and their contributions to the AI agent ecosystem.

