import random
import string

def generate_sale_code():
    """Génère un code de vente unique aléatoire."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))