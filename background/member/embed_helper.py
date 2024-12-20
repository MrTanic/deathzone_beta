import nextcord

def create_embed(title, description, color):
    return nextcord.Embed(title=title, description=description, color=color)

def create_error_embed(description):
    return create_embed("Fehler", description, 0xff0000)

def create_success_embed(description):
    return create_embed("Mitglieder-Datenbank Update", description, 0x00ff00)