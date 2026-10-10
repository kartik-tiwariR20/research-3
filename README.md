# Title

## Where Does Shared LLM Failure Come From? A Lineage-Aware Analysis of Open-Weight Models for Voting and Verification

*Target venue: AAAI-27 workshop (open-source models only).

---

# 1. Basic idea

## 1.1 The one-minute version

Many AI systems today do not rely on one language model. They ask **several models** and combine the answers (**voting / ensembling**), or they ask a second model to **check** the first model's answer (**verification / LLM-as-judge**). The hope behind both is simple: *different models make different mistakes, so the mistakes cancel out.*

That hope only holds if the models really do make *different* mistakes. Research already shows that today's models often make the **same** mistakes. Our project asks the next question:

> **When several models fail together, why? Is it because the question is simply very hard for everyone, because the models belong to the same "family", or because they share the same "ancestry" (for example, one was trained on another's outputs)? And how much of the shared failure can we avoid just by choosing models more carefully?**

## 1.2 An everyday analogy

Imagine you form a committee of doctors to diagnose patients by majority vote.

- If the doctors are **independent** and each is right 70% of the time, a committee of five is right about **84%** of the time. Voting helps a lot.
- But suppose all five trained at the **same school** under the **same teacher**. They tend to make the same wrong diagnosis on the same tricky cases. The committee is hardly better than one doctor, and sometimes worse.
- Now suppose some cases are so unusual that **no doctor in the world** would get them right. No committee can fix those.

So a committee's failures come from three sources: (1) **cases that are hard for everyone**, (2) **shared training (same school)**, and (3) **shared teacher (lineage)**. We want to *measure each source separately* for language models. Sources (2) and (3) are the ones you can fix by choosing different doctors; source (1) you cannot.

## 1.3 What "family" and "lineage" mean here

- **Family:** models from the same developer line that share design and training recipe (for example, different sizes of the same model series).
- **Lineage:** a chain of influence. For example, a small model that was trained on the answers of a large "teacher" model inherits habits from that teacher, even if the small model's architecture comes from a different family. Lineage can cross family boundaries, which is exactly what makes it interesting to study.

## 1.4 What we will actually do (in plain steps)

1. **Choose a set of open-source models** (about twenty or more) covering several families, including some that were trained from a teacher model's outputs, so we know their ancestry.
2. **Ask every model the same set of questions** from standard benchmarks and record, for every question, whether each model was right or wrong (and which answer it gave).
3. **Compare pairs of models along a "relationship ladder"**: the same model run twice, a model and its own tuned version, same family different size, a student and its teacher, a student and its original base model, and two unrelated models. We measure how much more often related pairs fail together than unrelated pairs of the same accuracy.
4. **Fit a statistical model** that splits the shared failure into three parts: *difficulty of the question (everyone)*, *family effect*, and *lineage effect*. This tells us how much shared failure is "unavoidable" and how much is "buy-back-able" by choosing differently.
5. **Test whether that statistical model can predict**, for a team of models it has not seen, how often *all* models in the team are wrong (the hard ceiling on what any combination can achieve) and how accurate their vote would be.
6. **(Stretch goal) Do the same for verification**: measure how often a checker model wrongly approves a generator's wrong answer, and whether this depends on the checker being from the same family or lineage.

## 1.5 What a reader will take away

- A clear picture of **where shared failure comes from** in open models.
- A practical rule: **when changing the model family is worth it, and when no choice of models will help.**
- Open data and code (the table of right/wrong answers per model and question) so others can reuse the analysis.

---

# 2. Real problem

## 2.1 The problem in one paragraph

Companies and researchers build systems from several language models because it seems safer: "if one model is wrong, another will catch it." But if models share blind spots, the extra models add cost without adding safety, and worse, the system can look *more* confident (several models agree) while being wrong. Today people mostly choose which models to combine by popularity, price or intuition, without a reliable way to know in advance how much diversity they are actually getting.

## 2.2 A concrete numeric illustration (worked by hand)

Suppose a benchmark has two kinds of questions:

- **Easy questions (70% of the benchmark):** each model answers correctly with probability 0.95.
- **Hard questions (30%):** each model answers correctly with probability only 0.20.

Each model's overall accuracy is $0.7 \times 0.95 + 0.3 \times 0.20 = 72.5\%$.

Now take a team of **5 such models** and let the majority decide.

| What we compute | Value |
|---|---|
| Majority accuracy if the models were **independent** (each simply 72.5% right on every question) | about **86.8%** |
| Majority accuracy given the **real two-type structure** above | about **71.7%** |
| Accuracy of **one** model | **72.5%** |
| Accuracy with **infinitely many** such models voting | **70%** (just the easy questions) |
| Probability that **all 5** models are wrong on the same question, if independent | about **0.16%** |
| Probability that **all 5** are wrong given the real structure | about **9.8%** |

Two lessons: (1) the naive "independent" calculation is wildly optimistic (86.8% vs 71.7%); (2) here **adding voters does not help at all**, and slightly hurts, because on hard questions the *majority* is wrong, so voting amplifies the wrong answer. Also, since all five models are wrong together on about 9.8% of questions, **no router, voter or judge that picks one of these models' answers can exceed about 90%** accuracy.

(You can check these numbers with the formulas in Section 4.)

## 2.3 What goes wrong in practice

1. **Voting stops helping.** Adding more models gives diminishing or even negative returns.
2. **Verification gives false comfort.** If the checker comes from the same family as the generator, it tends to approve the same wrong answers it would have produced itself.
3. **Judging is biased.** A judge model prefers answers from similar models, so leaderboards judged by models can be skewed.
4. **Selection is guesswork.** Teams cannot predict, before paying for inference, how much a new model will add.
5. **Capability hides everything.** Strong models are right on the same easy questions, so they *look* similar even when they would fail differently. Naive similarity numbers mostly measure accuracy, not diversity.

## 2.4 What is still not well understood (our gap)

Prior work shows that shared failure exists, that it grows as models improve, that it caps ensembles, and that same-family checkers share blind spots. What remains unclear, and what we address, is:

- **How much of the shared failure is due to difficulty vs family vs lineage?** (Only the last two are fixable by choosing different models.)
- **Do models trained from a teacher's outputs inherit the teacher's mistakes, or their base model's?**
- **Can a model with family and lineage structure predict the "all models wrong" ceiling better than simpler models, for teams it has not seen?**
- **(Stretch) Do the theoretical formulas for correlated verifiers hold on real language models?**

---

# 3. History of work

## 3.1 Timeline

| Period | Idea or result | Why it matters for us | Label |
|---|---|---|---|
| 1785 | **Condorcet jury theorem**: majority vote of independent voters, each better than chance, becomes almost perfect as voters increase | The original reason "more voters is better" | [memory] |
| 1950s | Von Neumann: building reliable systems from unreliable parts | Origin of "redundancy improves reliability" thinking | [checked, via citation] |
| 1990s | **Correlated voters**: majority-vote results extended to voters whose errors are dependent (Ladha); **ambiguity decomposition** of ensemble error (Krogh and Vedelsby) | Shows that correlation caps the benefit of voting; ensemble gain = member accuracy + disagreement | [memory] |
| 1996 to 2001 | **Bagging and random forests** (Breiman): ensemble error depends on both the strength of members and the correlation between them | The strength-vs-correlation trade-off | [memory] |
| 2000 to 2005 | Surveys and measures of **ensemble diversity** (Dietterich; Kuncheva and Whitaker; Brown et al.). Finding: common diversity measures relate only weakly to ensemble accuracy | Warns that "diversity" is hard to measure usefully | [checked, via citation] |
| 2020 | **Error consistency** between neural networks (Geirhos et al.): a chance-corrected agreement measure | A template for chance-adjusted comparison | [memory] |
| 2022 to 2024 | LLM era: **self-consistency** (sample several answers and vote), **multi-agent debate**, **mixture-of-agents**, "more agents is all you need", **LLM-Blender**; also doubts: LLMs cannot reliably self-correct reasoning without outside feedback; LLM judges favor their own outputs | Voting and checking become mainstream, together with first signs of trouble | [checked and memory] |
| 2023 | **Unified theory of ensemble diversity** (Wood et al.) | A rigorous framework: diversity helps only when managed against accuracy | [checked, via citation] |
| 2024 | "**Tyranny of the majority**" in debate (Estornell and Liu): correlated agents can lock in a wrong answer | Early evidence of correlated errors in agent systems | [checked, via citation] |
| 2025 (Feb) | **Great Models Think Alike** (Goel et al., ICML 2025): a chance-adjusted similarity metric from shared mistakes; judges favor similar models; mistakes become more similar as capability grows | Core prior work on similarity and oversight | [checked] |
| 2025 (Jun) | **Correlated Errors in LLMs** (Kim et al., ICML 2025): 350+ models; models often agree on the same wrong answer; more accurate models are more correlated; shared architecture and provider matter | Core prior work on measuring correlation at scale | [checked] |
| 2025 | **Self-Correction Bench** (Tsui): models fail to fix their own errors that they can fix when attributed to someone else (about 64.5% blind-spot rate across 14 open models) | Evidence of verifier blind spots on the generator's own errors | [checked, via citation] |
| 2025 (Dec) | **When Does Verification Pay Off?**: cross-family verification beats self and same-family verification; benefit falls as solver and verifier become more similar | Core prior work for the verification side | [checked] |
| 2026 | **Co-failure ceiling** (Chen): accuracy of any policy that returns one member's answer is at most one minus the all-models-wrong rate; average pairwise correlation cannot identify that rate | The key ceiling result we build on | [checked] |
| 2026 | **Predictive law of ensemble lift** (Ali): adjusted correlation predicts two-model ensemble gain on ten open-weight models; vote corpus released | Closest "prediction" work; a free pilot dataset | [checked] |
| 2026 | **Capability-controlled audit of diversity metrics** (D. Kim): most diversity statistics mainly re-express capability; only a modest residual shared-failure effect remains | Shows why capability must be controlled | [checked, read in full] |
| 2026 | **Partially correlated verifier cascades** (Han): theory with a blind-spot ceiling, validated on synthetic data | Gives formulas and a measurement protocol for verification | [checked, read in full] |
| 2026 | Debate vs matched voting in small models; selection vs voting in multi-agent pipelines; verification coupling in medical VQA; others | Supporting evidence: most debate benefit is the ensemble effect | [checked] |

## 3.2 The storyline in plain words

First, people believed more voters means more accuracy (Condorcet). Then statisticians showed that this only works when voters err independently. Machine learning built diversity measures to track independence, but they turned out to be only loosely related to results. With language models, the same belief returned (use many models, add a judge), and the last two years of research showed that language models' errors are strongly shared, that the sharing grows with capability, and that it creates hard ceilings for voting and checking. Our project takes the next step: **explain where the sharing comes from and what can be avoided.**

---

# 4. Complete theory

*This section builds the theory from scratch. Every step has a plain explanation and a formula.*

## 4.1 Setup and notation

- **Questions (items)** $x = 1, \dots, N$, each with a correct answer $y(x)$.
- **Models** $k = 1, \dots, K$, each giving answer $a_k(x)$.
- **Correctness indicator** $Z_{kx} = 1$ if model $k$ is right on question $x$, else $0$. **Error indicator** $E_{kx} = 1 - Z_{kx}$.
- **Accuracy** $p_k = \frac{1}{N}\sum_x Z_{kx}$, **error rate** $e_k = 1 - p_k$.

Everything below is about how the error indicators of different models relate to each other.

## 4.2 Why independence makes voting powerful (Condorcet)

If $K$ (odd) models are independent and each is right with probability $p$, the chance that the majority is right is

```math
A_K = \sum_{m=(K+1)/2}^{K} \binom{K}{m} p^m (1-p)^{K-m}.
```

**Example:** $K = 5$, $p = 0.7$: $A_5 = 10(0.7)^3(0.3)^2 + 5(0.7)^4(0.3) + (0.7)^5 \approx 0.309 + 0.360 + 0.168 = 0.837$. As $K \to \infty$, $A_K \to 1$ whenever $p > 1/2$.

**Plain meaning:** if mistakes are random coin flips, enough voters wash them out.

## 4.3 How correlation breaks this

Suppose all pairs of models have the same error correlation $\rho$. Then the average of $K$ correctness indicators has variance

```math
\mathrm{Var}\!\left(\tfrac1K\textstyle\sum_k Z_k\right)=\frac{p(1-p)}{K}\bigl[1+(K-1)\rho\bigr].
```

Define the **effective number of independent voters**

```math
K_{\text{eff}}=\frac{K}{1+(K-1)\rho}\;\longrightarrow\;\frac1\rho\quad(K\to\infty).
```

**Plain meaning:** with correlation $\rho=0.3$, even infinitely many models are worth only about $3.3$ independent ones. (This is a rule of thumb about averaging; majority vote is a tail event, so treat $K_{\text{eff}}$ as a guide, not an exact law.)

## 4.4 The "question difficulty" model and the voting ceiling

A very natural way correlation arises: **some questions are just harder.** Let $\theta(x)$ be the probability that a randomly chosen model from the population answers question $x$ correctly. Assume that, *given the question*, models err independently with this probability. Then:

- Average accuracy: $p = \mathbb{E}[\theta(x)]$.
- Correlation between two models' correctness: $\mathrm{Cov}(Z_i, Z_j) = \mathrm{Var}(\theta)$, so $\rho = \mathrm{Var}(\theta)/\bigl(p(1-p)\bigr)$.
- Majority-vote accuracy of $K$ models:

  ```math
  A_K=\mathbb{E}_x\Bigl[\Pr\bigl(\mathrm{Bin}(K,\theta(x))>K/2\bigr)\Bigr].
  ```

- As the number of voters grows:

  ```math
  \boxed{A_\infty=\Pr_x\bigl(\theta(x)>\tfrac12\bigr)}
  ```

**Plain meaning:** the best a voting team can ever do is the share of questions on which *most models in the population are right*. On questions where most models are wrong ($\theta<1/2$), more voting just makes the wrong answer win more reliably.

**Check with Section 2.2:** $\theta = 0.95$ on 70% of questions and $0.20$ on 30%. Then $p=0.725$, $\mathrm{Var}(\theta)=0.1181$, $\rho = 0.1181/(0.725\times 0.275)\approx 0.59$, so $1/\rho \approx 1.7$ effective voters; and $A_\infty = 0.70$. Accuracy goes $72.5\% \to 71.7\%$ (five voters) $\to 70\%$ (infinite voters): *more voters, lower accuracy.*

(If $\theta\sim\text{Beta}(a,b)$, then $\rho=1/(a+b+1)$, a convenient formula for simulations.)

## 4.5 The hard ceiling for any combination method: the all-wrong rate

Let $\beta$ be the probability that **every** model in the team is wrong on the same question:

```math
\beta = \Pr\bigl(E_1 = E_2 = \cdots = E_K = 1\bigr).
```

Any method that outputs one of the models' answers (voting, routing, a judge choosing among them, mixture-of-agents selecting one) has accuracy at most $1-\beta$. This ceiling is policy-independent. Importantly, **average pairwise correlation does not determine $\beta$**: different dependence structures with the same pairwise correlations can have different $\beta$. So $\beta$ must be modeled or measured directly.

If models were independent, $\beta=\prod_k e_k$. In Section 2.2's example this is $0.275^5\approx 0.16\%$, while the real value is about $9.8\%$.

## 4.6 Multi-answer questions: correct answers agree, wrong answers may scatter

For a question with several options, models that are wrong can pick *different* wrong answers. Then plurality voting can still succeed. What breaks voting is **agreement on the same wrong answer**. So we must track two things:

1. **Correlation of correctness** (do they fail on the same questions?), and
2. **Wrong-answer agreement**: $A^{\text{wrong}}_{ij} = \Pr\bigl(a_i(x) = a_j(x) \mid \text{both wrong}\bigr)$. For a 4-option question with uniformly random wrong picks, the chance baseline is $1/3$; observed values far above that mean shared mistakes are *the same* mistakes.

## 4.7 Measuring similarity fairly (capability-adjusted overlap)

Two accurate models agree a lot simply because both are correct on easy questions. To measure *shared mistakes*, we use error-focused, accuracy-adjusted measures.

- **Double-fault:** $\mathrm{DF}_{ij}=\Pr(E_i=1,E_j=1)$.
- **Excess co-failure:** $\mathrm{Cov}(E_i,E_j)=\mathrm{DF}_{ij}-e_ie_j$ (how much more often they fail together than independence predicts).
- **Phi correlation:** $\phi_{ij}=\mathrm{Cov}(E_i,E_j)/\sqrt{e_i(1-e_i)e_j(1-e_j)}$.
- **Adjusted phi:** $\phi^{\text{adj}}_{ij}=\phi_{ij}/\phi^{\max}_{ij}$ where, for $a=\min(e_i,e_j)$ and $b=\max(e_i,e_j)$, the largest phi possible given the two error rates is $\phi^{\max}=\sqrt{\dfrac{a(1-b)}{b(1-a)}}$. (This removes the part of phi that is forced by the two models having different accuracies.)
- **Chance-adjusted agreement (kappa style):** $\kappa_{ij}=(c_{\text{obs}}-c_{\exp})/(1-c_{\exp})$ with $c_{\text{obs}}=\Pr(Z_i=Z_j)$ and $c_{\exp}=p_ip_j+(1-p_i)(1-p_j)$.
- **CAPA** (from earlier research): a probabilistic, chance-adjusted similarity based on mistake overlap; we will use the authors' definition and code.

## 4.8 Where shared failure comes from (mechanisms we can test)

1. **Hard, ambiguous or mislabeled questions** (everyone fails). Note: a mislabeled question makes every *correct* model look wrong, creating fake shared failure.
2. **Shared pretraining data** (overlapping web text, benchmark leakage).
3. **Shared architecture and training recipe** (family).
4. **Learning from a teacher's outputs** (distillation and synthetic data), which can pass mistakes along (lineage).
5. **Similar instruction tuning or reinforcement learning**, which can make styles and errors converge.
6. **Prompt format**, for example multiple-choice vs free-response answer formats.
7. **Capability convergence:** as models saturate a benchmark, remaining errors concentrate on the hardest or noisiest items.

## 4.9 Verification theory: why a checker from the same family is weaker

Let $C=1$ mean the generator's answer is correct, with prior $p_0=\Pr(C=1)$. A verifier either accepts or rejects. Its **true-accept rate** is $\beta_v=\Pr(\text{accept}\mid C=1)$ and its **false-accept rate** on a *particular wrong answer* $x$ is $\alpha(x)=\Pr(\text{accept}\mid C=0,x)$.

- If $k$ gates are **conditionally independent** with constant false-accept rate $\bar\alpha$ and accept all correct answers, the reliability of an answer passed by all $k$ gates is

  ```math
  r_k=\frac{p_0}{p_0+(1-p_0)\bar\alpha^{\,k}},
  ```

  and failure falls **exponentially** in $k$.
- If false-accept rates differ across wrong answers, $\alpha\sim G$, with moments $m_k=\mathbb{E}[\alpha^k]$, then (under the assumption that gates are exchangeable given the answer)

  ```math
  r_k=\frac{p_0}{p_0+(1-p_0)\,m_k}.
  ```

  Because answers with $\alpha$ near 1 survive many gates, failure falls only **polynomially**. The correlation between two verdicts on a wrong answer is

  ```math
  \rho_v=\frac{\mathrm{Var}(\alpha)}{\bar\alpha(1-\bar\alpha)}\quad(\,=1/(a+b+1)\text{ if }\alpha\sim\mathrm{Beta}(a,b)\,).
  ```

- If a fraction $1-\pi$ of wrong answers is *never caught* (a **blind-spot mass** at $\alpha=1$), reliability saturates below 1:

  ```math
  r_\infty=\frac{p_0}{p_0+(1-p_0)(1-\pi)}<1.
  ```

**Worked example (from the theory's source and rechecked by hand):** $p_0=0.5$, $\bar\alpha=0.3$, $\rho_v=0.3$ (so $a=0.7$, $b\approx1.63$). The independence formula claims $r_5=99.8\%$; the correlated formula gives $r_5=1/(1+m_5)$ with $m_5=\prod_{j=0}^{4}\frac{a+j}{a+b+j}\approx0.049$, i.e. $r_5\approx95.3\%$. Failure is underestimated about twentyfold at five gates.

**Plain meaning:** the answers a verifier misses are not random. They are the answers that look right to that verifier, and a same-family generator produces exactly those. Adding more gates from the same family keeps meeting the same blind spots.

## 4.10 Our central modeling idea: separate difficulty, family and lineage

We model the probability that model $k$ answers question $x$ correctly with a **multilevel (hierarchical) logistic model**:

```math
\operatorname{logit}\Pr(Z_{kx}=1)=\mu+w_k+u_x+v_{f(k),x}+r_{\ell(k),x},
```

where $f(k)$ is the family and $\ell(k)$ the lineage of model $k$, and

- $w_k\sim N(0,\sigma_w^2)$: **model ability** (a stronger model is right more often everywhere);
- $u_x\sim N(0,\sigma_u^2)$: **question difficulty shared by everyone**;
- $v_{f,x}\sim N(0,\sigma_f^2)$: **extra difficulty shared within a family** (family blind spots);
- $r_{\ell,x}\sim N(0,\sigma_\ell^2)$: **extra difficulty shared within a lineage** (inherited blind spots).

On the latent (logit) scale, the covariance between two models' tendencies on the same question is:

| Two models are... | Shared variance |
|---|---|
| unrelated (different family, different lineage) | $\sigma_u^2$ |
| same family, different lineage | $\sigma_u^2+\sigma_f^2$ |
| different family, same lineage (for example a distilled student of another family's teacher) | $\sigma_u^2+\sigma_\ell^2$ |
| same family and same lineage | $\sigma_u^2+\sigma_f^2+\sigma_\ell^2$ |

**The number we really care about** is the share of shared failure that **switching to a different family and lineage can remove**:

```math
\mathcal A=\frac{\sigma_f^2+\sigma_\ell^2}{\sigma_u^2+\sigma_f^2+\sigma_\ell^2}.
```

If $\mathcal A$ is large, diversification pays; if it is small, the problem is in the questions themselves and the remedy must come from elsewhere (tools, retrieval, executable checks, human review).

---

# 5. Mathematical formulation (exactly what we will compute)

## 5.1 Data

- A roster of $K$ open-weight models with recorded **family** $f(k)$, **lineage** $\ell(k)$, size, and type (base, instruct, reasoning, distilled student).
- Benchmarks of $N$ questions each, in two answer formats where possible (multiple choice and free-response).
- Output: the **correctness matrix** $Z\in\{0,1\}^{K\times N}$ and the **answer matrix** $a_k(x)$.

## 5.2 Experiment 1: the relationship ladder (descriptive)

For each relationship type $r$ in the ladder:

1. same model, different seed or temperature,
2. base model vs its own instruct version,
3. same family, different size,
4. distilled student vs its teacher,
5. distilled student vs the instruct version of its own base,
6. unrelated models (different family and lineage),

form the set $\mathcal P_r$ of model pairs and compute

```math
\Omega_r=\frac{1}{|\mathcal P_r|}\sum_{(i,j)\in\mathcal P_r}\phi^{\text{adj}}_{ij}.
```

To keep capability from confounding the comparison, we also report $\Omega_r$ restricted to accuracy-matched pairs (accuracy difference below a preset tolerance). Uncertainty comes from **bootstrapping the questions** (not the model pairs, since pairs sharing a model are not independent).

## 5.3 Experiment 2: variance decomposition

Fit the model of Section 4.10 with a Bayesian multilevel logistic regression. Report posterior means and credible intervals for $\sigma_u^2$, $\sigma_f^2$, $\sigma_\ell^2$, $\sigma_w^2$, the share $\mathcal A$, and the **latent intraclass correlations**

```math
\mathrm{ICC}_{\text{univ}}=\frac{\sigma_u^2}{\sigma_u^2+\sigma_f^2+\sigma_\ell^2+\pi^2/3},\quad \mathrm{ICC}_{\text{fam}}=\frac{\sigma_f^2}{\sigma_u^2+\sigma_f^2+\sigma_\ell^2+\pi^2/3},
```

and similarly for lineage ($\pi^2/3$ is the logistic residual variance).

**Identifiability requirement:** family and lineage effects can only be separated if the roster has (a) at least two models per family, and (b) distilled models whose teacher belongs to a different family than their base. The roster is designed around this.

**Simulation check before collecting data:** simulate correctness matrices from the model with known variances at the planned numbers of models, families and questions, fit them, and confirm the variances are recovered with acceptable error.

## 5.4 Experiment 3: predicting the ceiling for unseen teams

For a team $S$ of models, the model implies

```math
\beta_S=\mathbb{E}_{u,v,r}\Bigl[\prod_{k\in S}\bigl(1-\sigma(\mu+w_k+u+v_{f(k)}+r_{\ell(k)})\bigr)\Bigr],
```

where $\sigma(\cdot)$ is the logistic function and the expectation is over the random effects (computed by simulation). Majority accuracy $A_S=\Pr(\text{more than half of }S\text{ correct})$ is obtained the same way.

**Baselines to beat:**

- **Independence:** $\beta_S=\prod_{k\in S}e_k$.
- **Single-factor copula (one shared "difficulty" for everyone):** with latent $L_k=\sqrt{\rho}\,\xi+\sqrt{1-\rho}\,\varepsilon_k$ ($\xi,\varepsilon_k$ standard normal) and model $k$ wrong when $L_k\le t_k=\Phi^{-1}(e_k)$,

  ```math
  \beta_S=\mathbb{E}_\xi\Bigl[\prod_{k\in S}\Phi\!\Bigl(\tfrac{t_k-\sqrt\rho\,\xi}{\sqrt{1-\rho}}\Bigr)\Bigr],
  ```

  with $\rho$ calibrated from tetrachoric correlations.
- **Effective voters:** $K_{\text{eff}}=K/(1+(K-1)\bar\rho)$ from average pairwise correlation.
- **Adjusted pairwise correlation** and **CAPA / double-fault** summaries.

**Held-out evaluation:** leave one *family* out (and separately one *lineage* out), fit on the rest, predict $\beta_S$ and $A_S$ for teams that include the held-out models (their family and lineage effects drawn from the fitted prior), and compare to the observed values. The error metric is $|\hat\beta_S-\beta_S^{\text{obs}}|$ and $|\hat A_S-A_S^{\text{obs}}|$ with bootstrap intervals.

## 5.5 Experiment 4 (stretch): verification on real models

For a generator $G$ and a verifier family $F$ (several models per family, plus an executable checker as a control):

1. Take **$G$'s own wrong answers** as the test population.
2. For each wrong answer $i$, collect $R$ verdicts (from verifiers sampled from the family, or repeated sampling of one verifier), giving $X_i\sim\mathrm{Bin}(R,\alpha_i)$.
3. Estimate $\bar\alpha=\frac1n\sum_i X_i/R$ and the second moment

   ```math
   \hat m_2=\frac1n\sum_i\frac{X_i(X_i-1)}{R(R-1)},\qquad \hat\rho_v=\frac{\hat m_2-\bar\alpha^2}{\bar\alpha(1-\bar\alpha)}.
   ```

4. Fit $G=\pi\,\mathrm{Beta}(a,b)+(1-\pi)\,\delta_1$ to estimate the **blind-spot mass** $1-\pi$.
5. **Falsification test:** fit on cascades of up to $k=3$ gates, predict reliability for $k=6$ to $8$ real cascades, and compare to the independence extrapolation.

## 5.6 Hypotheses (written down before looking at data)

| ID | Statement | What a result means |
|---|---|---|
| H1a | Capability-adjusted overlap $\Omega_r$ decreases along the ladder (closer relationships overlap more). | Supports that relationship drives shared failure. |
| H1b | A distilled student's errors overlap more with its teacher than with its base model's instruct version (or the reverse; we test both directions). | Tells us whether lineage or base pretraining dominates inherited mistakes. |
| H2 | $\sigma_f^2$ and $\sigma_\ell^2$ exceed a pre-set smallest effect of interest. | Family and lineage add shared failure beyond question difficulty. |
| H2b | The universal-difficulty share is larger in free-response than in multiple-choice format. | Answer format moves the all-wrong tail. |
| H3 | The multilevel model has lower held-out error for $\beta_S$ and $A_S$ than the single-factor and pairwise baselines. | Structure helps prediction beyond a single shared-difficulty factor. |
| H4a (stretch) | Same-family or same-lineage verifiers show larger blind-spot mass than cross-family verifiers at matched verifier accuracy. | Direct evidence on why same-family checking is weak. |
| H4b (stretch) | Low-order fits extrapolate to deeper cascades better than the independence formula. | Validates the correlated-verifier theory on real models. |
| H4c (control) | An executable checker has near-zero blind-spot mass on code and exact-answer math. | Confirms the measurement works. |

A null or reversed result is still a result: for example "family adds nothing beyond difficulty" would redirect practice toward other remedies.

## 5.7 Experimental design details

- **Models:** at least 20 open-weight models across at least 6 families (for example Llama, Qwen, Gemma, Mistral, DeepSeek, Phi, OLMo; verify availability), at least two models per family, base and instruct versions, 4 to 6 distilled students with documented teacher and base, one fully open-data family for contamination checks. Keep main-analysis sizes comparable.
- **Benchmarks:** MMLU-Pro (multiple choice); GPQA-Diamond in both multiple-choice and free-response form; MATH or GSM8K (exact answer); HumanEval+/MBPP+ (executable tests). Prefer cleaned or re-annotated subsets to reduce label noise.
- **Decoding:** fixed prompts, greedy or low temperature for the main run; a sampled-decoding ablation.
- **Controls:** accuracy matching; compute matching against single-model self-consistency; label-noise audit; answer-extraction audit (parsing errors create fake shared failure); contamination check; logging of truncated outputs for long-reasoning models; multiple prompt templates and seeds.
- **Pilot:** debug the metrics and the multilevel fit on an existing public vote corpus of ten open-weight models before any new inference (check its licence and contents).
- **Compute:** inference only. A single modern GPU with an efficient serving engine is workable for models in the 7B to 14B range; long-reasoning models dominate cost and need a separate budget.

## 5.8 Deliverables (what the final paper will contain)

1. **Figure 1:** the relationship ladder (adjusted overlap by relationship type, with intervals).
2. **Figure 2:** variance components and the "avoidable share" $\mathcal A$ per benchmark and format.
3. **Figure 3:** predicted vs observed all-wrong rate $\beta_S$ for held-out teams, for our model and each baseline.
4. **Table 1:** held-out prediction errors of all methods.
5. **(Stretch) Figure 4:** blind-spot mass by verifier relationship, and extrapolation test.
6. **Released data:** correctness and answer matrices, roster metadata, and analysis code.

## 5.9 Plan (about 6 to 8 weeks; check each workshop's actual deadline)

- Week 0-1: literature check, roster and benchmark choice, pilot.
- Week 1-2: run inference and build the matrices.
- Week 3: ladder analysis.
- Week 4: variance decomposition and simulation recovery.
- Week 5: held-out prediction against baselines.
- Week 6: writing (stretch: verification pilot).
- Week 7-8: audits, re-check the literature, finalize.

---

# 6. Previous research work to revisit

*Read these before starting. For each: what it did, what to take from it, and how our work differs. Labels show how well I verified it; confirm details before citing.*

## 6.1 Must-read (closest to our work)

| # | Paper | What it did | What to take | How we differ | Label |
|---|---|---|---|---|---|
| 1 | **Kim, Garg, Peng, Garg. Correlated Errors in Large Language Models** (ICML 2025; arXiv 2506.07962) | Measured error overlap across 350+ models; models often agree on the same wrong answer (about 60% on one leaderboard, against a 1/3 chance baseline); shared architecture and provider matter; more accurate models are more correlated; effects on LLM-as-judge and hiring | Datasets, the wrong-answer-agreement measure, the chance baseline | We decompose item-level variance into difficulty, family and lineage rather than only regressing pairwise overlap | [checked] |
| 2 | **Goel et al. Great Models Think Alike and this Undermines AI Oversight** (ICML 2025; arXiv 2502.04313) | CAPA similarity from shared mistakes; judges favor similar models; weak-to-strong gains depend on complementary knowledge | CAPA definition and code; capability-trend finding | We study sources of similarity (family, lineage) and ensemble ceilings rather than oversight bias | [checked] |
| 3 | **Chen. When Does Combining Language Models Help? A Co-Failure Ceiling...** (arXiv 2606.27288) | Ceiling: accuracy at most one minus the all-wrong rate; pairwise correlation cannot identify it; a single-factor model underprices the all-wrong tail across 67 models; free-response format reopens the tail | The ceiling statement, the single-factor baseline, the format experiment | We add family and lineage structure and open-weight natural experiments, and test held-out prediction | [checked, abstract level] |
| 4 | **Ali. Quantifying Diversity of Thought: A Predictive Law of Weighted LLM Ensemble Lift** (arXiv 2607.17384) | Exact decomposition of two-model ensemble lift into "rescue" and "damage"; adjusted phi predicts lift; ten open-weight models; vote corpus released | Adjusted-phi baseline; the released corpus for piloting | We target pool-level ceilings and sources of failure, not pairwise lift | [checked, abstract level] |
| 5 | **D. Kim. Are Diversity Metrics Measuring Diversity?** (arXiv 2607.20768) | 30 mostly API models; most diversity statistics re-express capability; modest residual shared-failure effect; weak held-out prediction | Capability-control procedures; algebraic identities among contingency-table measures; warnings about overlapping subsets | Open-weight roster with lineage, multilevel model, held-out prediction, optional verification | [checked, read in full] |
| 6 | **Han. Partially Correlated Verifier Cascades in LLM Harnesses** (arXiv 2607.13918) | Latent false-accept theory, polynomial reliability, blind-spot ceiling, measurement protocol; synthetic validation | The formulas of Section 4.9 and the estimation protocol of Section 5.5 | We test the theory on real generator-verifier pairs by family and lineage | [checked, read in full] |
| 7 | **When Does Verification Pay Off? A Closer Look at LLMs as Solution Verifiers** (arXiv 2512.02304) | Self vs same-family vs cross-family verification; benefit decreases with similarity | Experimental design for verifier comparisons | We measure latent blind-spot structure rather than only accuracy gains | [checked, snippet level] |

## 6.2 Supporting work

| Paper | Why revisit | Label |
|---|---|---|
| Beyond Symmetric Agents: Cognitive Diversity and Multi-Agent Debate in Small Language Models (arXiv 2609.35875) | Compute-matched comparison of debate vs voting across 23 models; good methodological template; warns about silently truncated transcripts | [checked] |
| When Agents Disagree: The Selection Bottleneck in Multi-Agent LLM Pipelines (arXiv 2603.20324) | Diversity helps under judge selection but not under majority voting | [checked] |
| Talk Isn't Always Cheap: Failure Modes in Multi-Agent Debate (arXiv 2509.05396) | Debate can underperform voting; groups converge on wrong answers | [checked] |
| Verification Mirage (arXiv 2605.10850); Cheap Verifiers, Large Blind Spots (arXiv 2609.01345); LLMs as a Jury (arXiv 2607.10139) | Empirical verifier coupling, blind-spot rates, and cross-model consensus signals | [checked, snippets] |
| Tsui. Self-Correction Bench | Origin of the blind-spot measurement on injected vs own errors | [checked, via citation] |
| Diversity Matters: Revisiting Test-Time Compute in Vision-Language Models (arXiv 2605.30713) | Simple copy-the-same-wrong-answer coupling model for voting | [checked] |
| Quantifying Correlations of Machine Learning Models (arXiv 2502.03937) | Error-correlation measurement beyond LLMs | [checked] |
| Kohli (2026), Nine judges, two effective votes; Aksu (2026), Odds Law; Liu (2026), voting moment papers | Cited inside the verifier-theory paper; relevant to effective votes and verification algebra; not opened | [checked, via citation] |

## 6.3 Classical foundations

| Work | Why revisit | Label |
|---|---|---|
| Condorcet jury theorem; Ladha on correlated voters (de Finetti view) | Origin of the voting ceiling | [memory] |
| Krogh and Vedelsby (ambiguity decomposition); Breiman (bagging, random forests) | Strength-correlation trade-off | [memory] |
| Dietterich (2000); Kuncheva and Whitaker (2003); Brown et al. (2005); Wood et al. (2023) | Diversity measures and theory; why they relate weakly to accuracy | [memory and checked via citation] |
| Geirhos et al. (2020), error consistency | Chance-corrected agreement template | [memory] |
| Gema et al., MMLU-Redux (re-annotated MMLU) | Evidence of label errors in benchmarks; use for label-noise control | [memory] |
| Self-consistency (Wang et al.), multi-agent debate (Du et al.), mixture-of-agents (Wang et al.), "Rethinking Mixture-of-Agents" (Li et al.), LLM-Blender (Jiang et al.), "LLMs cannot self-correct reasoning yet" (Huang et al.) | The methods whose limits we study | [memory and checked via citation] |

## 6.4 What to replicate first (to validate your pipeline)

1. **Wrong-answer agreement vs the 1/3 chance baseline** (Kim et al.): confirms your correctness and answer extraction.
2. **All-wrong rate $\beta$ and single-factor underestimation** (Chen): confirms your ceiling computation.
3. **Adjusted-phi relation to two-model lift** (Ali): confirms your ensemble code.
4. **Partial correlation of double-fault with voting gain after capability control** (D. Kim): confirms your capability controls.
5. **Synthetic recovery of verifier moments** (Han): confirms the stretch pipeline before touching real models.

## 6.5 Positioning statement (for the paper)

Prior work establishes that LLM errors are correlated, that correlation grows with capability, that it caps voting and routing, and that same-family verifiers share blind spots. We do not claim to rediscover these. Our contribution is to **attribute** shared failure to question difficulty, model family and model lineage on open-weight models, to use distillation relationships as natural experiments, and to test whether this structure predicts the all-wrong ceiling for unseen teams better than single-factor and pairwise baselines.

**Honest note on novelty:** this area produces new preprints almost monthly. Before starting and again one week before submission, search for newer work that already attributes shared failure to family or lineage, and check who cites the papers in Section 6.1.

---

# Glossary (plain language)

- **Ensemble / voting:** combining several models' answers, usually by majority.
- **Verification / LLM-as-judge:** using a model to check another model's answer.
- **Correlated errors:** different models being wrong on the same questions.
- **Independent errors:** each model's mistakes are unrelated to the others'.
- **Family:** models from the same development line.
- **Lineage:** chain of influence, for example a student trained on a teacher's outputs.
- **Distillation:** training a smaller model to imitate a larger model's outputs.
- **All-wrong rate ($\beta$):** share of questions on which every model in the team is wrong.
- **Ceiling:** the best any method that picks one team member's answer can achieve, namely $1-\beta$.
- **Blind-spot mass:** share of wrong answers that a checker never catches.
- **Capability-adjusted:** compared after accounting for the models' different accuracy levels.
- **Hierarchical / multilevel model:** a statistical model with several layers of shared effects (question, family, lineage, model).
- **Variance component:** how much of the variation is due to one layer (for example, how much comes from family).
- **Held-out prediction:** predicting results for models or families the fitting procedure did not see.
- **Open-weight model:** a model whose trained parameters are publicly downloadable.
