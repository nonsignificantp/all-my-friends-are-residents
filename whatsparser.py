import re
import pandas as pd
from dateutil.parser import parse

class WhatsParser:
    def __init__(self, file_path):
        self.messages = self._get_messages_from_file(file_path)
        self.count = 0

    def _get_messages_from_file(self, file_path):
        messages = []
        with open(file_path) as file:
            for line in file:

                if self._is_start_of_new_message(line):
                    message = self._construct_message(line)
                    messages.append(message)
                else:
                    messages[-1]._add_content(line)

        return messages

    def _construct_message(self, line):
        datetime = self._get_datetime_from_line(line)
        author = self._get_author_from_line(line)
        content = self._get_content_from_line(line, author)
        return Message(datetime, author, content)

    def to_dataframe(self):
        messages = [item.__dict__() for item in self.messages]
        return pd.DataFrame(messages)

    @staticmethod
    def _is_start_of_new_message(line):
        if re.match(r'^\d+/\d+/\d+\s\d+:\d+:\d+\s(AM|PM)', line):
            return True
        return False

    @staticmethod
    def _get_datetime_from_line(line):
        datetime = re.search(r'^.+(AM|PM)(?=:)', line).group()
        return datetime

    @staticmethod
    def _get_author_from_line(line):
        author = re.search(r'(?<=:\s)(.*?)(?=:)', line).group()
        return author

    @staticmethod
    def _get_content_from_line(line, author):
        start = re.search(author, line).span()[1]
        content = re.search(r'(?<=:\s).*$', line[start:]).group().strip()
        return content

    @property
    def authors(self):
        return list(set([msg.author for msg in self.messages]))

    def __getitem__(self, position):
        return self.messages[position]

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if len(self.messages) < self.count:
            self.count = 0
            raise StopIteration
        return self.messages[self.count-1]

    def __len__(self):
        return len(self.messages)

class Message:
    def __init__(self, datetime, author, content):
        self._datetime = self._parse_datetime(datetime)
        self._author = author
        self._content = content

    def _add_content(self, line):
        self._content += f' {line.strip()}'

    @staticmethod
    def _parse_datetime(datetime):
        return parse(datetime)

    @property
    def datetime(self):
        return self._datetime

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content

    @property
    def size(self):
        return len(self._content)

    def __str__(self):
        return f"{self._datetime} - {self._author}: {self._content}"

    def __repr__(self):
        return f"{self._datetime} - {self._author}: {self._content}"

    def __dict__(self):
        return {'datetime':self._datetime, 'author':self._author, 'content':self._content}
