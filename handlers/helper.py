from handlers.database import Database
from handlers.roles import Roles

# Role based authentication function
async def has_role(ctx, role_name: str):
    db = Database()
    user_data = db.universal_find_one('users', {'user_id': ctx.author.id})
    if not user_data:
        return False
    role = Roles.from_name(user_data['role'])
    if role.name == role_name:
        return True
    return False
