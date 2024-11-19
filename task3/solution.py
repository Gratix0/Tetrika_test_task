def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Вычисляет общее время присутствия ученика и учителя на уроке.
    """

    def merge_intervals(intervals):
        """Объединяет пересекающиеся интервалы."""
        merged = []
        for start, end in sorted(intervals):
            if merged and merged[-1][1] >= start:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged

    def intersect_intervals(intervals1, intervals2):
        """Возвращает пересечение двух списков интервалов."""
        i, j = 0, 0
        result = []
        while i < len(intervals1) and j < len(intervals2):
            start = max(intervals1[i][0], intervals2[j][0])
            end = min(intervals1[i][1], intervals2[j][1])
            if start < end:
                result.append([start, end])
            if intervals1[i][1] < intervals2[j][1]:
                i += 1
            else:
                j += 1
        return result

    # Преобразуем интервалы в пары [start, end]
    lesson = [[intervals['lesson'][0], intervals['lesson'][1]]]
    pupil_intervals = [[intervals['pupil'][i], intervals['pupil'][i + 1]] for i in range(0, len(intervals['pupil']), 2)]
    tutor_intervals = [[intervals['tutor'][i], intervals['tutor'][i + 1]] for i in range(0, len(intervals['tutor']), 2)]

    # Ограничиваем интервалы временем урока
    pupil_intervals = merge_intervals(intersect_intervals(lesson, pupil_intervals))
    tutor_intervals = merge_intervals(intersect_intervals(lesson, tutor_intervals))

    # Находим пересечения ученика и учителя
    common_intervals = intersect_intervals(pupil_intervals, tutor_intervals)

    # Суммируем длительности общих интервалов
    return sum(end - start for start, end in common_intervals)
