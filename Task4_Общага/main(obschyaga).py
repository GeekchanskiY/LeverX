import json
import argparse

import xml.etree.ElementTree as ET

class Writer:
    def __init__(self, data):
        self.data = data
        pass

    def write(self):
        raise NotImplementedError


class Serializer:
    def __init__(self, data):
        self.data = data
        self.serialized_data = None

    def serialize(self):
        raise NotImplementedError


class XmlSerializer(Serializer):
    def __init__(self, data, root):
        super().__init__(data)
        self.root = root

    def serialize(self):
        for i, item in enumerate(self.data, 1):
            person = ET.SubElement(self.root, "Room #{}".format(item["room"]))
            students = ET.SubElement(person, 'students')
            for student in item['students']:
                ET.SubElement(students, "student").text = student
        return self.root


class JsonWriter(Writer):
    def __init__(self, data):
        super().__init__(data)

    def write(self):
        with open("output.json", "w", encoding="cp1251") as f:
            json.dump(self.data, f)
            f.close()


class XmlWriter(Writer):
    def __init__(self, data):
        super().__init__(data)

    def write(self):
        root = XmlSerializer(self.data, ET.Element('root')).serialize()
        tree = ET.ElementTree(root)
        tree.write('output.xml')


class JsonReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, "r") as read_file:
            return json.load(read_file)




class Room(object):
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
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


def main():
    # Чтение данных из файлов
    parser = argparse.ArgumentParser(description="Path to data")
    parser.add_argument("path_to_rooms", type=str, help="Input absolute path for rooms.json", default=None)
    parser.add_argument("path_to_students", type=str, help="Input absolute path for students.json", default=None)
    parser.add_argument("output_format", type=int, help="Choose output format. 1 - Json, 2 - XML, 3 - both",
                        default=None)
    args = parser.parse_args()

    rooms_json = JsonReader(args.path_to_rooms).read()
    students_json = JsonReader(args.path_to_students).read()

    # Создание комнат и распределение учеников по комнатам

    rooms = [Room(i["id"]) for i in rooms_json]
    for i in students_json:
        student = Student(i["name"])
        rooms[int(i["room"])].students.append(student)

    # Получение данных из всех комнат с последующей записью в json и xml

    writing_data = []
    for room in rooms:
        writing_data.append({"room": room.get_data()[0], "students": room.get_data()[1]})

    if args.output_format == 1:
        JsonWriter(writing_data).write()
    elif args.output_format == 2:
        XmlWriter(writing_data).write()
    else:
        JsonWriter(writing_data).write()
        XmlWriter(writing_data).write()


if __name__ == '__main__':
    main()
