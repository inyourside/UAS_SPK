from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api
from models import Smartphone as SmartphoneModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from tabulate import tabulate

session = Session(engine)

app = Flask(__name__)
api = Api(app)


class BaseMethod():

    def __init__(self):
        self.raw_weight = {'kamera': 3, 'baterai': 4,
                           'layar': 3, 'ram': 4, 'processor': 5, 'harga': 5}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(SmartphoneModel.no, SmartphoneModel.type, SmartphoneModel.kamera, SmartphoneModel.baterai, SmartphoneModel.layar,
                       SmartphoneModel.ram, SmartphoneModel.processor, SmartphoneModel.harga, SmartphoneModel.benefit)
        result = session.execute(query).fetchall()
        print(result)
        return [{'no': Smartphone.no, 'type': Smartphone.type, 'kamera': Smartphone.kamera, 'baterai': Smartphone.baterai,
                'layar': Smartphone.layar, 'ram': Smartphone.ram, 'processor': Smartphone.processor, 'harga': Smartphone.harga} for Smartphone in result]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        kamera_values = []  # max
        baterai_values = []  # max
        layar_values = []  # max
        ram_values = []  # max
        processor_values = []  # max
        harga_values = []  # min

        for data in self.data:
            # Kamera
            kamera_spec = data['kamera']
            numeric_values = [int(value.split()[0]) for value in kamera_spec.split(
                ',') if value.split()[0].isdigit()]
            max_kamera_value = max(numeric_values) if numeric_values else 1
            kamera_values.append(max_kamera_value)

            # Baterai
            baterai_spec = data['baterai']
            baterai_numeric_values = [int(
                value.split()[0]) for value in baterai_spec.split() if value.split()[0].isdigit()]
            max_baterai_value = max(
                baterai_numeric_values) if baterai_numeric_values else 1
            baterai_values.append(max_baterai_value)

            # Layar
            layar_spec = data['layar']
            layar_numeric_values = [float(value.split()[0]) for value in layar_spec.split(
            ) if value.replace('.', '').isdigit()]
            max_layar_value = max(
                layar_numeric_values) if layar_numeric_values else 1
            layar_values.append(max_layar_value)

            # RAM
            ram_spec = data['ram']
            ram_numeric_values = [
                int(value) for value in ram_spec.split() if value.isdigit()]
            max_ram_value = max(
                ram_numeric_values) if ram_numeric_values else 1
            ram_values.append(max_ram_value)

            # Processor
            processor_spec = data['processor']
            processor_numeric_values = [
                int(value) for value in processor_spec.split() if value.isdigit()]
            max_processor_value = max(
                processor_numeric_values) if processor_numeric_values else 1
            processor_values.append(max_processor_value)

            # Harga
            harga_cleaned = ''.join(
                char for char in data['harga'] if char.isdigit())
            harga_values.append(float(harga_cleaned)
                                if harga_cleaned else 0)  # Convert to float

        return [
            {'no': data['no'],
             'type': data['type'],
             'kamera': kamera_value / max(kamera_values),
             'baterai': baterai_value / max(baterai_values),
             'layar': layar_value / max(layar_values),
             'ram': ram_value / max(ram_values),
             'processor': processor_value / max(processor_values),
             # To avoid division by zero
             'harga': min(harga_values) / max(harga_values) if max(harga_values) != 0 else 0
             }
            for data, kamera_value, baterai_value, layar_value, ram_value, processor_value, harga_value
            in zip(self.data, kamera_values, baterai_values, layar_values, ram_values, processor_values, harga_values)
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights


class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = [
            {
                'no': row['no'],
                'produk': row['kamera']**self.weight['kamera'] *
                row['baterai']**self.weight['baterai'] *
                row['layar']**self.weight['layar'] *
                row['ram']**self.weight['ram'] *
                row['processor']**self.weight['processor'] *
                row['harga']**self.weight['harga'],
                'type': row.get('type', '')
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)
        sorted_data = [
            {
                'ID': product['no'],
                'type': product['type'],
                'score': round(product['produk'], 3)
            }
            for product in sorted_produk
        ]
        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return sorted(result, key=lambda x: x['score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'xiaomi': sorted(result, key=lambda x: x['score'], reverse=True)}, HTTPStatus.OK.value


class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = [
            {
                'ID': row['no'],
                'type': row.get('type'),
                'Score': round(row['kamera'] * weight['kamera'] +
                               row['baterai'] * weight['baterai'] +
                               row['layar'] * weight['layar'] +
                               row['ram'] * weight['ram'] +
                               row['processor'] * weight['processor'] +
                               row['harga'] * weight['harga'], 3)
            }
            for row in self.normalized_data
        ]
        sorted_result = sorted(result, key=lambda x: x['Score'], reverse=True)
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights


class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return sorted(result, key=lambda x: x['Score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'xiaomi': sorted(result, key=lambda x: x['Score'], reverse=True)}, HTTPStatus.OK.value


class Smartphone(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None

        if page > page_count or page < 1:
            abort(404, description=f'Data Tidak Ditemukan.')
        return {
            'page': page,
            'page_size': page_size,
            'next': next_page,
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = session.query(SmartphoneModel).order_by(SmartphoneModel.no)
        result_set = query.all()
        data = [{'no': row.no, 'type': row.type, 'kamera': row.kamera, 'baterai': row.baterai,
                 'layar': row.layar, 'ram': row.ram, 'processor': row.processor, 'harga': row.harga}
                for row in result_set]
        return self.get_paginated_result('xiaomi/', data, request.args), 200


api.add_resource(Smartphone, '/xiaomi')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)
