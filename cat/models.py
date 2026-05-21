from random import randint

from django.db import models


class Cat(models.Model):
    SAD_AVATAR = 'cat/images/cat_sad.svg'
    CALM_AVATAR = 'cat/images/cat_calm.svg'
    HAPPY_AVATAR = 'cat/images/cat_happy.svg'
    SLEEPING_AVATAR = 'cat/images/cat_sleeping.svg'

    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=1)
    fullness = models.PositiveIntegerField(default=40)
    happiness = models.PositiveIntegerField(default=40)
    is_sleeping = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def avatar(self):
        if self.is_sleeping:
            return self.SLEEPING_AVATAR
        if self.happiness <= 30:
            return self.SAD_AVATAR
        if self.happiness <= 70:
            return self.CALM_AVATAR
        return self.HAPPY_AVATAR

    @property
    def mood(self):
        if self.is_sleeping:
            return 'спит'
        if self.happiness <= 30:
            return 'грустит'
        if self.happiness <= 70:
            return 'спокоен'
        return 'счастлив'

    def feed(self):
        if self.is_sleeping:
            return

        self.fullness += 15
        self.happiness += 5

        if self.fullness > 100:
            self.happiness -= 30

        self.normalize_stats()

    def play(self):
        if self.is_sleeping:
            self.is_sleeping = False
            self.happiness -= 5
            self.normalize_stats()
            return

        self.happiness += 15
        self.fullness -= 10

        if randint(1, 3) == 1:
            self.happiness = 0

        self.normalize_stats()

    def sleep(self):
        self.is_sleeping = True
        self.normalize_stats()

    def do_action(self, action):
        if action == 'feed':
            self.feed()
        elif action == 'play':
            self.play()
        elif action == 'sleep':
            self.sleep()

    def normalize_stats(self):
        self.fullness = max(0, min(100, self.fullness))
        self.happiness = max(0, min(100, self.happiness))
