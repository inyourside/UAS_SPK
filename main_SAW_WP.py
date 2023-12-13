import sys
from colorama import Fore, Style
from models import Base, Smartphone
from engine import engine
from tabulate import tabulate

from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import DEV_SCALE

session = Session(engine)


def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')


def review_data():
    query = select(Smartphone)
    for phone in session.scalars(query):
        print(phone)


class BaseMethod():

    def __init__(self):
        # 1-5
        self.raw_weight = {'kamera': 3, 'baterai': 4,
                           'layar': 3, 'ram': 4, 'processor': 5, 'harga': 5}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Smartphone.no, Smartphone.type, Smartphone.kamera, Smartphone.baterai, Smartphone.layar,
                       Smartphone.ram, Smartphone.processor, Smartphone.harga, Smartphone.benefit)
        result = session.execute(query).fetchall()
        return [{'no': phone.no, 'type': phone.type, 'kamera': phone.kamera, 'baterai': phone.baterai,
                'layar': phone.layar, 'ram': phone.ram, 'processor': phone.processor, 'harga': phone.harga} for phone in result]

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
            processor_value = DEV_SCALE['processor'].get(data['processor'], 1)
            processor_values.append(processor_value)

            # Harga
            harga_cleaned = ''.join(
                char for char in data['harga'] if char.isdigit())
            harga_values.append(float(harga_cleaned)
                                if harga_cleaned else 0)  # Convert to float

        return [
            {'no': data['no'],
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


class WeightedProduct(BaseMethod):
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
                row['harga']**self.weight['harga']
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)
        sorted_data = [
            {
                'no': product['no'],
                'score': product['produk']  # Nilai skor akhir
            }
            for product in sorted_produk
        ]
        return sorted_data


class SimpleAdditiveWeighting(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['no']:
                  round(row['kamera'] * weight['kamera'] +
                        row['baterai'] * weight['baterai'] +
                        row['layar'] * weight['layar'] +
                        row['ram'] * weight['ram'] +
                        row['processor'] * weight['processor'] +
                        row['harga'] * weight['harga'], 3)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result


def run_saw():
    saw = SimpleAdditiveWeighting()
    result = saw.calculate
    print(tabulate(result.items(), headers=['no', 'Score'], tablefmt='grid'))


def run_wp():
    wp = WeightedProduct()
    result = wp.calculate
    headers = result[0].keys()
    rows = [
        {k: round(v, 3) if isinstance(v, float) else v for k, v in val.items()}
        for val in result
    ]
    print(tabulate(rows, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == 'create_table':
            create_table()
        elif arg == 'saw':
            run_saw()
        elif arg == 'wp':
            run_wp()
        else:
            print('command not found')
