from decimal import Decimal, InvalidOperation

from flask import Flask, render_template, request


app = Flask(__name__)
app.config["SECRET_KEY"] = "portal-de-servicios-local"


def parse_decimal(form, field, label, allow_negative=False):
    raw_value = form.get(field, "").strip()
    if not raw_value:
        raise ValueError(f"Ingresa {label.lower()}.")

    try:
        value = Decimal(raw_value)
    except InvalidOperation as error:
        raise ValueError(f"Ingresa un valor numérico válido para {label.lower()}.") from error

    if not value.is_finite():
        raise ValueError(f"{label} debe ser un número válido.")
    if not allow_negative and value < 0:
        raise ValueError(f"{label} debe ser un número igual o mayor que cero.")
    return value


def money(value):
    return f"${value:,.2f}"


def number(value):
    return f"{value.normalize():f}"


def render_calculator(template, **context):
    return render_template(template, **context)


@app.get("/")
def inicio():
    return render_template("inicio.html", active_page="inicio")


@app.route("/compra", methods=["GET", "POST"])
def compra():
    values = {"cantidad": "", "precio": ""}
    result = None
    error = None

    if request.method == "POST":
        values = {
            "cantidad": request.form.get("cantidad", "").strip(),
            "precio": request.form.get("precio", "").strip(),
        }
        try:
            cantidad_decimal = parse_decimal(request.form, "cantidad", "Cantidad")
            if cantidad_decimal != cantidad_decimal.to_integral_value() or cantidad_decimal == 0:
                raise ValueError("La cantidad debe ser un número entero mayor que cero.")
            cantidad = int(cantidad_decimal)
            precio = parse_decimal(request.form, "precio", "Precio unitario")
            subtotal = cantidad * precio
            descuento = subtotal * Decimal("0.10") if subtotal > Decimal("1000") else Decimal("0")
            total = subtotal - descuento
            result = {
                "cantidad": cantidad,
                "precio": money(precio),
                "subtotal": money(subtotal),
                "descuento": money(descuento),
                "total": money(total),
                "aplica_descuento": descuento > 0,
            }
        except ValueError as validation_error:
            error = str(validation_error)

    return render_calculator(
        "compra.html",
        active_page="compra",
        values=values,
        result=result,
        error=error,
    )


@app.route("/salario", methods=["GET", "POST"])
def salario():
    values = {"horas": "", "pago_hora": ""}
    result = None
    error = None

    if request.method == "POST":
        values = {
            "horas": request.form.get("horas", "").strip(),
            "pago_hora": request.form.get("pago_hora", "").strip(),
        }
        try:
            horas = parse_decimal(request.form, "horas", "Horas trabajadas")
            pago_hora = parse_decimal(request.form, "pago_hora", "Pago por hora")
            horas_normales = min(horas, Decimal("40"))
            horas_extra = max(horas - Decimal("40"), Decimal("0"))
            pago_normal = horas_normales * pago_hora
            pago_extra = horas_extra * pago_hora * Decimal("2")
            result = {
                "horas": number(horas),
                "pago_hora": money(pago_hora),
                "horas_normales": number(horas_normales),
                "horas_extra": number(horas_extra),
                "pago_normal": money(pago_normal),
                "pago_extra": money(pago_extra),
                "total": money(pago_normal + pago_extra),
            }
        except ValueError as validation_error:
            error = str(validation_error)

    return render_calculator(
        "salario.html",
        active_page="salario",
        values=values,
        result=result,
        error=error,
    )


@app.route("/temperatura", methods=["GET", "POST"])
def temperatura():
    values = {"celsius": ""}
    result = None
    error = None

    if request.method == "POST":
        values = {"celsius": request.form.get("celsius", "").strip()}
        try:
            celsius = parse_decimal(
                request.form, "celsius", "Temperatura en Celsius", allow_negative=True
            )
            fahrenheit = celsius * Decimal("9") / Decimal("5") + Decimal("32")
            kelvin = celsius + Decimal("273.15")
            result = {
                "celsius": number(celsius),
                "fahrenheit": number(fahrenheit),
                "kelvin": number(kelvin),
            }
        except ValueError as validation_error:
            error = str(validation_error)

    return render_calculator(
        "temperatura.html",
        active_page="temperatura",
        values=values,
        result=result,
        error=error,
    )


@app.get("/empresa")
def empresa():
    return render_template("empresa.html", active_page="empresa")


@app.get("/servicios")
def servicios():
    return render_template("servicios.html", active_page="servicios")


@app.get("/contacto")
def contacto():
    return render_template("contacto.html", active_page="contacto")


if __name__ == "__main__":
    app.run()
