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
    print("-" * 74)

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

# ==========================================
# БЛОК 2: Варіант 2 (Двофакторна автентифікація 2FA)
# ==========================================
def run_block_2():
    print("=== БЛОК 2: Варіант 2 (Двофакторна автентифікація 2FA) ===")
    N = 100000
    p_S1 = 0.85          # Пароль введено вірно (подія A)
    p_S2_given_S1 = 0.90 # Push підтверджено (подія B|A)

    count_A = 0
    count_B = 0
    count_A_and_B = 0
    count_A_or_B = 0
    count_notA_or_notB = 0

    for _ in range(N):
        event_A = (random.random() < p_S1)
        event_B = False
        if event_A:
            event_B = (random.random() < p_S2_given_S1)

        if event_A:
            count_A += 1
        if event_B:
            count_B += 1
        if event_A and event_B:
            count_A_and_B += 1
        if event_A or event_B:
            count_A_or_B += 1
        if (not event_A) or (not event_B):
            count_notA_or_notB += 1

    w_A_and_B = count_A_and_B / N
    w_B = count_B / N
    w_A_or_B = count_A_or_B / N
    w_A_given_B = count_A_and_B / count_B if count_B > 0 else 0
    w_notA_or_notB = count_notA_or_notB / N

    print(f"P(A ∩ B)                     = {w_A_and_B:.4f} (Теорія = 0.7650)")
    print(f"P(B)                         = {w_B:.4f} (Теорія = 0.7650)")
    print(f"P(A ∪ B)                     = {w_A_or_B:.4f} (Теорія = 0.8500)")
    print(f"P(A|B)                       = {w_A_given_B:.4f} (Теорія = 1.0000)")
    print(f"P(~A ∪ ~B) [Відмова]         = {w_notA_or_notB:.4f} (Теорія = 0.2350)\n")

# ==========================================
# БЛОК 3: Надійність серійно-паралельної системи
# ==========================================
def run_block_3():
    print("=== БЛОК 3: Надійність серійно-паралельної системи ===")
    p1 = 0.98 # LB
    p2 = 0.90 # Web1
    p3 = 0.90 # Web2
    p4 = 0.95 # DB1
    p5 = 0.95 # DB2

    p_sys_theory = p1 * (1 - (1 - p2) * (1 - p3)) * (1 - (1 - p4) * (1 - p5))
    sample_sizes = [100, 1000, 10000, 100000, 1000000]
    w_sys_estimates = []

    print(f"{'N':>8} | {'Успішних':>10} | {'Оцінка W_sys':>12} | {'Теорія P_sys':>12} | {'Похибка':>10}")
    print("-" * 64)

    for N in sample_sizes:
        successes = 0
        for _ in range(N):
            lb_ok = (random.random() < p1)
            web_ok = (random.random() < p2) or (random.random() < p3)
            db_ok = (random.random() < p4) or (random.random() < p5)

            if lb_ok and web_ok and db_ok:
                successes += 1

        w_sys = successes / N
        w_sys_estimates.append(w_sys)
        error = abs(w_sys - p_sys_theory)
        print(f"{N:>8} | {successes:>10} | {w_sys:>12.6f} | {p_sys_theory:>12.6f} | {error:>10.6f}")

    plt.figure(figsize=(8, 5))
    plt.axhline(y=p_sys_theory, color="r", linestyle="--", label=f"Теорія P_sys = {p_sys_theory:.6f}")
    plt.plot(sample_sizes, w_sys_estimates, "go-", label="Оцінка надійності W_sys", markersize=6)
    plt.xscale("log")
    plt.title("Блок 3: Збіжність оцінки надійності системи")
    plt.xlabel("Кількість випробувань N (log scale)")
    plt.ylabel("Надійність системи")
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    plt.savefig("graphics/block3_system_reliability.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("-> Графік збережено в graphics/block3_system_reliability.png\n")

# ==========================================
# БЛОК 4: Варіант 8 (API Rate Limiter)
# ==========================================
def run_block_4():
    print("=== БЛОК 4: Професійна задача (Варіант 8 - API Rate Limiter) ===")
    N = 100000
    p_L1 = 0.20 # Перший запит перевищує ліміт
    p_L2 = 0.30 # Другий запит перевищує ліміт

    p_theory = p_L1 + p_L2 - (p_L1 * p_L2) # 0.44

    rejected_count = 0
    for _ in range(N):
        l1_exceeded = (random.random() < p_L1)
        l2_exceeded = (random.random() < p_L2)

        if l1_exceeded or l2_exceeded:
            rejected_count += 1

    w_stat = rejected_count / N
    error = abs(w_stat - p_theory)

    print(f"Кількість пар запитів (N): {N}")
    print(f"Кількість відхилених пар:  {rejected_count}")
    print(f"Статистична частота W:     {w_stat:.5f}")
    print(f"Теоретична ймовірність P:  {p_theory:.5f}")
    print(f"Абсолютна похибка:         {error:.5f}\n")

if __name__ == "__main__":
    random.seed(12)
    run_block_1()
    run_block_2()
    run_block_3()
    run_block_4()