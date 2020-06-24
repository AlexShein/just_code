# Alexander Shein 04.06.20
from typing import Dict, List


def t1(data_in: str) -> Dict[int, str]:
    '''
    1) Пронумеруй все элементы строки.
    '''
    return {1: 'a'}


def t2(data_in: List[Dict]) -> List[int]:
    '''
    2) Есть список словарей вида:
    [
        {'id': 161, 'status': 'done',},
        {'id': 162, 'status': 'error',},
        {'id': 163, 'status': 'done',},
        {'id': 164, 'status': 'error',},
        {'id': 165, 'status': 'done',},
    ]
    Как получить id только тех элементов, у которых статус 'error'?
    '''
    return [0]


def t3(data_in: List[Dict]) -> List[Dict]:
    '''
    3) Входные данные как в задачке 2.
    Поменяй статус на 'in_progress', у которых статус 'error'.
    '''
    return [{'a': 'b'}]


def t4_timing():
    '''
    4) Напиши декоратор, считающий время выполнения функции
    и оберни им функцию calculations
    '''
    pass


def calculations(x: int) -> int:
    for i in range(1, 10000):
        x += i * i
    return x


class Task:
    data = [
        {'id': 161, 'res': 200},
        {'id': 162, 'res': 10},
        {'id': 163, 'res': 150},
        {'id': 164, 'res': 300},
        {'id': 165, 'res': 450},
    ]

    def filter_(self, res__gt: int = 0) -> List[Dict]:
        return list(filter(lambda x: x['res'] > res__gt, self.data))


def t5_stats_view(min_res: int) -> Dict:
    '''
    5) Напиши логику, которая валидирует, что min_res больше 0 и возвращает
    для всех элементов с res > min_res словарик вида
    {'max_res': 123, 'ids': [1,2,3]}
    '''
    task_model = Task()
    return {}


if __name__ == '__main__':

    # 1
    t1_data_in = 'abcdef'
    task_1_res = t1(t1_data_in)
    print(f'Task 1: {task_1_res}')

    # 2
    t2_data_in = [
        {'id': 161, 'status': 'done',},
        {'id': 162, 'status': 'error',},
        {'id': 163, 'status': 'done',},
        {'id': 164, 'status': 'error',},
        {'id': 165, 'status': 'done',},
    ]
    task_2_res = t2(t2_data_in)
    print(f'Task 2: {task_2_res}')

    # 3
    t3_data_in = [
        {'id': 161, 'status': 'done',},
        {'id': 162, 'status': 'error',},
        {'id': 163, 'status': 'done',},
        {'id': 164, 'status': 'error',},
        {'id': 165, 'status': 'done',},
    ]
    task_3_res = t3(t3_data_in)
    print(f'Task 3: {t3_data_in}')

    # 4
    calculations(4)

    # 5
    task_5_res = t5_stats_view(160)
    print(f'Task 5: {task_5_res}')

