from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        """Получить строку сообщения."""
        return self.message.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    M_IN_HOUR = 60
    LEN_STEP = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    MEAN_SPEED_MULTIPLIER = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return (self.SPEED_MULTIPLIER * self.get_mean_speed()
                - self.MEAN_SPEED_MULTIPLIER
                ) * self.weight / self.M_IN_KM * self.duration * self.M_IN_HOUR


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MILTIPLIER = 0.035
    CALORIES_MULTIPLIER = 0.029
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        return (self.WEIGHT_MILTIPLIER
                * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIES_MULTIPLIER * self.weight
                ) * self.duration * self.M_IN_HOUR


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
                )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        COEFF_1 = 1.1
        COEFF_2 = 2
        return (self.get_mean_speed() + COEFF_1) * COEFF_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type not in workouts:
        raise ValueError('No such type of training!')
    if len(data) not in (3, 4, 5):
        raise ValueError('Incorrect data param format')
    return workouts[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:

        main(read_package(workout_type, data))
