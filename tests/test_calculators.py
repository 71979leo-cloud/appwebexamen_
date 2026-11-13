import unittest

from app import app


class PortalTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_all_seven_pages_load(self):
        for path in (
            "/",
            "/compra",
            "/salario",
            "/temperatura",
            "/empresa",
            "/servicios",
            "/contacto",
        ):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_calculator_fields_do_not_show_example_placeholders(self):
        for path in ("/compra", "/salario", "/temperatura"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertNotIn("placeholder=", response.get_data(as_text=True))

    def test_purchase_with_discount(self):
        response = self.client.post("/compra", data={"cantidad": "5", "precio": "250"})
        page = response.get_data(as_text=True)
        self.assertIn("$1,250.00", page)
        self.assertIn("$125.00", page)
        self.assertIn("$1,125.00", page)
        self.assertIn("5 × $250.00", page)

    def test_purchase_without_discount(self):
        response = self.client.post("/compra", data={"cantidad": "2", "precio": "250"})
        page = response.get_data(as_text=True)
        self.assertIn("$500.00", page)
        self.assertIn("El descuento se aplica", page)

    def test_salary_with_overtime(self):
        response = self.client.post("/salario", data={"horas": "45", "pago_hora": "100"})
        page = response.get_data(as_text=True)
        self.assertIn("$4,000.00", page)
        self.assertIn("$1,000.00", page)
        self.assertIn("$5,000.00", page)

    def test_salary_without_overtime(self):
        response = self.client.post("/salario", data={"horas": "40", "pago_hora": "100"})
        page = response.get_data(as_text=True)
        self.assertIn("$4,000.00", page)
        self.assertIn("0 h extra", page)

    def test_temperature_conversion(self):
        response = self.client.post("/temperatura", data={"celsius": "25"})
        page = response.get_data(as_text=True)
        self.assertIn("77<small>°F</small>", page)
        self.assertIn("298.15<small>K</small>", page)

    def test_temperature_accepts_negative_celsius(self):
        response = self.client.post("/temperatura", data={"celsius": "-40"})
        page = response.get_data(as_text=True)
        self.assertIn("-40<small>°F</small>", page)
        self.assertIn("233.15<small>K</small>", page)

    def test_invalid_purchase_is_reported(self):
        response = self.client.post("/compra", data={"cantidad": "-2", "precio": "100"})
        self.assertIn("igual o mayor que cero", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
