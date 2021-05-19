import json
import argparse

import xml.etree.ElementTree as ET


class MyMeta(type):
    """ Метакласс использован для возвращения всех экземпляров класса Room """
    instances = []

    def __call__(cls, *args, **kwargs):
        instance = super(MyMeta, cls).__call__(*args, **kwargs)
        cls.instances.append(instance)
        return instance


class Room(object, metaclass=MyMeta):
    """

    Класс содержит свой номер и экземпляры учеников
    Методы для добавления учеников и вывода номера комнаты со списком имен учеников

     """
    def __init__(self, room_id):
        self.room_id = room_id
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def get_data(self):
        return self.room_id, [student.get_name() for student in self.students]


class Student:
    """

    Студент содержит в себе метод для вывода своего имени

    """
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


def read_json(path):
    """ Чтение json """
    with open(path, 'r', encoding="cp1251") as json_file:
        json_data = json.load(json_file)
        json_file.close()
    return json_data


def write_json(final_json_data):
    """ Запись json """
    with open("output.json", "w", encoding="cp1251") as f:
        json.dump(final_json_data, f)
        f.close()


def write_xml(data):
    """ Запись xml """
    root = ET.Element('root')
    for i, item in enumerate(data, 1):
        person = ET.SubElement(root, "Room #{}".format(item["room"]))
        students = ET.SubElement(person, 'students')
        for student in item['students']:
            ET.SubElement(students, "student").text = student
    tree = ET.ElementTree(root)
    tree.write('output.xml')


def main():
    """ Чтение данных из файлов """
    parser = argparse.ArgumentParser(description="Path to data")
    parser.add_argument("path_to_rooms", type=str, help="Input absolute path for rooms.json", default=None,
                        required=True)
    parser.add_argument("path_to_students", type=str, help="Input absolute path for students.json", default=None,
                        required=True)
    parser.add_argument("output_format", type=int, help="Choose output format. 1 - Json, 2 - XML, 3 - both",
                        default=None, required=True)
    args = parser.parse_args()
    print(args.output_format)
    rooms_json = read_json(args.path_to_rooms)
    students_json = read_json(args.path_to_students)

    """ Создание комнат и распределение учеников по комнатам """

    [Room(i["id"]) for i in rooms_json]
    for i in students_json:
        student = Student(i["name"])
        Room.instances[int(i["room"])].students.append(student)

    """ Получение данных из всех комнат с последующей записью в json и xml """

    writing_data = []
    for room in Room.instances:
        writing_data.append({"room": room.get_data()[0], "students": room.get_data()[1]})

    if args.output_format == 1:
        write_json(writing_data)
    elif args.output_format == 2:
        write_xml(writing_data)
    else:
        write_json(writing_data)
        write_xml(writing_data)


if __name__ == '__main__':
    main()
