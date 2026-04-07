from django import template

register = template.Library()

@register.filter
def cop_format(value):
    """
    Formatea un número a formato de moneda colombiana usando puntos como separador de miles.
    Ejemplo: 200000 -> 200.000
    """
    try:
        value = float(value)
        # Formatear a string con comas para miles: "200,000"
        formatted = "{:,.0f}".format(value)
        # Reemplazar la coma por punto: "200.000"
        return formatted.replace(",", ".")
    except (ValueError, TypeError):
        return value
