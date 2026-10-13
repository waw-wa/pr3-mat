import os
import random
import matplotlib.pyplot as plt

# Створюємо каталог для збереження графіків
os.makedirs("graphics", exist_ok=True)

# ==========================================
# БЛОК 1: Умовна ймовірність (Запити до БД)
# ==========================================
def run_block_1():
    print("=== БЛОК 1: Умовна ймовірність (Запити до БД) ===")
    p_B = 0.30           # Складний JOIN-запит
    p_A_given_B = 0.70    # Затримка при JOIN
    p_A_given_notB = 0.10 # Затримка при простому запиті

    # Теоретичні значення
    p_A_and_B_theory = p_B * p_A_given_B               # 0.21
    p_A_theory = p_A_and_B_theory + (1 - p_B) * p_A_given_notB  # 0.28
    p_B_given_A_theory = p_A_and_B_theory / p_A_theory # 0.75

    sample_sizes = [100, 1000, 10000, 100000, 1000000]
    p_B_given_A_estimates = []

    print(f"{'N':>8} | {'W(A)':>8} | {'W(B)':>8} | {'W(A∩B)':>8} | {'W(A|B)':>8} | {'W(B|A)':>8} | {'Похибка':>8}")
    print("-" * 75)

    for N in sample_sizes:
        count_A = 0
        count_B = 0
        count_A_and_B = 0

        for _ in range(N):
            is_B = (random.random() < p_B)
            prob_delay = p_A_given_B if is_B else p_A_given_notB
            is_A = (random.random() < prob_delay)

            if is_A:
                count_A += 1
            if is_B:
                count_B += 1
            if is_A and is_B:
                count_A_and_B += 1

        w_A = count_A / N
        w_B = count_B / N
        w_A_and_B = count_A_and_B / N
        w_A_given_B = count_A_and_B / count_B if count_B > 0 else 0
        w_B_given_A = count_A_and_B / count_A if count_A > 0 else 0

        p_B_given_A_estimates.append(w_B_given_A)
        error = abs(w_B_given_A - p_B_given_A_theory)

        print(f"{N:>8} | {w_A:>8.4f} | {w_B:>8.4f} | {w_A_and_B:>8.4f} | {w_A_given_B:>8.4f} | {w_B_given_A:>8.4f} | {error:>8.5f}")

    # Побудова графіка збіжності
    plt.figure(figsize=(8, 5))
    plt.axhline(y=p_B_given_A_theory, color="r", linestyle="--", label=f"Теорія P(B|A) = {p_B_given_A_theory:.2f}")
    plt.plot(sample_sizes, p_B_given_A_estimates, "bo-", label="Оцінка W(B|A)", markersize=6)
    plt.xscale("log")
    plt.title("Блок 1: Збіжність умовної ймовірності P(B|A)")
    plt.xlabel("Кількість запитів N (log scale)")
    plt.ylabel("Умовна ймовірність")
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    plt.savefig("graphics/block1_conditional_prob.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("-> Графік збережено в graphics/block1_conditional_prob.png\n")

if __name__ == "__main__":
    random.seed(12)
    run_block_1()