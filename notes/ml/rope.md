## Topic

transformers

## Tags

rope,rotary-position-embedding,attention,positional-encoding,relative-position

### Name

RoPE injects position through rotations

### Question

Mathematically, how does RoPE inject position information into attention, and why does the attention score depend on relative position?

### Answer

RoPE injects position by changing the geometry of the query and key vectors: it rotates them by position-dependent rotation matrices.

Without RoPE, attention uses:

$$
q_m^\top k_n
$$

With RoPE, the query at position $m$ and the key at position $n$ are rotated:

$$
(R_m q_m)^\top (R_n k_n)
$$

where $R_m$ and $R_n$ are rotation matrices depending on positions $m$ and $n$.

The key identity is:

$$
(R_m q_m)^\top (R_n k_n)
=

q_m^\top R_m^\top R_n k_n
$$

For rotation matrices, the inverse rotation by $m$ followed by the rotation by $n$ gives a relative rotation:

$$
\boxed{
R_m^\top R_n = R_{n-m}
}
$$

Therefore:

$$
(R_m q_m)^\top (R_n k_n)
=

q_m^\top R_{n-m} k_n
$$

So the attention score depends on position only through the relative offset $n-m$, not the absolute positions $m$ and $n$ separately.

Intuitively, RoPE lets attention learn relative relationships like “attend 5 tokens back,” which helps with length extrapolation compared with purely absolute position encodings.
