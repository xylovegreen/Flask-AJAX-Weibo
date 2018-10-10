import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()


class UserRoleEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def userrole_encoder(d):
    if UserRoleEncoder.prefix in d:
        name = d[UserRoleEncoder.prefix]
        return UserRole[name]
    else:
        return d
