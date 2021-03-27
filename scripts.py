import random

from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid


def fix_marks(schoolkid):
    fixed_marks_number = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=4)
    if fixed_marks_number > 0:
        print(f'Исправлено {fixed_marks_number} оценок')
    else:
        print('Плохих оценок нет!')


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    deleted_chastisements_number = chastisements.delete()[0]
    if deleted_chastisements_number > 0:
        print(f'Удалено {deleted_chastisements_number} замечаний')
    else:
        print('Замечания отсутствуют')


def create_commendation(schoolkid, subject):
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!', 'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!'
    ]
    commendation_text = random.choice(commendations)

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by('-date').first()

    if not lesson:
        print(f'Предмет {subject} не найден!')
        return

    Commendation.objects.create(
        text=commendation_text,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )

    print(f'Добавлена похвала: {commendation_text}')


def fix(full_name, subject):
    if not full_name:
        print('Не введено имя')
        return
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject)
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено несколько учеников с именем {full_name}. Скрипт завершает работу.')
    except Schoolkid.DoesNotExist:
        print(f'Ученик с именем {full_name} не найден. Скрипт завершает работу.')
