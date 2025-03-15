import time
import random
from typing import Dict


class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        """Ініціалізація Rate Limiter з мінімальним інтервалом між повідомленнями."""
        self.min_interval = min_interval
        self.user_last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        """Перевіряє, чи може користувач надіслати повідомлення на основі часу останнього повідомлення."""
        current_time = time.time()
        if user_id not in self.user_last_message_time:
            return True
        last_time = self.user_last_message_time[user_id]
        return (current_time - last_time) >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        """Реєструє нове повідомлення користувача, якщо дозволено."""
        if self.can_send_message(user_id):
            self.user_last_message_time[user_id] = time.time()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """Обчислює час до можливості надсилання наступного повідомлення."""
        if user_id not in self.user_last_message_time:
            return 0.0
        last_time = self.user_last_message_time[user_id]
        time_left = self.min_interval - (time.time() - last_time)
        return max(0.0, time_left)


# ✅ **Тестова функція для перевірки роботи Rate Limiter**
def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Симуляція потоку повідомлень (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Випадкова затримка між повідомленнями
        time.sleep(random.uniform(0.1, 1.0))

    print("\nОчікуємо 10 секунд...")
    time.sleep(10)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_throttling_limiter()