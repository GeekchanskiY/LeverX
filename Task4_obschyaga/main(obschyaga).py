import json
import argparse
import pymysql

import xml.etree.ElementTree as ET

from queries import *

from decimal import Decimal

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
    def __init__(self, data, filename):
        super().__init__(data)
        self.filename = filename

    def write(self):
        with open("{}.json".format(self.filename), "w", encoding="cp1251") as f:
            json.dump(self.data, f, ensure_ascii=False, default=str)
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
    def __init__(self, room_id):
        self.room_id = room_id
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def get_data(self):
        return self.room_id, [student.get_name() for student in self.students]


class Student:
    def __init__(self, name, id, sex, birthday, room):
        self.name = name
        self.id = id
        self.birthday = birthday
        self.room = room
        self.sex = sex

    def get_name(self):
        return self.name


def main():
    # Чтение данных из файлов
    parser = argparse.ArgumentParser(description="Path to data")
    parser.add_argument("path_to_rooms", type=str, help="Input absolute path for rooms.json", default=None)
    parser.add_argument("path_to_students", type=str, help="Input absolute path for students.json", default=None)
    parser.add_argument("output_format", type=int, help="Choose output format. 1 - Json, 2 - XML, 3 - both",
                        default=None)
    parser.add_argument("db_host", type=str, help="Database host")
    parser.add_argument("db_user", type=str, help="Database user")
    parser.add_argument("db_password", type=str, help="Database password")
    args = parser.parse_args()

    # Создание (в случае отсутствия) таблиц студентов и комнат
    init(args)

    rooms_json = JsonReader(args.path_to_rooms).read()
    students_json = JsonReader(args.path_to_students).read()

    # Запись комнат и студентов в базу
    data = []
    for i in rooms_json:
        data.append(i["id"])

    add_rooms(args, data)
    add_students(args, students_json)

    # Вывод обработанных данных
    JsonWriter(min_avg_age(args), "min_avg_age").write()
    JsonWriter(diff_sex(args), "different_sex").write()
    JsonWriter(max_diff_age(args), "max_diff_age").write()


    rooms = [Room(i["id"]) for i in rooms_json]
    for i in students_json:
        student = Student(id=i["id"], sex=i["sex"], name=i["name"], birthday=i["birthday"], room=i["room"])
        rooms[int(i["room"])].students.append(student)

    # Получение данных из всех комнат с последующей записью в json и xml

    writing_data = []
    for room in rooms:
        writing_data.append({"room": room.get_data()[0], "students": room.get_data()[1]})

    if args.output_format == 1:
        JsonWriter(writing_data, "output").write()
    elif args.output_format == 2:
        XmlWriter(writing_data).write()
    else:
        JsonWriter(writing_data, "output").write()
        XmlWriter(writing_data).write()


if __name__ == '__main__':
    main()
