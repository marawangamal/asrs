## Topic
analysis
## Tags
topology
### Name
Open set
### Question
What is an open set?
### Answer
A set $U \subseteq \mathbb{R}^n$ is **open** if for every $x \in U$, there exists an $\epsilon > 0$ such that the open ball
$$
B(x, \epsilon) = \{ y : \|y - x\| < \epsilon \} \subseteq U.
$$

Intuition: every point of $U$ has some wiggle room — you can move a little in any direction and stay inside. Equivalently, $U$ is open iff it equals the union of all open balls it contains, iff its complement is closed.
