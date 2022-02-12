from typing import Dict
from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть строку сообщения"""
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {round(self.duration,3):.3f} ч.;'
                f' Дистанция: {round(self.distance,3):.3f} км;'
                f' Ср. скорость: {round (self.speed,3):.3f} км/ч;'
                f' Потрачено ккал: {round(self.calories,3):.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # length of one step
    M_IN_KM: int = 1000     # constant to recalculate of meanf from m to km

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18  # first coeffcicient in spent_calories formula
    COEFF_CALORIE_2: int = 20  # second coefficient in spent_calories formula
    COEFF_CALORIE_3: int = 60  # constant to tecalculate hours in minutes

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.COEFF_CALORIE_1 * 
                                super().get_mean_speed() 
                                - self.COEFF_CALORIE_2) * self.weight 
                                / self.M_IN_KM * self.duration 
                                * self.COEFF_CALORIE_3)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035  # first coeffcicient in spent_calories equat
    COEFF_CALORIE_2: int = 2  # second coefficient in spent_calories equat
    COEFF_CALORIE_3: float = 0.029  # third coefficient in spent_calories equat.
    COEFF_CALORIE_4: int = 60  # constant to tecalculate hours in minutes


    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # user height in m
    
    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.COEFF_CALORIE_1 * self.weight 
                                 + ((super().get_mean_speed() 
                                 ** self.COEFF_CALORIE_2) 
                                 // self.height)
                                 * self.COEFF_CALORIE_3 * self.weight)
                                 * self.duration * self.COEFF_CALORIE_4)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1  # first coeff. in spent_calories equat.
    COEFF_CALORIE_2: float = 2  # second coeff. in spent_calories equat.

    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                length_pool: float,
                count_pool: float
                ) -> None:
        super().__init__(action, 
                        duration, 
                        weight)
        self.length_pool = length_pool  # in metres
        self.count_pool = count_pool  # swiming pools amount by user

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool
                            / (self.M_IN_KM) / (self.duration))
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                                * self.COEFF_CALORIE_2 * self.weight)
        return spent_calories
        
        
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str: Union[Swimming, 
                                  Running,
                                  SportsWalking]
                        ] = {'SWM': Swimming,
                            'RUN': Running,
                            'WLK': SportsWalking
                            }
   
    return (workout_types[workout_type](*data))


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
                ('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180]),
               ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
