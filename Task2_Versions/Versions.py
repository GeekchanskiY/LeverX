class Version:

    """

    Сравнение версий ведется чисто для упомянутых примеров

    Добавление .replace() добавляет новый постфикс, приоритеты можно менять


    0-alpha < o-alpha.1
    .1b < 10-alpha.beta ! Сравнивается само число 10
    0-rc.1 < 0

    Приоритеты контроля:
    альфа: 1
    бета: 2
    rc: -1

    Конструкция получилась довольно массивной, но она обрабатывает все возможные случаи

    """

    def __init__(self, version):
        self.version = version

    def get_version(self):
        """
        Метод возвращает список с преобразованием к общему формату
        """
        version = self.version.replace("-", "").replace(" ","").replace(":", "").replace("alpha", ":1").replace("beta", ":2").replace("rc", ":-1")\
            .replace("b", ":2").split('.')
        return version

    def __lt__(self, other):
        """
            Сравнение значений приведенных к общему формату
        """
        my_v = self.get_version()
        other_v = other.get_version()
        if len(my_v) >= len(other_v):
            highest = my_v
            lowest = other_v
            highest_length = True
        else:
            highest = other_v
            lowest = my_v
            highest_length = False
        for i in range(len(highest)):

            try:
                highest_number = int(highest[i].split(':')[0])
            except ValueError:
                """ Нужен если на конце конструкции стоит .beta без цифры, например """
                highest_number = 0


            try:
                lowest_number = int(lowest[i].split(':')[0])
            except ValueError:
                lowest_number = 0
            except IndexError:
                """
                Если все значения до конца одной из версий совпали, то в зависимости от самой длинной версии будет
                делаться вывод какая новее. Это первое что пришло в голову, короче с той же точностью
                вариантов пока что не нашел.
                """
                if highest_length:
                    return False
                else:
                    return True


            if highest_number != lowest_number:
                """
                    Сравнение голых чисел
                """
                if highest_number < lowest_number:
                    if highest_length:
                        return True
                    else:
                        return False
            else:
                """
                    Сравнение приоритетов
                """
                try:
                    highest_priority = int(highest[i].split(':')[1])
                except IndexError:
                    """
                        Отсутствие приоритета делает его ранвым 0
                    """
                    highest_priority = 0
                try:
                    lowest_priority = int(lowest[i].split(':')[1])
                except IndexError:
                    lowest_priority = 0

                if highest_priority != lowest_priority:
                    if highest_priority > lowest_priority:
                        if highest_length:
                            return False
                        else:
                            return True
                    else:
                        if highest_length:
                            return True
                        else:
                            return False
        return False

    def __gt__(self, other):
        """
            метод использует для сравнения существующие методы lt и ne
        """
        if self != other and not self < other:
            return True
        else:
            return False

    def __ne__(self, other):
        """
            сравнивает приведенные к стандартной форме значения
        """
        my_v = self.get_version()
        other_v = other.get_version()
        if len(my_v) == len(other_v):
            for i in range(len(my_v)):
                if my_v[i] != other_v[i]:
                    return True
        else:
            return True

        return False



def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1.0.0.1", "1.0.0.1.1")
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()