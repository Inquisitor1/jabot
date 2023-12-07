import json
import random
from datetime import datetime


class Jaba:
    jabas = {}
    maxstat = 100

    def __init__(self, name, bellyful=50, happiness=50, sleep=50, hygiene=50,
                 is_sleeping=False, went_to_sleep=0, last_slept=int(datetime.now().timestamp()),
                 last_ate=int(datetime.now().timestamp()),
                 last_played=int(datetime.now().timestamp()),
                 last_washed=int(datetime.now().timestamp()), overeat=1.5):
        self.name = name
        self.bellyful = bellyful
        self.happiness = happiness
        self.sleep = sleep
        self.hygiene = hygiene
        self.is_sleeping = is_sleeping
        self.went_to_sleep = went_to_sleep
        self.last_slept = last_slept
        self.last_ate = last_ate
        self.last_played = last_played
        self.last_washed = last_washed
        self.overeat = overeat

    def __del__(self):
        self.name = "NN"

    @classmethod
    def save_jaba(cls, jaba):
        cls.jabas.update({jaba.name: {"Bellyful": jaba.bellyful,
                                      "Happiness": jaba.happiness,
                                      "Sleep": jaba.sleep,
                                      "Hygiene": jaba.hygiene,
                                      "Is_sleeping": jaba.is_sleeping,
                                      "When_went_to_sleep": jaba.went_to_sleep,
                                      "Last_slept": jaba.last_slept,
                                      "Last_ate": jaba.last_ate,
                                      "Last_played": jaba.last_played,
                                      "Last_washed": jaba.last_washed,
                                      "Overeat_index": jaba.overeat}})

    def random_runaway(self):
        av = self.ret_average()
        chance = 0
        if av <= 30:
            if 30 >= av > 25:
                chance = 10
            elif 25 >= av > 20:
                chance = 20
            elif 20 >= av > 15:
                chance = 50
            elif 15 >= av > 10:
                chance = 100
            r = random.randint(1, 1001)
            if r <= chance:
                return True  # сбежала
            else:
                return False
        return False

    @staticmethod
    def look_for():
        chance = 333
        r = random.randint(1, 1001)
        if r <= chance:
            return True  # нашлась
        else:
            return False

    def ranaway(self):  # для случая, если после 3-х попыток не нашлась жабка, вызываешь этот метод
        Jaba.jabas.pop(self.name)
        self.__del__()

    def ret_average(self):
        return (self.bellyful + self.happiness + self.sleep + self.hygiene) / 4

    def get_name(self):
        return self.name
    def double_overeat(self):
        if self.overeat <= 45:
            self.overeat *= 2

    def clear_overeat(self):
        self.overeat = 1.5

    def set_played(self):
        self.last_played = int(datetime.now().timestamp())

    def set_ate(self):
        self.last_ate = int(datetime.now().timestamp())

    def set_washed(self):
        self.last_washed = int(datetime.now().timestamp())

    def set_slept(self):
        self.last_slept = int(datetime.now().timestamp())

    def update_stats(self):
        s = int(datetime.now().timestamp()) - self.last_slept
        print(s)
        if s > 300:
            self.sleep -= int(s / 300)
            if self.sleep < 0:
                self.sleep = 0
            self.set_slept()
        e = int(datetime.now().timestamp()) - self.last_ate
        if e > 300:
            self.bellyful -= int(e / 300)
            if self.bellyful < 100:
                self.clear_overeat()
            if self.bellyful < 0:
                self.bellyful = 0
            self.set_ate()
        p = int(datetime.now().timestamp()) - self.last_played
        if p > 300:
            self.happiness -= int(p / 300)
            if self.happiness < 0:
                self.happiness = 0
            self.set_played()
        h = int(datetime.now().timestamp()) - self.last_washed
        if h > 300:
            self.hygiene -= int(h / 300)
            if self.hygiene < 0:
                self.hygiene = 0
            self.set_washed()
        if self.ret_average() < 10:
            self.__del__()
            return False  # если умерла
        else:
            return True  # если просто сократились статы

    def to_feed(self):
        if self.bellyful >= Jaba.maxstat:
            r = random.randint(1, 1001)
            if r <= self.overeat * 10:
                #self.__del__()
                #Jaba.jabas.pop(self.name)
                return False  # Померла от переедания
            self.double_overeat()
        self.bellyful += 10
        return True  # все ок, похавала и не сдохла

    def to_play(self):
        if self.happiness < Jaba.maxstat:
            self.happiness += 25
            return True  # если получилось поиграть (статы меньше максимума)
        else:
            return False  # Наигралась

    def to_wash(self):
        self.hygiene = Jaba.maxstat
        return True  # мыть можно всегда

    def go_sleep(self):
        self.is_sleeping = True
        self.went_to_sleep = int(datetime.now().timestamp())

    def wake_up(self):
        self.is_sleeping = False
        self.set_slept()
        slept = int(datetime.now().timestamp()) - self.went_to_sleep
        self.went_to_sleep = 0
        if slept > 300:
            self.sleep += int(slept / 300)
            if self.sleep > 100:
                self.sleep = Jaba.maxstat

    def ret_stats(self):
        return self.sleep, self.hygiene, self.bellyful, self.happiness, self.ret_average()
    def get_happiness(self):
        return self.happiness
    def get_hygiene(self):
        return self.hygiene
    def get_bellyful(self):
        return self.bellyful
    def get_sleep(self):
        return self.sleep
    def set_name(self, name):
        self.name = name

    @classmethod
    def to_file(cls):
        with open("jabas.json", "w", encoding="utf-8") as f:
            json.dump(cls.jabas, f, indent=4)

    @classmethod
    def from_file(cls):
        with open("jabas.json", "r", encoding="utf-8") as f:
            cls.jabas = json.load(f)

def create_frog(name):
    jaba = Jaba(name)
    return jaba

jab = Jaba("ыыыыыыыы")
jab.save_jaba(jab)
jab.to_file()
print(jab.ret_average())
#сасите
jab.update_stats()
print(jab.ret_average())

