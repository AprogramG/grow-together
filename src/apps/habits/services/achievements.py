from apps.habits.models import Achievement, CompletedAchievement


def user_achievement_progress(request):
    """Получает прогресс достижений пользователя"""

    achievements = Achievement.objects.all()
    achievements_data = []
    for achievement in achievements:
        # Не добавляем достижение, если оно уже выполнено
        if not CompletedAchievement.objects.filter(
            user=request.user,
            achievement=achievement,
        ).exists():
            # Получаем прогресс для текущего пользователя из функции в модели Achievement
            progress_data = achievement.calculate_progress(request.user)

            if progress_data["current_value"] == progress_data["target"]:
                CompletedAchievement.objects.get_or_create(
                    user=request.user,
                    achievement=achievement,
                )

            achievement_data = {
                "name": achievement.name,
                "description": achievement.description,
                "img": achievement.img,
                "progress": progress_data["progress"],
                "current_value": progress_data["current_value"],
                "target_value": progress_data["target"],
                "id": achievement.id,
            }

            # Конвертируем строковый процент в число для корректной сортировки
            progress_percent = float(progress_data["progress"].rstrip("%"))
            achievement_data["progress_percent"] = progress_percent

            if progress_percent < 100:
                achievements_data.append(achievement_data)

    # Сортируем достижения по проценту выполнения в порядке убывания
    achievements_data.sort(key=lambda x: x["progress_percent"], reverse=True)

    # Удаляем временное поле progress_percent
    for achievement in achievements_data:
        del achievement["progress_percent"]

    return achievements_data


def update_achievements_status(request):
    """Обновляет статус достижений пользователя"""

    achievements = Achievement.objects.all()
    for achievement in achievements:
        progress_data = achievement.calculate_progress(request.user)

        if progress_data["current_value"] == progress_data["target"]:
            print("True")
            CompletedAchievement.objects.get_or_create(
                user=request.user,
                achievement=achievement,
            )
