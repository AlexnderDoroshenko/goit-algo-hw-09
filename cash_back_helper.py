from typing import Dict, Tuple, List
import timeit

COINS_NOMINAL = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int, coins: List[int] = COINS_NOMINAL) -> Dict[int, int]:
    """
    Використовує жадібний алгоритм для визначення кількості монет, 
    необхідних для видачі решти покупцеві.

    :param amount: Сума, яку потрібно видати.
    :param coins: Доступний номінал монет.
    :return: Словник з номіналами монет і їх кількістю.
    """
    result = {}

    for coin in coins:
        # Перевірка, чи залишилася сума для видачі
        if amount == 0:
            break
        # Визначаємо, скільки монет даного номіналу можна використати
        count = amount // coin
        if count > 0:
            result[coin] = count  # Додаємо монети до результату
            amount -= coin * count  # Зменшуємо суму, що залишилася

    return result


def find_min_coins(amount: int, coins: List[int] = COINS_NOMINAL) -> Dict[int, int]:
    """
    Використовує динамічне програмування для визначення мінімальної кількості монет,
    необхідних для видачі решти покупцеві.

    :param amount: Сума, яку потрібно видати.
    :param coins: Доступний номінал монет.
    :return: Словник з номіналами монет і їх кількістю для досягнення заданої суми.
    """
    # Ініціалізуємо масив для зберігання мінімальної кількості монет
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Для суми 0 потрібно 0 монет
    used_coins = [0] * (amount + 1)  # Масив для відстеження використаних монет

    for coin in coins:
        for x in range(coin, amount + 1):
            # Перевіряємо, чи можемо зменшити кількість монет для даної суми
            if dp[x - coin] + 1 < dp[x]:
                # Оновлюємо мінімальну кількість монет
                dp[x] = dp[x - coin] + 1
                # Запам'ятовуємо, яка монета вже була використана
                used_coins[x] = coin

    result = {}
    while amount > 0:
        # Визначаємо, яка монета була використана для поточної суми
        coin = used_coins[amount]
        if coin in result:
            result[coin] += 1  # Збільшуємо лічильник для монет цього номіналу
        else:
            result[coin] = 1  # Додаємо новий номінал до поточного результату
        amount -= coin  # Зменшуємо залишкову суму

    return result


# Тестування

GREEDY_FAILS_COINS = [25, 10, 6, 1]


def run_tests():
    test_cases: Tuple[Tuple[int, str, Dict[int, int], Dict[int, int]]] = [
        (113, "Тест: Сума 113", {50: 2, 10: 1,
         2: 1, 1: 1}, {1: 1, 2: 1, 10: 1, 50: 2}),
        (75, "Тест: Сума 75 (можна зібрати найбільшими номіналами)",
         {50: 1, 25: 1}, {25: 1, 50: 1}),
        (8, "Тест: Сума 8 (складний випадок)", {
         5: 1, 2: 1, 1: 1}, {5: 1, 2: 1, 1: 1}),
        (1000, "Тест: Сума 1000", {50: 20}, {50: 20}),  # Сума з 50 копійок
        (234, "Тест: Сума 234", {50: 4, 25: 1, 5: 1, 2: 2}, {
            2: 2, 5: 1, 25: 1, 50: 4}),
        (99, "Тест: Сума 99 (складний випадок)", {
         50: 1, 25: 1, 10: 2, 2: 2},
         {2: 2, 10: 2, 25: 1, 50: 1}),
        (33, "Тест: Сума 33 (складний випадок)", {
         25: 1, 5: 1, 2: 1, 1: 1}, {1: 1, 2: 1, 5: 1, 25: 1}),
        (0, "Тест: Сума 0 (0 копійок)", {}, {}),
    ]

    for amount, description, expected_greedy, expected_min_coins in test_cases:
        print(f"\n{description}:")

        # Жадібний алгоритм
        greedy_time = timeit.timeit(
            lambda: find_coins_greedy(amount), number=1000)
        greedy_result = find_coins_greedy(amount)
        print(f"  Жадібний алгоритм: {
              greedy_result} (Час: {greedy_time:.6f} секунд)")
        assert greedy_result == expected_greedy, f"Помилка: очікував {
            expected_greedy}, отримав {greedy_result}"

        # Динамічне програмування
        min_coins_time = timeit.timeit(
            lambda: find_min_coins(amount), number=1000)
        min_coins_result = find_min_coins(amount)
        print(f"  Динамічне програмування: {
              min_coins_result} (Час: {min_coins_time:.6f} секунд)")
        assert min_coins_result == expected_min_coins, f"Помилка: очікував {
            expected_min_coins}, отримав {min_coins_result}"


def test_greedy_failure():
    amount = 30

    # Жадібний алгоритм
    greedy_result = find_coins_greedy(
        amount, GREEDY_FAILS_COINS)  # Викликаємо жадібний алгоритм

    # Динамічне програмування
    # Викликаємо динамічний алгоритм
    min_coins_result = find_min_coins(amount, GREEDY_FAILS_COINS)

    # Очікуваний результат (правильний)
    expected_min_coins = {10: 3}

    print(f"Жадібний алгоритм повернув: {greedy_result}")
    assert greedy_result == expected_min_coins, \
        f"Жадібний алгоритм надав не оптимальне рішення! очикується {
            expected_min_coins}, фактичний результат {greedy_result}"

    print(f"Динамічний алгоритм повернув: {greedy_result}")
    assert min_coins_result == expected_min_coins, \
        "Динамічний алгоритм надав не оптимальне рішення!"


# Запуск тестів
run_tests()

# Запуск складного тесту
test_greedy_failure()
