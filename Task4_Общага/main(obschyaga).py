import json
import argparse
import pymysql

import xml.etree.ElementTree as ET

from queries import *

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
    print(min_avg_age(args))
    print(diff_sex(args))
    print(max_diff_age(args))
    #init(args)


    rooms_json = JsonReader(args.path_to_rooms).read()
    students_json = JsonReader(args.path_to_students).read()
    rooms = [Room(i["id"]) for i in rooms_json]
    data = []
    for i in rooms_json:
        data.append(i["id"])
    #add_rooms(args, data)
    #add_students(args, students_json)
    students = [Student(name=i["name"], birthday=i["birthday"], sex=i["sex"], room=i["room"], id=i["id"]) for i in students_json]


    # Создание комнат и распределение учеников по комнатам


if __name__ == '__main__':
    main()
