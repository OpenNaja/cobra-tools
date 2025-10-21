from generated.base_enum import BaseEnum


class ActionScope(BaseEnum):
    GAME_OBJECT_SWITCH: ActionScope
    GLOBAL: ActionScope
    GAME_OBJECT_ID: ActionScope
    GAME_OBJECT_STATE: ActionScope
    ALL: ActionScope
    ALL_EXCEPT_ID: ActionScope
