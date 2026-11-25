"""Worked solutions to the editor drills, using only the Python standard library."""
import math


def cross_entropy(logits, target):
    peak = max(logits)
    return (peak - logits[target]) + math.log(sum(math.exp(z - peak) for z in logits))


def merge_stats(left, right):
    n, mean, m2 = left
    k, other_mean, other_m2 = right
    if n == 0:
        return right
    if k == 0:
        return left
    delta = other_mean - mean
    total = n + k
    return total, mean + delta * k / total, m2 + other_m2 + delta**2 * n * k / total


def attention(query, keys, values, allowed):
    indices = [i for i, keep in enumerate(allowed) if keep]
    if not indices:
        return [0.0] * len(values[0])
    scale = math.sqrt(len(query))
    scores = [sum(x * y for x, y in zip(query, keys[i])) / scale for i in indices]
    peak = max(scores)
    weights = [math.exp(s - peak) for s in scores]
    denom = sum(weights)
    return [sum(w * values[i][j] for w, i in zip(weights, indices)) / denom
            for j in range(len(values[0]))]


def token_loss(rank_sums, rank_counts):
    count = sum(rank_counts)
    if not count:
        raise ValueError("no valid tokens")
    return sum(rank_sums) / count


def gae(rewards, values, next_values, terminated, episode_end, gamma, lam):
    advantages = [0.0] * len(rewards)
    tail = 0.0
    for t in reversed(range(len(rewards))):
        bootstrap = 0.0 if terminated[t] else gamma * next_values[t]
        delta = rewards[t] + bootstrap - values[t]
        tail = delta + (0.0 if episode_end[t] else gamma * lam * tail)
        advantages[t] = tail
    return advantages


def ppo_term(log_new, log_behavior, advantage, epsilon):
    ratio = math.exp(log_new - log_behavior)
    clipped = min(1 + epsilon, max(1 - epsilon, ratio))
    return min(ratio * advantage, clipped * advantage)


def dpo_loss(chosen, rejected, ref_chosen, ref_rejected, beta):
    margin = beta * ((chosen - ref_chosen) - (rejected - ref_rejected))
    return max(0.0, -margin) + math.log1p(math.exp(-abs(margin)))


def pass_at_k(n, c, k):
    if k > n - c:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def kv_bytes(lengths, layers, kv_heads, head_dim, bytes_per_element, block):
    slots = sum((length + block - 1) // block * block for length in lengths)
    return slots * 2 * layers * kv_heads * head_dim * bytes_per_element


def decoding_frontier(candidates, max_p99):
    feasible = [row for row in candidates if row[3] <= max_p99]
    frontier = []
    for name, quality, cost, _ in feasible:
        dominated = any(q >= quality and c <= cost and (q > quality or c < cost)
                        for _, q, c, _ in feasible)
        if not dominated:
            frontier.append(name)
    return frontier
