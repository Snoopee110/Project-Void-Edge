from enum import Enum

class Badges(Enum):
    # Staff Given Badges
    BOT_DEVELOPER = ('Bot Developer', '<:bot_developer:1309366562435760190>', 'This user is a developer of the bot.')
    CONTRIBUTOR   = ('Contributor', '<:contributor:1309366597219123250>', 'This user has contributed to the bot in some way.')
    STAFF         = ('Staff', '<:staff:1310812514140819478>', 'This user is a staff member of the bot.')


    @property
    def name(self):
        return self.value[0]

    @property
    def emoji(self):
        return self.value[1] if self.value[1] != '0' else None

    @property
    def description(self):
        return self.value[2]

    @classmethod
    def normalize_name(cls, name):
        return name.title()

    @classmethod
    def from_name(cls, name):
        """Get enum by its name, ensuring normalization."""
        normalized_name = cls.normalize_name(name)
        for badge in cls:
            if badge.name == normalized_name:
                return badge
        raise ValueError(f"No badge with name '{normalized_name}' found.")


class LevelBadges(Enum):
    LEVEL_5  =  ('Level 5', 0, 'This user has reached level 5.', 5)
    LEVEL_10 =  ('Level 10', 0, 'This user has reached level 10.', 10)
    LEVEL_20 =  ('Level 15', 0, 'This user has reached level 20.', 20)
    LEVEL_30 =  ('Level 30', 0, 'This user has reached level 30.', 30)
    LEVEL_40 =  ('Level 40', 0, 'This user has reached level 40.', 40)
    LEVEL_50 =  ('Level 50', 0, 'This user has reached level 50.', 50)
    LEVEL_100 = ('Level 100', 0, 'This user has reached level 100.', 100)

    @property
    def name(self):
        return self.value[0]

    @property
    def emoji(self):
        return self.value[1]

    @property
    def description(self):
        return self.value[2]

    @property
    def level(self):
        return self.value[3]
