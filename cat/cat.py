from dataclasses import asdict, dataclass
from random import randint


@dataclass
class Cat:
    SAD_AVATAR = 'cat/images/cat_sad.svg'
    CALM_AVATAR = 'cat/images/cat_calm.svg'
    HAPPY_AVATAR = 'cat/images/cat_happy.svg'
    SLEEPING_AVATAR = 'cat/images/cat_sleeping.svg'

    name: str
    age: int = 1
    fullness: int = 40
    happiness: int = 40
    is_sleeping: bool = False

    @classmethod
    def from_session(cls, data):
        return cls(
            name=data.get('name', ''),
            age=data.get('age', 1),
            fullness=data.get('fullness', 40),
            happiness=data.get('happiness', 40),
            is_sleeping=data.get('is_sleeping', False),
        )

    def to_session(self):
        return asdict(self)

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

        self.normalize()

    def play(self):
        if self.is_sleeping:
            self.is_sleeping = False
            self.happiness -= 5
            self.normalize()
            return

        self.happiness += 15
        self.fullness -= 10

        if randint(1, 3) == 1:
            self.happiness = 0

        self.normalize()

    def sleep(self):
        self.is_sleeping = True
        self.normalize()

    def apply_action(self, action):
        actions = {
            'feed': self.feed,
            'play': self.play,
            'sleep': self.sleep,
        }
        if action in actions:
            actions[action]()

    def normalize(self):
        self.fullness = max(0, min(100, self.fullness))
        self.happiness = max(0, min(100, self.happiness))
