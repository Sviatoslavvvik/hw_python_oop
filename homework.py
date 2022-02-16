from typing import Dict, List, ClassVar, Optional
from dataclasses import dataclass


@dataclass(init=True,
           repr=False,
           eq=False
            )
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вернуть строку сообщения"""
        info_message: str = (f'Тип тренировки: {self.training_type};'
                             f' Длительность: {self.duration:.3f} ч.;'
                             f' Дистанция: {round(self.distance,3):.3f} км;'
                             f' Ср. скорость: {round (self.speed,3):.3f} км/ч;'
                             f' Потрачено ккал: {round(self.calories,3):.3f}.'
                             )
        return info_message


@dataclass(init=True,
           repr=False,
           eq=False
           )
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65  # length of one step
    M_IN_KM: ClassVar[int] = 1000  # m in km
    MINUTES_IN_HOUR: ClassVar[float] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_pass: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определите run '
                                  f'в {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories()
                           )


@dataclass(init=False,
           repr=False,
           eq=False
           )
class Running(Training):
    """Тренировка: бег."""
    CALORIES_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_SPEED_DEDUCT: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_SPEED_MULTIPLIER
                                 * self.get_mean_speed()
                                 - self.CALORIES_SPEED_DEDUCT) * self.weight
                                 / self.M_IN_KM * self.duration
                                 * self.MINUTES_IN_HOUR)
        return spent_calories


@dataclass(init=True,
           repr=False,
           eq=False
           )
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WHEIGHT_MULTIPLYER: ClassVar[float] = 0.035
    MEAN_SPEED_POWER: ClassVar[int] = 2
    SECOND_WHEIGHT_MULTIPLYER: ClassVar[float] = 0.029

    height: float  # user's height in m

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_WHEIGHT_MULTIPLYER
                                 * self.weight
                                 + ((self.get_mean_speed()
                                     ** self.MEAN_SPEED_POWER)
                                     // self.height)
                                 * self.SECOND_WHEIGHT_MULTIPLYER
                                 * self.weight)
                                 * self.duration * self.MINUTES_IN_HOUR)
        return spent_calories


@dataclass(init=True,
           repr=False,
           eq=False
           )
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    CALORIE_SPEED_SUMMAND: ClassVar[float] = 1.1
    CALORIES_SPEED_MULTIPL: ClassVar[float] = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.get_mean_speed()
                                  + self.CALORIE_SPEED_SUMMAND)
                                 * self.CALORIES_SPEED_MULTIPL * self.weight)
        return spent_calories


def read_package(workout_type: str, data: List[float]) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str: Training] = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking
                                          }

    return (workout_types.get(workout_type)(*data))


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180])]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training:
            main(training)
        else:
            raise Exception('Такого типа тренировки несуществует')
