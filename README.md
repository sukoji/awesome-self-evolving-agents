<p align="center">
  <img src="assets/banner.svg" alt="Awesome Self-Evolving Agents" width="840">
</p>

<p align="center">
  <a href="https://awesome.re"><img src="https://awesome.re/badge-flat2.svg" alt="Awesome"></a>
  <a href="https://github.com/sukoji/awesome-self-evolving-agents/stargazers"><img src="https://img.shields.io/github/stars/sukoji/awesome-self-evolving-agents?logo=github&logoColor=white&style=flat&labelColor=1b1b1b&color=d85a30" alt="Stars"></a>
  <a href="https://github.com/sukoji/awesome-self-evolving-agents/network/members"><img src="https://img.shields.io/github/forks/sukoji/awesome-self-evolving-agents?logo=github&logoColor=white&style=flat&labelColor=1b1b1b&color=c0417a" alt="Forks"></a>
  <a href="https://github.com/sukoji/awesome-self-evolving-agents/commits/main"><img src="https://img.shields.io/github/last-commit/sukoji/awesome-self-evolving-agents?style=flat&labelColor=1b1b1b&color=1d9e75" alt="Last commit"></a>
  <a href="https://github.com/sukoji/awesome-self-evolving-agents/graphs/contributors"><img src="https://img.shields.io/github/contributors/sukoji/awesome-self-evolving-agents?style=flat&labelColor=1b1b1b&color=378add" alt="Contributors"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/papers-155+-8a63d2?style=flat&labelColor=1b1b1b" alt="155+ papers">
  <img src="https://img.shields.io/badge/topics-17-1d9e75?style=flat&labelColor=1b1b1b" alt="17 topics">
  <a href="COMMUNITY.md"><img src="https://img.shields.io/badge/community_projects-15+-c0417a?style=flat&labelColor=1b1b1b" alt="Community projects"></a>
  <a href="#reference-implementations"><img src="https://img.shields.io/badge/code-runnable-d85a30?style=flat&labelColor=1b1b1b" alt="Runnable code"></a>
  <a href="https://github.com/sukoji/awesome-self-evolving-agents/issues/new/choose"><img src="https://img.shields.io/badge/suggest-paper_or_project-issue-378add?style=flat&labelColor=1b1b1b" alt="Suggest via issue"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat&labelColor=1b1b1b" alt="PRs welcome"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC0%201.0-lightgrey?style=flat&labelColor=1b1b1b" alt="License: CC0-1.0"></a>
</p>

<p align="center">
  <sub><b>155+ papers</b> across <b>17 topics</b> · <b>15+ community projects</b> · <b>2 runnable demos</b> · reviewed monthly · last pass <b>2026-09</b></sub>
</p>

<p align="center">
  <a href="docs/primer.md">Primer</a> ·
  <a href="#the-four-evolution-pathways">Taxonomy</a> ·
  <a href="#recursive-self-improvement">RSI</a> ·
  <a href="#safety-misevolution-and-defenses">Safety</a> ·
  <a href="#community-spotlight">Community</a> ·
  <a href="#reference-implementations">Code</a> ·
  <a href="docs/contributing-guide.md">Contribute</a> ·
  <a href="#a-reading-path">Reading path</a> ·
  <a href="#updates">Updates</a>
</p>

A curated, deliberately opinionated map of **self-evolving / self-improving LLM agents**: systems that keep changing themselves after deployment — refining their prompts, memory, tools, and even weights from their own experience.

Most lists in this space are link dumps. This one tries to be a *map you can walk*: a short primer that builds the ideas from the ground up, a taxonomy that reflects how the field actually splits, two small **runnable** reference implementations, and — unusually — an honest section on how these systems fail. Self-evolution is powerful and half-broken at the same time, and a reading list that only shows the wins is misleading.

If you read one thing first, read the [**primer**](docs/primer.md). If you run one thing, run [`code/safety_gated_evolution.py`](code/safety_gated_evolution.py).

---

## Contents

