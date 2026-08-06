# Problem map for Erdős Problem #409

## Definition

Let

$$
T(n)=\varphi(n)+1.
$$

For prime $p$, set $F(p)=0$. For composite $n$, define

$$
F(n)=1+F(T(n)).
$$

Since $\varphi(n)+1<n$ for composite $n>2$, every positive-integer trajectory strictly decreases until it reaches a prime.

## Question 1: stopping times and upper bounds

The first question asks how many iterations may be required. The current repository contributes explicit lower-bound witnesses:

$$
F(6{,}668{,}696{,}999)=71.
$$

This proves $\sup_n F(n)\ge71$. It does not determine whether $F$ is bounded, what the correct asymptotic upper bound is, or whether larger records already exist elsewhere.

Two computational directions are represented here:

- **forward exploration**, which evaluates many starting values and records long trajectories;
- **inverse extension**, which solves $\varphi(x)=y-1$ to prepend one step to an already certified trajectory.

## Question 2: infinitely many starts with a common terminal prime

All four certified record witnesses in this repository terminate at

$$
9{,}500{,}401.
$$

That gives several explicit starts in one basin, but finitely many examples do not address infinitude. The exact rooted inverse tree is useful local data for this question because it records a finite portion of the backward basin. Its extinction at the next level concerns only that rooted branch.

A proof of infinitude would require a construction producing infinitely many distinct predecessors or an infinite family entering the basin by another mechanism. A proof of finiteness would require a global obstruction, not a finite search cutoff.

## Question 3: density of a fixed basin

The current packet contains no density theorem. A finite census can estimate finite-range frequencies, but asymptotic density requires analysis controlling all sufficiently large starting values.

Computational experiments relevant to density should record at least:

- the sampled interval and whether it was exhaustive or random;
- the terminal-prime counts;
- stopping-time distributions;
- code and exact seeds;
- uncertainty or deterministic coverage;
- a clear distinction between empirical frequency and asymptotic density.

## Relationship among the questions

Long-record construction studies deep paths in the functional graph. Basin-infinitude studies the size of a backward component. Density studies the asymptotic proportion of vertices entering that component. They use related data structures, but success on one question does not automatically resolve the others.
