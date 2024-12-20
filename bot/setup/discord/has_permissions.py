from bot.setup.discord.user_ids import BOT_OWNER_ID, DEATHZONE_VIZE_ID, ACADEMY_VIZE_ID, IMMO_VIZE_ID, UTOPIA_VIZE_ID, FIGHTERZ_VIZE_ID

def has_permission(user, permission_type):
    if permission_type == 'owner':
        return user.id == BOT_OWNER_ID
    elif permission_type == 'dzvize':
        return any(role.id == DEATHZONE_VIZE_ID for role in user.roles)
    elif permission_type == 'acvize':
        return any(role.id == ACADEMY_VIZE_ID for role in user.roles)
    elif permission_type == 'imvize':
        return any(role.id == IMMO_VIZE_ID for role in user.roles)
    elif permission_type == 'utvize':
        return any(role.id == UTOPIA_VIZE_ID for role in user.roles)
    elif permission_type == 'fzvize':
        return any(role.id == FIGHTERZ_VIZE_ID for role in user.roles)
    else:
        return False