- [Scope and stance](#scope-and-stance)
- [A one-diagram primer](#a-one-diagram-primer)
- [The four evolution pathways](#the-four-evolution-pathways)
- [Surveys and roadmaps](#surveys-and-roadmaps)
- [Foundations and precursors](#foundations-and-precursors)
- [Automated and self-evolving system design](#automated-and-self-evolving-system-design)
- [Test-time learning and self-improvement](#test-time-learning-and-self-improvement)
- [Memory: non-parametric to parametric](#memory-non-parametric-to-parametric)
- [Experience-driven lifelong learning and skills](#experience-driven-lifelong-learning-and-skills)
- [Zero-data self-evolution and self-play](#zero-data-self-evolution-and-self-play)
- [Self-evolving coding agents](#self-evolving-coding-agents)
- [Recursive self-improvement](#recursive-self-improvement)
- [Reinforcement learning for self-evolution](#reinforcement-learning-for-self-evolution)
- [Multi-agent co-evolution](#multi-agent-co-evolution)
- [Forgetting, drift, and stability](#forgetting-drift-and-stability)
- [Why they fail: failure analysis and attribution](#why-they-fail-failure-analysis-and-attribution)
- [Safety: misevolution and defenses](#safety-misevolution-and-defenses)
- [Benchmarks and environments](#benchmarks-and-environments)
- [Interoperability protocols](#interoperability-protocols)
- [Domain applications](#domain-applications)
- [Community spotlight](#community-spotlight)
- [Reference implementations](#reference-implementations)
- [A reading path](#a-reading-path)
- [Updates](#updates)
- [How this list is maintained](#how-this-list-is-maintained)
- [Related lists](#related-lists)
- [Contributing](#contributing)
- [License](#license)

---

## Scope and stance

**In scope:** LLM-based agents whose *behavior-generating machinery* changes over time from their own operation — automated agent/workflow design, test-time learning, evolving memory, skill acquisition, RL-driven self-improvement, and the safety and evaluation problems these create.

**Out of scope (mostly):** one-shot prompting tricks, static multi-agent frameworks with no learning loop, and pure model pre/post-training that is not agentic. Classic reasoning and memory papers appear only where they are load-bearing precursors.

**Our stance, stated plainly so you can discount it:**

1. The most important result of the last year is a negative one — *misevolution* (see [safety](#safety-misevolution-and-defenses)). Self-improvement and safety-alignment decay are the same process seen from two angles.
2. "More agents / more evolution" is not a strategy. The design-as-search literature keeps rediscovering that unconstrained self-modification overshoots into worse operating points.
3. Benchmarks are the bottleneck. Most reported gains are measured on setups that cannot see slow drift, forgetting, or safety erosion.

Entries carry a one-line, non-marketing description. Where an arXiv ID is shown it has been checked against the source; where a paper is listed without a link we could not verify a stable ID and welcome a PR that adds one.

---

## A one-diagram primer

The canonical cautionary tale is a refund agent that learns from customer satisfaction. Approving a refund makes the customer happy, so the agent slowly learns *"approving is good"* as a context-blind rule — and starts approving things it should refuse. Task success stays high the whole time, which is exactly why the failure is easy to miss.

<p align="center">
  <img src="assets/misevolution-loop.svg" alt="The misevolution feedback loop" width="720">
</p>

Two root causes run through most of this list:

- **Reward hacking.** The agent optimizes an easy-to-measure proxy (satisfaction) instead of the true goal (correct decisions).
- **Context-blindness.** When adaptation flows through one blunt channel, raising it to catch borderline-good cases unavoidably lets bad cases through too. Utility and safety get tied together.

The full build-up — from "what is an agent" to Pareto frontiers — is in [`docs/primer.md`](docs/primer.md), and the loop above is reproduced by [`code/safety_gated_evolution.py`](code/safety_gated_evolution.py).

---

## The four evolution pathways

A useful spine for the whole field (popularized by the misevolution work) is to ask *what* is being changed:

| Pathway | What changes | Typical mechanism | Representative work |
|---|---|---|---|
| **Model** | The weights themselves | self-training, RL, continual fine-tuning | TTRL, Evolving-RL, continual instruction tuning |
| **Memory** | What the agent remembers | reflection, memory writes, LoRA-as-memory | Reflexion, MemGPT, TMEM, Evo-Memory |
| **Tool** | The tools it can call | tool creation, skill libraries | AutoSkill, SkillFlow, EvoSkill |
| **Workflow** | Roles, topology, prompts | search / meta-optimization | ADAS, AFlow, MaAS, GPTSwarm |

The sections below are organized roughly along these pathways, plus the cross-cutting concerns (failure, safety, evaluation, protocols).

---

## Surveys and roadmaps

Start here to get the shape of the field before diving into primary work.

- **A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence** — TMLR 2026. [arXiv:2507.21046](https://arxiv.org/abs/2507.21046). Organizes work by the *what/when/how/where* of evolution and traces the ADAS→AFlow→MaAS lineage.
- **A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems** — 2025. [arXiv:2508.07407](https://arxiv.org/abs/2508.07407). Section 5.2 on self-evolving multi-agent systems is the cleanest short treatment of design-as-search.
- **A Systematic Survey of Self-Evolving Agents: From Model-Centric to Environment-Driven Co-Evolution** — 2026 (Xiang et al.). [TechRxiv](https://doi.org/10.36227/techrxiv.177203250.05832634/v2). Taxonomy of model-centric, environment-centric, and co-evolutionary self-improvement loops.
- **Lifelong Learning of Large Language Model Based Agents: A Roadmap** — IEEE TPAMI 2026. [arXiv:2501.07278](https://arxiv.org/abs/2501.07278). Organizes the lifelong-agent problem around a perception / memory / action pipeline.
- **Self-Improvements in Modern Agentic Systems: A Survey** — 2026. [arXiv:2607.13104](https://arxiv.org/abs/2607.13104). Surveys self-improvement across modern agentic systems, later than the two surveys above and covering the coding-agent and zero-data lines they predate.

---

## Foundations and precursors

Not self-evolving on their own, but every later method assumes these.

- **Self-Refine: Iterative Refinement with Self-Feedback** — NeurIPS 2023. [arXiv:2303.17651](https://arxiv.org/abs/2303.17651). The agent critiques and revises its own output in a loop.
- **Reflexion: Language Agents with Verbal Reinforcement Learning** — NeurIPS 2023. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366). Verbal reflection appended to the prompt across episodes — still the baseline everyone compares against.
- **Generative Agents: Interactive Simulacra of Human Behavior** — UIST 2023. [arXiv:2304.03442](https://arxiv.org/abs/2304.03442). Memory stream + reflection + planning; the origin of much agent-memory design.
- **MemGPT: Towards LLMs as Operating Systems** — 2023. [arXiv:2310.08560](https://arxiv.org/abs/2310.08560). Tiered memory management for long context.
- **Voyager: An Open-Ended Embodied Agent with Large Language Models** — TMLR 2024. [arXiv:2305.16291](https://arxiv.org/abs/2305.16291). Lifelong skill-library growth in Minecraft; the template for "learn reusable skills from experience."
- **DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines** — 2023. [arXiv:2310.03714](https://arxiv.org/abs/2310.03714). Treats prompts/pipelines as programs to be optimized.
- **Automatic Prompt Engineer (APE)** — ICLR 2023. [arXiv:2211.01910](https://arxiv.org/abs/2211.01910). Propose-and-score prompt search.
- **Large Language Models as Optimizers (OPRO)** — 2023. [arXiv:2309.03409](https://arxiv.org/abs/2309.03409). The model itself proposes improved instructions.
- **Promptbreeder: Self-Referential Self-Improvement via Prompt Evolution** — 2023. [arXiv:2309.16797](https://arxiv.org/abs/2309.16797). Evolutionary prompt mutation, including of the mutation prompts.
- **TextGrad: Automatic "Differentiation" via Text** — 2024. [arXiv:2406.07496](https://arxiv.org/abs/2406.07496). Backprop-style credit assignment through natural-language feedback.
- **STaR: Bootstrapping Reasoning With Reasoning** — 2022. [arXiv:2203.14465](https://arxiv.org/abs/2203.14465). Trains a model on the rationales it generated and got right, then repeats — the bootstrap loop most later self-training work is a variation on.

---

## Automated and self-evolving system design

Design the multi-agent system by *searching* over prompts, roles, and topology instead of hand-crafting it. This is the most mature sub-area; the ADAS→AFlow→MaAS arc is the backbone.

- **GPTSwarm: Language Agents as Optimizable Graphs** — ICML 2024. [arXiv:2402.16823](https://arxiv.org/abs/2402.16823). Models agents as optimizable computational graphs with node- and edge-level search.
- **Automated Design of Agentic Systems (ADAS)** — ICLR 2025. [arXiv:2408.08435](https://arxiv.org/abs/2408.08435). Frames design as search over a Turing-complete code space with a meta-agent + archive. Frames agentic-system design as meta-level search over a code/archive space.
- **AFlow: Automating Agentic Workflow Generation** — ICLR 2025 (Oral). [arXiv:2410.10762](https://arxiv.org/abs/2410.10762). Makes ADAS practical with reusable operators and Monte Carlo Tree Search over workflows.
- **Multi-agent Architecture Search via Agentic Supernet (MaAS)** — ICML 2025 (Oral). [arXiv:2502.04180](https://arxiv.org/abs/2502.04180). Samples a query-specific multi-agent system from a probabilistic supernet.
- **AgentSquare: Automatic LLM Agent Search in Modular Design Space** — ICLR 2025. [arXiv:2410.06153](https://arxiv.org/abs/2410.06153). Searches modular planning / reasoning / tool-use / memory combinations via module evolution and recombination.
- **Multi-Agent Design: Optimizing Agents with Better Prompts and Topologies (MASS)** — 2025. [arXiv:2502.02533](https://arxiv.org/abs/2502.02533). Co-optimizes prompts and multi-agent topology jointly.
- **G-Designer: Architecting Multi-agent Communication Topologies** — 2024. [arXiv:2410.11782](https://arxiv.org/abs/2410.11782). Generates task-specific communication topologies with a graph auto-encoder.
- **EvoAgent: Towards Automatic Multi-Agent Generation via Evolutionary Algorithms** — 2024. [arXiv:2406.14228](https://arxiv.org/abs/2406.14228). Evolves a population of agents from a single-agent seed.
- **AutoAgents: A Framework for Automatic Agent Generation** — 2023. [arXiv:2309.17288](https://arxiv.org/abs/2309.17288). Instantiates task-specific agent teams under a planner/manager.
- **MAS-GPT: Training LLMs to Build LLM-Based Multi-Agent Systems** — 2025. [arXiv:2503.03686](https://arxiv.org/abs/2503.03686). Learns to emit an executable multi-agent program from a query.
- **FlowReasoner: Reinforcing Query-Level Meta-Agents** — 2025. [arXiv:2504.15257](https://arxiv.org/abs/2504.15257). RL-trained meta-agent that designs a workflow per query.
- **ScoreFlow: Mastering LLM Agent Workflows via Score-Based Preference Optimization** — 2025. [arXiv:2502.04306](https://arxiv.org/abs/2502.04306). Preference optimization over workflow variants.
- **MetaAgent: Automatically Constructing Multi-Agent Systems Based on Finite State Machines** — ICML 2025. [arXiv:2507.22606](https://arxiv.org/abs/2507.22606). Constructs multi-agent systems as finite state machines.
- **AutoMaAS / AdaptMaAS: Self-Evolving Multi-Agent Architecture Search** — 2025. [arXiv:2510.02669](https://arxiv.org/abs/2510.02669). Adds a dynamic operator lifecycle, online feedback, and explicit cost-awareness to supernet search.
- **ABSTRAL: Automatic Design of Multi-Agent Systems Through Iterative Refinement and Abstraction** — 2026. [arXiv:2603.22791](https://arxiv.org/abs/2603.22791). Treats MAS architecture as an evolving natural-language document refined by contrastive trace analysis. Measures the coordination tax (26% turn efficiency under fixed budgets), shows design knowledge transfers across domains, and discovers specialist roles absent from any initial design.
- **EvoMAS: Evolutionary Generation of Multi-Agent Systems** — 2026. [arXiv:2602.06511](https://arxiv.org/abs/2602.06511). Survey-plus-method view of automatic MAS generation.
- **Difficulty-Aware Agent Orchestration in LLM-Powered Workflows** — 2025. [arXiv:2509.11079](https://arxiv.org/abs/2509.11079). Allocates deliberation to a query in proportion to its difficulty.
- **CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery** — 2026. [arXiv:2604.01658](https://arxiv.org/abs/2604.01658). Open-ended multi-agent evolution for discovery.
- **R&D-Agent: Automating Data-Driven AI Solution Building** — 2025. [github.com/microsoft/RD-Agent](https://github.com/microsoft/RD-Agent). Automates research, development, and iteration over data-driven AI solutions.

---

## Test-time learning and self-improvement

Improve *during deployment*, with or without weight updates. The fastest-moving cluster right now.

- **Self-Improving LLM Agents at Test-Time (TT-SI)** — 2025. [arXiv:2510.07841](https://arxiv.org/abs/2510.07841). Generates its own targeted practice data at test time for uncertain cases.
- **AREX: Towards a Recursively Self-Improving Agent for Deep Research** — 2026. [arXiv:2607.21461](https://arxiv.org/abs/2607.21461). Exploits the gap between costly discovery and cheap constraint-wise verification: an outer loop audits the provisional answer and launches targeted follow-up research. Named for RSI, but what recurses is the answer to one task, not the system.
- **EvoTest: Evolutionary Test-Time Learning for Self-Improving Agentic Systems** — 2025. [arXiv:2510.13220](https://arxiv.org/abs/2510.13220). An Act–Evolve loop that evolves the *whole* configuration (policy, hyperparameters, memory rules), using the full trajectory transcript as rich narrative feedback for credit assignment.
- **Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory** — 2025. [arXiv:2504.07952](https://arxiv.org/abs/2504.07952). A running, self-curated scratchpad of reusable tips.
- **TTRL: Test-Time Reinforcement Learning** — 2025. [arXiv:2504.16084](https://arxiv.org/abs/2504.16084). RL updates at inference time without ground-truth labels.
- **Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification** — 2026. [arXiv:2601.15808](https://arxiv.org/abs/2601.15808). Scales the *verifier* rather than the generator. Derives rubrics from an automatically constructed failure taxonomy (5 categories, 13 sub-categories) and reports 12-48% meta-evaluation F1 gains over agent-as-judge baselines.
- **Learning to Reason Without External Rewards** — 2025. [arXiv:2505.19590](https://arxiv.org/abs/2505.19590). Intrinsic signals in place of external reward.
- **Reinforcement Learning from Meta-Evaluation: Aligning Language Models Without Ground-Truth Labels** — 2026. [arXiv:2601.21268](https://arxiv.org/abs/2601.21268). Reaches accuracy and sample efficiency comparable to label-based training, with controllable trade-offs among objectives, in open-domain settings where labels do not exist.
- **GEPA: Reflective Prompt Evolution** — ICLR 2026. [arXiv:2507.19457](https://arxiv.org/abs/2507.19457). Reflective prompt evolution using natural-language feedback from trajectories.

---

## Memory: non-parametric to parametric

The sharpest current design axis: keep experience as *text you retrieve* or write it *into weights*.

- **MemoryBank: Enhancing LLMs with Long-Term Memory** — 2024. [arXiv:2305.10250](https://arxiv.org/abs/2305.10250). Forgetting-curve-inspired hierarchical memory updates.
- **Memento: Fine-tuning LLM Agents without Fine-tuning LLMs** — 2025. [arXiv:2508.16153](https://arxiv.org/abs/2508.16153). Case-based memory with online reinforcement learning, without weight updates.
- **ArcMemo: Abstract Reasoning Composition with Lifelong LLM Memory** — 2025. [arXiv:2509.04439](https://arxiv.org/abs/2509.04439). Stores reusable concept-level abstractions for compositional reasoning.
- **Agent KB: Leveraging Cross-Domain Experience for Agentic Problem Solving** — 2025. [arXiv:2507.06229](https://arxiv.org/abs/2507.06229). A shared experience base transferable across tasks.
- **ExpSeek: Self-Triggered Experience Seeking for Web Agents** — 2026. [arXiv:2601.08605](https://arxiv.org/abs/2601.08605). Lets the agent decide when to retrieve relevant past experience.
- **Doc-to-LoRA: Learning to Instantly Internalize Contexts** — 2026. [arXiv:2602.15902](https://arxiv.org/abs/2602.15902). A hypernetwork that meta-learns approximate context distillation in a single forward pass, generating a LoRA adapter from an unseen prompt so later queries skip re-reading the context. Included as the mechanism parametric memory builds on.
- **Scaling Self-Evolving Agents via Parametric Memory (TMEM)** — 2026. [arXiv:2606.04536](https://arxiv.org/abs/2606.04536). Argues prompt-space memory lets an agent *look up* experience but never *learn from* it, since the policy stays frozen. Absorbs distilled supervision into fast LoRA weights within a single episode; setting the weight delta to zero recovers explicit-memory agents as a special case.
- **Learning to Self-Evolve** — 2026. [arXiv:2603.18620](https://arxiv.org/abs/2603.18620). Trains models to refine their own test-time contexts with improvement-based rewards.

---

## Experience-driven lifelong learning and skills

Accumulate reusable capability across a long life of tasks — and try not to forget or drift.

- **RewardHarness: Self-Evolving Agentic Post-Training** — 2026. [arXiv:2605.08703](https://arxiv.org/abs/2605.08703). Evolves a reusable library of scoring skills and tools from preference feedback while keeping the evaluator model frozen.
- **Building Self-Evolving Agents via Experience-Driven Lifelong Learning (ELL) + StuLife** — 2025. [arXiv:2508.19005](https://arxiv.org/abs/2508.19005). Formalizes ELL (long-term memory, skill learning, self-motivation) and ships StuLife, a simulated college-life benchmark for it.
- **Yunjue Agent Tech Report: A Fully Reproducible, Zero-Start In-Situ Self-Evolving Agent System for Open-Ended Tasks** — 2026. [arXiv:2601.18226](https://arxiv.org/abs/2601.18226). Identifies *tool evolution* as the key pathway because it yields verifiable binary feedback; uses Parallel Batch Evolution to merge similar tools and prevent tool explosion. Starts from an empty toolset.
- **OpenSkill: Open-World Self-Evolution for LLM Agents** — 2026. [arXiv:2606.06741](https://arxiv.org/abs/2606.06741). Acquires reusable skills from public resources and constructs verification signals without target-task supervision.
- **AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution** — 2026. [arXiv:2603.01145](https://arxiv.org/abs/2603.01145). Derives, maintains, and reuses skills from dialogue traces as a model-agnostic plugin layer, injecting relevant skills into future requests without retraining.
- **SkillFlow: Benchmarking Lifelong Skill Discovery and Evolution for Autonomous Agents** — 2026. [arXiv:2604.17308](https://arxiv.org/abs/2604.17308). Method plus benchmark for continuous skill revision.
- **EvoSkill: Automated Skill Discovery for Multi-Agent Systems** — 2026. [arXiv:2603.02766](https://arxiv.org/abs/2603.02766). Discovers reusable skills for multi-agent teams from experience.
- **SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning** — 2026. [arXiv:2602.08234](https://arxiv.org/abs/2602.08234). Evolves agents with recursively composed skill libraries under RL.
- **SkillClaw: Let Skills Evolve Collectively with an Agentic Evolver** — 2026. [arXiv:2604.08377](https://arxiv.org/abs/2604.08377). Evolves a shared skill pool collectively across agents.
- **ARISE: Agent Reasoning with Intrinsic Skill Evolution in Hierarchical RL** — 2026. [arXiv:2603.16060](https://arxiv.org/abs/2603.16060). Learns hierarchical skills intrinsically during agent reasoning.
- **PolySkill: Learning Generalizable Skills Through Polymorphic Abstraction** — ICLR 2026. [arXiv:2510.15863](https://arxiv.org/abs/2510.15863). Abstracts skills so they transfer across domains rather than overfitting to one.
- **Self-Evolving LLMs via Continual Instruction Tuning** — 2025. [arXiv:2509.18133](https://arxiv.org/abs/2509.18133). Continually updates instruction-following behavior from new experience.
- **Self-Evolving Curriculum for LLM Reasoning** — 2025. [arXiv:2505.14970](https://arxiv.org/abs/2505.14970). The agent designs its own curriculum.
- **ForeDreamer: A Self-Evolving Dual-Agent Memory Architecture for Future Event Prediction** — EMNLP Findings 2026. [arXiv:2608.20920](https://arxiv.org/abs/2608.20920). Separates question-specific factual memory from persistent experiential memory and evolves an Experience Bank together with MemGuide/MemTool procedures through validation-gated updates.
- **ExpeL: LLM Agents Are Experiential Learners** — 2023. [arXiv:2308.10144](https://arxiv.org/abs/2308.10144). Collects trajectories across a task set, extracts natural-language insights from them, and reuses both at inference without touching the weights.

---

## Zero-data self-evolution and self-play

The most striking recent claim in the field: an agent can bootstrap capability with **no human-curated tasks or labels at all**, by generating its own curriculum. Usually a *proposer* invents tasks and a *solver* learns to solve them, with an executor or majority vote supplying verification in place of ground truth.

- **Absolute Zero: Reinforced Self-play Reasoning with Zero Data** — 2025. [arXiv:2505.03335](https://arxiv.org/abs/2505.03335). A single model proposes tasks that maximize its own learning progress and improves by solving them, using a code executor as the unified source of verifiable feedback. Reaches strong coding/math results with no external data.
- **R-Zero: Self-Evolving Reasoning LLM from Zero Data** — ICLR 2026. [arXiv:2508.05004](https://arxiv.org/abs/2508.05004). A Challenger and a Solver, both initialized from the same base model, co-evolve; filtering plus majority vote substitutes for labels. Reports roughly +6.5 on math and +7.5 on general reasoning for a 4B backbone.
- **SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning** — ICLR 2026. [arXiv:2506.24119](https://arxiv.org/abs/2506.24119). Frames self-improvement as multi-turn zero-sum self-play.
- **Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning** — 2025. [arXiv:2511.16043](https://arxiv.org/abs/2511.16043). Adds tool-integrated execution to self-generated curricula.
- **MM-Zero: Self-Evolving Multi-Model Vision Language Models From Zero Data** — 2026. [arXiv:2603.09206](https://arxiv.org/abs/2603.09206). Extends the proposer/solver idea to vision-language via self-generation and self-verification.
- **Evolving Language Models without Labels: Majority Drives Selection, Novelty Promotes Variation** — 2025. [arXiv:2509.15194](https://arxiv.org/abs/2509.15194). Analyzes what actually drives label-free evolution.
- **Towards Understanding Self-play for LLM Reasoning** — 2025. [arXiv:2510.27072](https://arxiv.org/abs/2510.27072). An empirical dissection of the AZR recipe — useful before you trust the headline numbers.
- **Tool-R0: Self-Evolving LLM Agents for Tool-Learning from Zero Data** — 2026. [arXiv:2602.21320](https://arxiv.org/abs/2602.21320). The zero-data recipe applied to tool use.

> Read this cluster together with [forgetting and drift](#forgetting-drift-and-stability). Self-generated curricula are exactly the setting where the agent supplies its own data, its own evaluator, and its own prior — which is where most guarantees stop applying.

---

## Self-evolving coding agents

Software engineering has become the flagship domain for self-evolution, because executable feedback, repository context, and test suites give an unusually reliable reward signal.

- **Self-Evolving Coding Agents: A Survey** — 2026. [arXiv:2608.03392](https://arxiv.org/abs/2608.03392). A target-centered taxonomy of *what* evolves, plus *when* evolution happens and which code-specific signals drive it. Notes that executable feedback and repo-level context make software a natural fit — while introducing feedback reliability, benchmark overfitting, reversibility, and cost problems. Ships a curated companion list updated through August 2026.
- **A Self-Improving Coding Agent** — 2025. [OpenReview](https://openreview.net/forum?id=rShJCyLsOr). An agent that edits its own codebase to get better at editing codebases.
- **Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement** — ACL 2025. [arXiv:2410.04444](https://arxiv.org/abs/2410.04444). The clearest statement of recursive self-modification in this space.
- **R&D-Agent: An LLM-Agent Framework Towards Autonomous Data Science** — 2025. [arXiv:2505.14738](https://arxiv.org/abs/2505.14738). Automated research/development loops for data-driven work.
- **Controlled Self-Evolution for Algorithmic Code Optimization** — 2026. [arXiv:2601.07348](https://arxiv.org/abs/2601.07348). Puts explicit controls around the self-modification loop.
- **AlphaApollo: A System for Deep Agentic Reasoning** — 2026. [arXiv:2510.06261](https://arxiv.org/abs/2510.06261).
- **SEMAG: Self-Evolutionary Multi-Agent Code Generation** — 2026. [arXiv:2603.15707](https://arxiv.org/abs/2603.15707).
- **Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents** — 2025. [arXiv:2505.22954](https://arxiv.org/abs/2505.22954). Rewrites its own code and keeps an archive of every variant, so improvements that look like dead ends stay available to build on later.
- **AlphaEvolve: A Coding Agent for Scientific and Algorithmic Discovery** — 2025. [arXiv:2506.13131](https://arxiv.org/abs/2506.13131). Evolves programs against an automated evaluator, and reports discovered algorithms that improve on the best known ones.
- **Co-Evolving LLM Coder and Unit Tester via Reinforcement Learning** — NeurIPS 2025. [arXiv:2506.03136](https://arxiv.org/abs/2506.03136). Coder and test-writer improve against each other.

---

## Recursive self-improvement

The narrow end of the field, and the one with the most new work this year. *Recursive* self-improvement (RSI) means improving the process that produces the next system — the harness, the training algorithm, the exploration policy, the evaluator — so the gain compounds instead of being spent on one answer. The line runs from Gödel Agent and the Darwin Gödel Machine in the [coding section](#self-evolving-coding-agents) to the papers below; ICLR 2026 gave it a [dedicated workshop](https://iclr.cc/virtual/2026/workshop/10000796).

- **Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops** — 2026. [arXiv:2607.07663](https://arxiv.org/abs/2607.07663). Surveys 1,250 papers along what is improved (behaviour, policy, evaluator, research process) and how closed the loop is, and finds that demonstrated improvement strength tracks the strength of the verification signal — formal verifiers at the top, intrinsic self-assessment at the bottom. Start here.
- **Generalized Agent Iteration: One Formal Framework for Iterative Policy Improvement and Recursive Self-Improvement** — 2026. [arXiv:2609.13406](https://arxiv.org/abs/2609.13406). Casts RSI and classical policy iteration as one cycle distinguished by two dials — whether the improver is part of the agent, and whether the standard it is measured against is grounded outside it — so existing systems, and their defects, sit on the same axes.
- **The Economics of Recursive Self-Improvement** — 2026. [arXiv:2609.15802](https://arxiv.org/abs/2609.15802). Models RSI as feedback loops whose net acceleration is the product of their elasticities, separates narrow AI-R&D gains from broad capability, and calibrates to existing data: the loops are not yet strong enough to be self-sustaining, though they appear to be strengthening.
- **Dream-RSI: Recursive Self-Improvement through Evolving Worlds** — 2026. [arXiv:2609.14858](https://arxiv.org/abs/2609.14858). Treats the accumulated history of discovery trees as a replay simulator, refines the exploration policy off-policy inside it, and redeploys the policy online, leaving the underlying coding agent unchanged; across algorithm engineering, mathematical optimization, and GPU kernels it matches or improves discovery quality and cuts discovery cost in several of the settings.
- **ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement** — 2026. [arXiv:2609.14857](https://arxiv.org/abs/2609.14857). Evolves a harness split into five modules on 2,000 tasks disjoint from the evaluation benchmarks, contrasting successful and failed runs of the same task, so improvements transfer to unseen tasks and other foundation models instead of fitting the benchmark.
- **HELIX: Model-Harness Co-evolution for Recursive Self-Improvement** — 2026. [arXiv:2608.13951](https://arxiv.org/abs/2608.13951). Makes harness edits typed and source-traceable, so harness evolution both improves a fixed model and yields verified sibling trajectories as training data for the next; the paper runs one round, on code repair, and stops before the model update.
- **Meta^n: Recursive Self-Improvement through Emergent Depth** — 2026. [arXiv:2608.24735](https://arxiv.org/abs/2608.24735). Holds a single meta-operation fixed and recurses on its growing input rather than editing itself, to get past the roughly two meta-levels that self-editing systems stay stable at; the only self-improving agent in its comparison to score above zero on ARC-AGI-2.
- **MetaRSI / RSI2: A Meta-Recursive Self-Improving System for Recursive Self-Improving Systems Themselves** — 2026. [arXiv:2609.06396](https://arxiv.org/abs/2609.06396). Schedules three typed operators — data, harness, and model RSI — over one loop, with a meta-policy that revises the schedule, so improvements across the model-production pipeline compose rather than compete. Argues RSI must leave machine-checkable domains, but validates only on code and closed-form science.
- **Mendel Gödel Machine: Recursive Self-Improving Coding Agents via Comparative Evolution** — 2026. [arXiv:2608.07645](https://arxiv.org/abs/2608.07645). Adds two self-modifications to single-trajectory mutation — editing from many tasks at once, and from another lineage's run on the same task — with a convergence argument and gains on SWE-bench and Polyglot.
- **The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators** — 2026. [arXiv:2606.26294](https://arxiv.org/abs/2606.26294). Lets the utility change between epochs while holding it fixed within one, so evaluators can co-evolve with the agents they judge without voiding per-epoch improvement guarantees. A preliminary preprint by its own description.
- **RSIAgent: Autonomous Exploration for Recursive Self-improvement in New Environments** — 2026. [arXiv:2609.15364](https://arxiv.org/abs/2609.15364). A training-free curriculum–actor–verifier loop that explores a new digital environment broad-then-deep and freezes what it learns as reusable causal memory.
- **Frontis-MA1: Training an AI4AI Model towards Recursive Self-Improvement in Machine Learning Engineering** — 2026. [arXiv:2607.28568](https://arxiv.org/abs/2607.28568). Releases OpenMLE, an open stack of gym, RL, and evolutionary search for ML engineering, and a 35B model post-trained on the same four program-evolution operators its search composes.

> Read this section against its own measurements. On [AI4AI-Bench](#benchmarks-and-environments) the best system closes under a fifth of the gap between a repository's shipped training algorithm and the optimum; the survey finds open-ended RSI bounded on every axis it measured; the economics paper puts the loops below self-sustaining. The failure modes that matter most here — [self-authored verification](#why-they-fail-failure-analysis-and-attribution) and [harness tampering](#safety-misevolution-and-defenses) — are already documented. For the case that RSI is further off than the headlines, see [MIT Technology Review, August 2026](https://www.technologyreview.com/2026/08/18/1142188/ai-recursive-self-improvement/).

---

## Reinforcement learning for self-evolution

Instead of hand-designing the improvement rule, learn the *capacity to improve*.

- **Evolving-RL: End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents** — 2026. [arXiv:2605.10663](https://arxiv.org/abs/2605.10663). Jointly optimizes experience *extraction* and *utilization* rather than treating them separately. Notably reports that skills a base model extracts on its own can *degrade* performance versus injecting nothing.
- **Self-Evolved Reward Learning for LLMs** — 2024. [arXiv:2411.00418](https://arxiv.org/abs/2411.00418). The reward model bootstraps itself.
- **Complementary RL: Towards Efficient Experience-Driven Agent Learning** — 2026. [arXiv:2603.17621](https://arxiv.org/abs/2603.17621). Combines parametric RL with experience-driven learning rather than treating them as alternatives.
- **SEAS: Self-Evolving Adversarial Safety Optimization** — AAAI 2025. [arXiv:2408.02632](https://arxiv.org/abs/2408.02632). Co-evolves attacker and defender models for adversarial safety hardening.

---

## Multi-agent co-evolution

Several agents (or an agent and its data generator) improve against each other.

- **Multi-Agent Evolve: LLM Self-Improve through Co-Evolution** — 2025. [arXiv:2510.23595](https://arxiv.org/abs/2510.23595). Self-play-style improvement among cooperating or competing agents.
- **AgentNet: Decentralized Evolutionary Coordination for LLM-Based Multi-Agent Systems** — 2025. [arXiv:2504.00587](https://arxiv.org/abs/2504.00587). Decentralized evolutionary coordination among LLM agents.
- **X-MAS: Towards Building Multi-Agent Systems with Heterogeneous LLMs** — 2025. [arXiv:2505.16997](https://arxiv.org/abs/2505.16997). Builds multi-agent teams from heterogeneous LLM backbones.
- **Agent-World: Scaling Real-World Environment Synthesis for Evolving General Agent Intelligence** — 2026. [arXiv:2604.18292](https://arxiv.org/abs/2604.18292). Co-evolves agents with synthesized real-world environments.
- **Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing** — 2026. [arXiv:2602.04837](https://arxiv.org/abs/2602.04837). A population of agents improves by sharing experience rather than each learning alone.
- **TerraLingua: Emergence and Analysis of Open-Endedness in LLM Ecologies** — 2026. [arXiv:2603.16910](https://arxiv.org/abs/2603.16910). Studies open-endedness in populations of interacting models.
- **MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory** — 2026. [arXiv:2601.03192](https://arxiv.org/abs/2601.03192). RL applied at runtime over episodic memory.
- **Agent-Pro: Learning to Evolve via Policy-Level Reflection and Optimization** — ACL 2024. [arXiv:2402.17574](https://arxiv.org/abs/2402.17574). Reflection at the level of policy rather than individual actions.

---

## Forgetting, drift, and stability

An agent that keeps updating itself can quietly *lose* capabilities it already had. This is the plasticity-vs-stability problem, and it is the second-biggest corrective thread after misevolution.

- **Do Self-Evolving Agents Forget? Capability Degradation and Preservation in Lifelong LLM Agent Adaptation** — 2026. [arXiv:2605.09315](https://arxiv.org/abs/2605.09315). Documents classical catastrophic forgetting under vanilla self-evolution: later updates overwrite parameter regions supporting earlier behaviors. Proposes Capability-Preserving Evolution, an EWC-style regularizer using Fisher importance weights, and argues stable long-horizon evolution requires *explicitly preserving* old capabilities, not just acquiring new ones.
- **Self-Evolving Agents with Anytime-Valid Certificates** — 2026. [arXiv:2607.00871](https://arxiv.org/abs/2607.00871). Names the **endogenous-loop failure mode**: the evolving policy generates the data it trains on, the evaluator it is judged by, and the hypothesis space it searches — so continual-learning and PAC-Bayes guarantees proved for *exogenous* environments no longer apply. The sharpest theoretical critique in the field right now.
- **Governing Evolving Memory in LLM Agents: the SSGM Framework** — 2026. [arXiv:2603.11768](https://arxiv.org/abs/2603.11768). Argues unconstrained memory autonomy is the primary catalyst for semantic drift, forgetting, and adversarial memory poisoning, and proposes decoupling the agent's policy from its memory substrate via governance middleware. Also names the hard open problem: telling *drift* apart from a *legitimate update*.
- **EvoMemBench: Benchmarking Agent Memory from a Self-Evolving Perspective** — 2026. [arXiv:2605.18421](https://arxiv.org/abs/2605.18421). Compares 15 memory methods against strong long-context baselines and finds no memory form wins consistently — long-context remains highly competitive.
- **EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle** — 2025. [arXiv:2510.16079](https://arxiv.org/abs/2510.16079). Distills abstract strategic knowledge rather than storing raw trajectories.
- **Towards Trustworthy Agentic AI: Safety, Robustness, Privacy, and System Security** — 2026. [arXiv:2605.23989](https://arxiv.org/abs/2605.23989). Broad survey; its lifelong-adaptation section frames the trust-utility trade-off.
- **ANCHOR: An External LLM-Driven Supervisory Module Facilitating Healthy Evolution in Self-Evolving Systems** — 2026. [arXiv:2606.06114](https://arxiv.org/abs/2606.06114). Adds an external supervisor that reviews each phase of self-evolution and feeds its verdicts back as context; retrofitted onto two open self-evolving frameworks, it raises safety while core capability holds steady.

> Memory accumulation alone does not solve continual learning — several independent lines report the opposite, with stale or misleading experiences acting as an active failure mode unless refinement and verification are explicit.

---

## Why they fail: failure analysis and attribution

The corrective literature. If you are building any of the above, read this section before you trust your numbers.

- **Why Do Multi-Agent LLM Systems Fail?** — 2025. [arXiv:2503.13657](https://arxiv.org/abs/2503.13657). Introduces the MAST taxonomy: 14 failure modes across system design, inter-agent misalignment, and verification, from 1,600+ annotated traces. The key finding: better base models will not fix most of them.
- **Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems** — ICML 2025. [arXiv:2505.00212](https://arxiv.org/abs/2505.00212). Attributes multi-agent failures to the responsible agent and step.
- **RAFFLES: Reasoning-based Attribution of Faults for LLM Systems** — 2025. [arXiv:2509.06822](https://arxiv.org/abs/2509.06822). Attributes faults in LLM systems via structured reasoning.
- **GUARDIAN: Safeguarding LLM Multi-Agent Collaborations with Temporal Graph Modeling** — 2025. [arXiv:2505.19234](https://arxiv.org/abs/2505.19234). Models multi-agent collaboration dynamics with temporal graphs for safeguarding.
- **Aegis: Taxonomy and Optimizations for Overcoming Agent-Environment Failures** — 2025. [arXiv:2508.19504](https://arxiv.org/abs/2508.19504). Treats the environment as a first-class component.
- **The Six Sigma Agent: Achieving Enterprise-Grade Reliability in LLM Systems Through Consensus-Driven Decomposed Execution** — 2026. [arXiv:2601.22290](https://arxiv.org/abs/2601.22290). Decomposes execution with consensus checks for higher reliability.
- **Understanding Bugs in Modern Agentic Frameworks: Symptoms, Root Causes, and Triggering Conditions** — 2026. [arXiv:2604.08906](https://arxiv.org/abs/2604.08906). 409 fixed bugs across five agentic frameworks under a five-layer architectural abstraction; finds the model-integration layer most bug-prone yet least covered by tests.
- **Efficient Failure Management for Multi-Agent Systems with Reasoning Trace Representation** — 2026. [arXiv:2603.21522](https://arxiv.org/abs/2603.21522). Manages multi-agent failures using compact reasoning-trace representations.
- **Training Agents to Evolve with Their Harness: TaoLive Digital Avatar Agent Technical Report** — 2026. [arXiv:2608.15763](https://arxiv.org/abs/2608.15763). Studies how fixed-harness training impedes later runtime edits and tests harness-state augmentation with frozen-weight edit evaluation.
- **Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents** — 2026. [arXiv:2607.24300](https://arxiv.org/abs/2607.24300). When an agent writes both the policy and the tests that accept it, self-assigned scores stay near perfect while sealed deployment performance degrades; adding an accept/reject audit the agent can neither see nor author outperforms unprotected baselines across six models.
- **On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification** — 2026. [arXiv:2608.18066](https://arxiv.org/abs/2608.18066). Re-runs memory-based self-improving agents across seeds and shuffled task orders, and finds the reported gains lean on a default ordering that acts as a hidden curriculum.
- **Rehearse: Stepping Back from the Confidence Cliff in Self-Improving Autoresearch** — 2026. [arXiv:2607.27687](https://arxiv.org/abs/2607.27687). An autoresearch loop's judgment of which change will help collapses late in the run — selective accuracy falls from 82.8% to 56.9% while the judge keeps deciding — and focused memory of similar past attempts restores it.

---

## Safety: misevolution and defenses

The part of the field that is under-appreciated relative to how important it is. Self-improvement can silently erode alignment.

- **Your Agent May Misevolve: Emergent Risks in Self-Evolving LLM Agents** — ICLR 2026. [arXiv:2509.26354](https://arxiv.org/abs/2509.26354). The paper this list is oriented around. Defines *misevolution* along the model/memory/tool/workflow pathways and shows it is pervasive even on top-tier backbones — including safety-refusal rates dropping sharply after self-training. Its four distinguishing traits (temporal emergence, environmental origin, limited data control, expanded risk surface) are why static safety evaluation misses it.
- **TAME: A Trustworthy Test-Time Evolution of Agent Memory with Systematic Benchmarking** — 2026. [arXiv:2602.03224](https://arxiv.org/abs/2602.03224). The closest thing to a defense. Introduces the Trust-Memevo benchmark, confirms trustworthiness declines even under *benign* task evolution, and proposes a dual-memory framework that evolves executor memory and evaluator memory separately so utility and safety improve together rather than trading off.
- **SEAS: Self-Evolving Adversarial Safety Optimization** — AAAI 2025. [arXiv:2408.02632](https://arxiv.org/abs/2408.02632). (Also in [RL section](#reinforcement-learning-for-self-evolution).) Co-evolutionary red-teaming.
- **Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses** — 2026. [arXiv:2605.02900](https://arxiv.org/abs/2605.02900). Surveys risks, attacks, and defenses for embodied AI systems.
- **AgenticRed: Optimizing Agentic Systems for Automated Red-teaming** — 2026. [arXiv:2601.13518](https://arxiv.org/abs/2601.13518). Turns the optimization machinery on the attack side — automated red-teaming of agentic systems.
- **Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward** — 2026. [arXiv:2602.12430](https://arxiv.org/abs/2602.12430). Treats self-acquired skills as a security surface, not just a capability store.
- **Identifying the Risks of LM Agents with an LM-Emulated Sandbox (ToolEmu)** — 2023. [arXiv:2309.15817](https://arxiv.org/abs/2309.15817). The precursor for sandboxed risk discovery, still the standard reference for testing agents safely.
- **Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents** — 2026. [arXiv:2608.12851](https://arxiv.org/abs/2608.12851). Misevolution measured at the skill level: all 21 evolved configurations authored unsafe artifacts, three malicious exposures raised carryover attack success from 16.0% to 35.3%, and the SafeEvolve wrapper cuts fresh-session harm by 17.3 points for a 0.4-point utility change.
- **Auditing Harness Tampering in Self-Improving Agents** — 2026. [arXiv:2609.00069](https://arxiv.org/abs/2609.00069). Extends reward and measurement tampering to agents that edit their own harness, and finds tampering — illusory gains, broken authorization or provenance — in real runs, often persisting in the best agent's lineage.
- **LLM-as-a-Judge Is Not an Oracle: Why Self-Improving Agents Need Deterministic Guardrails** — 2026. [arXiv:2609.02246](https://arxiv.org/abs/2609.02246). Eleven ways the evaluation signal failed across months of production prompt-optimization loops — including a 100% pass rate concealing 68% true capability — and the deterministic guardrails built in response, with the failures they still missed. A single-author position paper.

> If you take one idea from this list into production: aggregate task-success curves will look great while safety silently collapses. Measure utility and safety on separate axes, over time. The [reference implementation](#reference-implementations) exists to make that failure — and its partial fixes — visible in the reference code.

---

## Benchmarks and environments

Evaluation is the field's bottleneck; static one-shot benchmarks cannot see drift, forgetting, or safety erosion.

- **StuLife** — 2025. [arXiv:2508.19005](https://arxiv.org/abs/2508.19005). Simulated college journey testing long-term memory, proactivity, and learning-from-experience.
- **Evo-Memory** — 2025. [arXiv:2511.20857](https://arxiv.org/abs/2511.20857). Benchmarks test-time learning with self-evolving memory across sequential tasks.
- **SkillFlow** — 2026. [arXiv:2604.17308](https://arxiv.org/abs/2604.17308). Lifelong skill discovery and evolution.
- **LifelongAgentBench** — 2025. [arXiv:2505.11942](https://arxiv.org/abs/2505.11942). Interdependent task sequences across DB / OS / KG that require building on prior skills.
- **LTMBenchmark** — 2024. [github.com/GoodAI/goodai-ltm-benchmark](https://github.com/GoodAI/goodai-ltm-benchmark). Tests long-term memory retention under interleaved, distracted dialogue.
- **MLGym: A Framework and Benchmark for Advancing AI Research Agents** — 2025. [arXiv:2502.14499](https://arxiv.org/abs/2502.14499). Benchmarks agents that perform ML research tasks.
- **EvoClinician: A Self-Evolving Agent for Multi-Turn Medical Diagnosis via Test-Time Evolutionary Learning** — 2026. [arXiv:2601.22964](https://arxiv.org/abs/2601.22964). Ships the Med-Inquire benchmark for iterative diagnosis and a Diagnose-Grade-Evolve loop in which a Process Grader assigns credit per action on both clinical yield and resource cost.
- **AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design for Recursive Self-Improvement** — 2026. [arXiv:2608.20318](https://arxiv.org/abs/2608.20318). Ten frozen research repositories where the agent must rewrite the training algorithm itself, rerun from scratch and scored by a hidden evaluator; the best of 29 configurations closes under a fifth of the gap to the optimum.
- **RSIBench-Data: Benchmarking Data-Centric Research for Recursive Self-Improvement** — 2026. [arXiv:2607.25886](https://arxiv.org/abs/2607.25886). Isolates the data-strategy half of the loop on a fixed post-training stack; agents improve on their first attempt in 58% of settings, but 78% of searches that continue past their best score end lower.
- **PAST-Bench: Benchmarking the Foundations of Recursive Self-Improvement in Personal Agents** — 2026. [arXiv:2608.04003](https://arxiv.org/abs/2608.04003). Turns retained experience on and off across ordered fresh-session tasks, and checks whether gains came through the intended save–retrieve–update pathway.
- **The Meta-Agent Challenge: Are Current Agents Capable of Autonomous Agent Development?** — 2026. [arXiv:2606.04455](https://arxiv.org/abs/2606.04455). A code agent builds an agent against a held-out set under anti-reward-hacking defenses; meta-agents rarely match human baselines, and high optimization pressure surfaces ground-truth exfiltration.
- **S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?** — 2026. [arXiv:2608.31100](https://arxiv.org/abs/2608.31100). Separates permissive exploration from strict held-out evaluation in seven verifiable games, and compares history, summary memory, and parameter training as routes from experience to improvement.

---

## Interoperability protocols

Self-evolving tool use and multi-agent delegation increasingly ride on shared protocols. Included because "tool" and "workflow" evolution now happen across vendor boundaries.

- **MCP (Model Context Protocol)** — Anthropic, 2024. Agent-to-tool connectivity; now under the Linux Foundation's Agentic AI Foundation.
- **A2A (Agent-to-Agent)** — Google, 2025. Agent-to-agent discovery, delegation, and collaboration across vendors.
- **ACP (Agent Communication Protocol)** — IBM. REST-native agent messaging (later converging with A2A).
- **ANP (Agent Network Protocol)** — community. Decentralized, DID-based agent networks.
- **Beyond Message Passing: A Semantic View of Agent Communication Protocols** — 2026. [arXiv:2604.02369](https://arxiv.org/abs/2604.02369). Analyzes 18 protocols across communication, syntactic, and semantic layers, finding transport and schema support mature while clarification, context alignment, and verification remain thin.
- **Permission Manifests for Web Agents** — 2026. [arXiv:2601.02371](https://arxiv.org/abs/2601.02371). Capability scoping for agents acting on the web.

---

## Domain applications

Self-evolution grounded in a specific domain, useful as end-to-end case studies.

- **GenoMAS: A Multi-Agent Framework for Scientific Discovery via Code-Driven Gene Expression Analysis** — 2025. [arXiv:2507.21035](https://arxiv.org/abs/2507.21035). Multi-agent scientific discovery via code-driven gene-expression analysis.
- **EvoScientist: Towards Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery** — 2026. [arXiv:2603.08127](https://arxiv.org/abs/2603.08127). Evolves both ideation and experiment-execution strategies under one objective across the full discovery pipeline.
- **Mimosa Framework: Toward Evolving Multi-Agent Systems for Scientific Research** — 2026. [arXiv:2603.28986](https://arxiv.org/abs/2603.28986). Synthesizes task-specific workflows and refines them via experimental feedback, using MCP for dynamic tool discovery. Finds that the benefit of workflow evolution depends heavily on the backbone model.
- **PestMA: LLM-based Multi-Agent System for Informed Pest Management** — 2025. [arXiv:2504.09855](https://arxiv.org/abs/2504.09855). Multi-agent pest-management decisions from field and policy data.
- **OWL: Optimized Workforce Learning for General Multi-Agent Assistance** — 2025. [arXiv:2505.23885](https://arxiv.org/abs/2505.23885). Learns workforce-style coordination for general multi-agent assistance.
- **Self-Evolving Embodied AI** — 2026. [arXiv:2602.04411](https://arxiv.org/abs/2602.04411). Self-improving embodied agents in interactive environments.
- **Administrative Decentralization in Edge-Cloud Multi-Agent for Mobile Automation** — 2026. [arXiv:2604.07767](https://arxiv.org/abs/2604.07767). Edge–cloud multi-agent coordination for mobile automation.

---

## Community spotlight

Papers are the spine of this repo; **open-source projects** are the hands. [`COMMUNITY.md`](COMMUNITY.md) is a community-maintained board of harnesses, design-as-search stacks, benchmarks, and safety tooling — separate from the reading list so you can jump straight to code.

<p align="center">
  <a href="https://github.com/OpenHands/OpenHands"><img src="https://img.shields.io/badge/OpenHands-harness-d85a30?style=flat&labelColor=1b1b1b" alt="OpenHands"></a>
  <a href="https://github.com/stanfordnlp/dspy"><img src="https://img.shields.io/badge/DSPy-compile_&_optimize-8a63d2?style=flat&labelColor=1b1b1b" alt="DSPy"></a>
  <a href="https://github.com/FoundationAgents/aflow"><img src="https://img.shields.io/badge/AFlow-workflow_search-1d9e75?style=flat&labelColor=1b1b1b" alt="AFlow"></a>
  <a href="https://github.com/THUDM/AgentBench"><img src="https://img.shields.io/badge/AgentBench-eval-378add?style=flat&labelColor=1b1b1b" alt="AgentBench"></a>
  <a href="https://huggingface.co/datasets/ai-safety-institute/AgentHarm"><img src="https://img.shields.io/badge/AgentHarm-safety-c0417a?style=flat&labelColor=1b1b1b" alt="AgentHarm"></a>
  <a href="COMMUNITY.md"><img src="https://img.shields.io/badge/→_full_board-15+_projects-1b1b1b?style=flat&labelColor=1b1b1b&color=666" alt="Full community board"></a>
</p>

| | |
|---|---|
| **Add yours** | [Suggest a project (issue)](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-project.yml) · [PR to COMMUNITY.md](COMMUNITY.md) · [guide](docs/contributing-guide.md#adding-a-community-project-communitymd) |
| **Recently merged** | See [Recently added](COMMUNITY.md#recently-added) — new entries stay visible for one month |

> **Papers →** `README.md` &nbsp;·&nbsp; **Repos & tools →** `COMMUNITY.md` &nbsp;·&nbsp; **Corrections →** always welcome, always fast-tracked

---

## Reference implementations

Two small, dependency-light programs that make the core ideas concrete. Both are offline and deterministic; each is structured so a real LLM call drops into a single clearly marked method.

### `code/auto_mas.py` — design-as-search in miniature

A faithful miniature of ADAS / AFlow / MaAS: designing a multi-agent system framed as searching over `(operators, topology)` to maximize a **cost-aware** utility. An evolutionary meta-search discovers that a debate operator wins — and, crucially, that adding still more agents keeps raising raw accuracy while *lowering* utility once compute is priced in. That is the "more agents is not a strategy" result, reproduced in one file.

### `code/safety_gated_evolution.py` — misevolution, and two defenses

Reproduces the misevolution collapse and then studies two mitigations, tracing the utility–safety Pareto frontier:

- a memory **write-gate** (a verifier blocks detected violations from being learned), and
- periodic **re-anchoring** (leak the learned bias back toward the safety prior).

Findings the code is built to expose:

1. Unconstrained self-evolution overshoots to the worst corner — utility ≈ 1.0, safety ≈ 0.0.
2. The write-gate alone barely helps, because the drift is also fed by *legitimate* approvals.
3. Re-anchoring buys safety back, but along a frontier — a real utility cost.

<p align="center">
  <img src="assets/pareto_frontier.png" alt="Utility-safety Pareto frontier" width="440">
  <img src="assets/timeseries.png" alt="Safety and utility over time" width="820">
</p>

```bash
cd code
python3 auto_mas.py
python3 safety_gated_evolution.py   # writes plots to the current directory (examples in assets/)
```

See [`docs/primer.md`](docs/primer.md) for a line-by-line reading of `safety_gated_evolution.py` that maps each concept to its code.

---

## A reading path

**If you are new to the idea:** primer → *Why Do Multi-Agent LLM Systems Fail?* → *Your Agent May Misevolve* → run `safety_gated_evolution.py`.

**If you want to build automated design:** GPTSwarm → ADAS → AFlow → MaAS → ABSTRAL, then `auto_mas.py`.

**If you care about deployment-time learning:** Reflexion → EvoTest → TT-SI → TMEM → TAME.

**If you care about recursive self-improvement:** Gödel Agent → Darwin Gödel Machine → the RSI survey → Generalized Agent Iteration → AI4AI-Bench → *Auditing Harness Tampering*.

**If you care about evaluation:** the surveys' benchmark sections → StuLife → Evo-Memory → SkillFlow.

---

## Updates

A running log so you can see what changed without diffing. Newest first.

- **2026-09** — Added a [recursive self-improvement](#recursive-self-improvement) section (*Dream-RSI*, *ModularRSI*, *HELIX*, *Meta^n*, the Gödel-machine successors, and the 1,250-paper RSI survey), RSI benchmarks (*AI4AI-Bench*, *RSIBench-Data*, *PAST-Bench*, *Meta-Agent Challenge*, *S3Gym*), and the failure and safety work that came with them (*self-authored verification*, *harness tampering*, *skill misevolution*). Linked *Gödel Agent* and corrected its title. A second pass re-read every new description against its abstract and softened five that claimed more than the paper shows, moved *AREX* to test-time learning, linked the six remaining entries that had no link, and corrected the paper count, which had been counting bullet lines rather than papers.
- **2026-09** — Added three sections: [zero-data self-evolution](#zero-data-self-evolution-and-self-play) (*Absolute Zero*, *R-Zero*, *Tool-R0*), [self-evolving coding agents](#self-evolving-coding-agents) following the August survey, and [forgetting, drift, and stability](#forgetting-drift-and-stability) (*Do Self-Evolving Agents Forget?*, *anytime-valid certificates*, *SSGM*). Merged four community entries (*OpenSkill*, *RewardHarness*, *ForeDreamer*, *HAT*). Ran a link-verification pass over the whole list: every arXiv identifier now resolves to a paper whose title matches, one wrong title was corrected (the agentic-framework bug study), three more were corrected against arXiv metadata (*EvoMAS*, *Six Sigma Agent*, *ABSTRAL*), and the two entries with no paper are linked to their canonical repositories.
- **2026-07** — Community layer: [`COMMUNITY.md`](COMMUNITY.md) project board, [contributing guide](docs/contributing-guide.md), issue/PR templates, and spotlight strip above.
- **2026-07** — Initial public release: 90+ papers across 13 topics, four-pathway taxonomy, misevolution safety section, primer, and two runnable reference implementations.

> Watching the repo (top-right of the page) is the reliable way to get these — the `last-commit` badge above updates on every merge.

---

## How this list is maintained

A few notes on process, because a curated list is only as good as its upkeep:

- **Entries are read, not scraped.** Each one gets a single neutral sentence describing what the work *does*. If a description reads like a press release, it hasn't been reviewed yet — open an issue.
- **Links are checked, not guessed.** Every arXiv identifier in the list has been resolved against the arXiv API and its title compared with the entry's, so no link here is a guess. Where a work has no stable paper ID, the entry links its canonical repository instead; where neither exists, it is kept without a link and marked `needs-link` rather than given a fabricated one. No entry currently carries that marker.
- **The link policy is enforced by CI.** [`.github/workflows/link-check.yml`](.github/workflows/link-check.yml) re-resolves every arXiv identifier through the arXiv API, compares the returned title with the entry's, and requests every other link — on each pull request and once a month. A broken or mislabelled link fails the check.
- **Monthly review pass.** Roughly once a month the newest work is triaged into the taxonomy and the [Updates](#updates) log is appended. The date in the banner reflects the last pass.
- **Scope is enforced.** New sub-areas are added only when several papers justify them, to keep the list walkable rather than exhaustive. See [related lists](#related-lists) for wider, more encyclopedic coverage.

Found something wrong or missing? Corrections are the most welcome PRs of all — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Star history

<p align="center">
  <a href="https://star-history.com/#sukoji/awesome-self-evolving-agents&Date">
    <img src="https://api.star-history.com/svg?repos=sukoji/awesome-self-evolving-agents&type=Date" alt="Star history chart" width="620">
  </a>
</p>

---

## Related lists

This list is curated to be walkable rather than exhaustive; these go wider and are worth watching:

- [EvoAgentX/Awesome-Self-Evolving-Agents](https://github.com/ANative-Lab/Awesome-Self-Evolving-Agents) — companion to the *Comprehensive Survey*.
- [XMUDeepLIT/Awesome-Self-Evolving-Agents](https://github.com/XMUDeepLIT/Awesome-Self-Evolving-Agents) — companion to the *What/When/How/Where* survey.

If a paper here is mis-attributed or missing a stable link, that is on this list, not on those.

---

## Contributing

This list is maintained by the community. Pick your lane:

| Contribution | Where | How |
|---|---|---|
| **Paper** | `README.md` | [Suggest paper](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-paper.yml) or PR |
| **OSS project / benchmark** | [`COMMUNITY.md`](COMMUNITY.md) | [Suggest project](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-project.yml) or PR |
| **Fix** | either file | [Correction issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=correction.yml) — fastest merge |

Full walkthrough: [docs/contributing-guide.md](docs/contributing-guide.md) · rubric: [CONTRIBUTING.md](CONTRIBUTING.md) · conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

Short version: **one entry per PR**, one neutral sentence, verifiable link (or explicit `needs-link`), correct section/pathway tag.

## License

[CC0 1.0](LICENSE) for the list itself. The code under [`code/`](code/) is MIT — see [`code/LICENSE`](code/LICENSE).
