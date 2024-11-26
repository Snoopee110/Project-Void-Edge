import enum

class Roles(enum.Enum):
    OWNER         = ('Owner', '<:owner:1310811192377475093>', 'This user is the owner of the bot.')
    ADMINISTRATOR = ('Administrator', '<:administrator:1309366532664721550>', 'This user is a bot administrator.')
    GLOBAL_MOD    = ('Global Moderator', '<:global_mod:1309366625262243911>', 'This user is a global bot moderator.')
    QUOTEBOOK_MOD = ('Quotebook Gatekeeper', '<:quotebook_mod:1309366653196304425>', 'This user is a moderator of the quotebook.')

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
        """Normalize a name to match the enum's name format."""
        return name.title()

    @classmethod
    def from_name(cls, name):
        """Get enum by its name, ensuring normalization."""
        normalized_name = cls.normalize_name(name)
        for badge in cls:
            if badge.name == normalized_name:
                return badge
        raise ValueError(f"No badge with name '{normalized_name}' found.")
