import json
import os

from config.constant import cur_path


class FTWCConfig:
    def __init__(self):
        self.id_list = []
        self.channel_list = []
        self.file_path = os.path.join(cur_path, 'config', 'ftwc_config')
        self.load()

    def load(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.channel_list = data.get('channel_list', [])
                self.id_list = data.get('id_list', [])
        except FileNotFoundError:
            print("FTWC load error")

    def save(self):
        data = {
            'channel_list': self.channel_list,
            'id_list': self.id_list
        }
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def add_channel(self, channel):
        if channel not in self.channel_list:
            self.channel_list.append(channel)
            self.save()

    def remove_channel(self, channel):
        if channel in self.channel_list:
            self.channel_list.remove(channel)
            self.save()

    def add_id(self, qq_id):
        if qq_id not in self.id_list:
            self.id_list.append(qq_id)
            self.save()

    def remove_id(self, qq_id):
        if qq_id in self.id_list:
            self.id_list.remove(qq_id)
            self.save()

    def channel_id_in_config(self, channel, qq_id):
        return channel in self.channel_list and qq_id in self.id_list
