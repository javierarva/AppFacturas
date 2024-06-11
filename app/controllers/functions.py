import re

def confirmar(prompt):
    return input(prompt + "(s/n): ").strip().lower() == 's'

def valor_valido(valor, tipo):
    if 'int' in tipo:
        return valor.isdigit()
    elif 'double' in tipo or 'float' in tipo:
        try:
            float(valor)
            return True
        except ValueError:
            return False
    elif 'varchar' in tipo or 'text' in tipo:
        return True
    elif 'date' in tipo:
        return re.match(r'^\d{4}-\d{2}-\d{2}$', valor) is not None
    return True