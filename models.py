from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Smartphone(Base):
    __tablename__ = "tbl_xiaomi"
    no = Column(Integer, primary_key=True)
    type = Column(String(255))
    kamera = Column(String(255))
    baterai = Column(String(255))
    layar = Column(String(255))
    ram = Column(String(255))
    processor = Column(String(255))
    harga = Column(String(255))
    benefit = Column(String(255))

    def __init__(self, type, kamera, baterai, layar, ram, processor, harga, benefit):
        self.type = type
        self.kamera = kamera
        self.baterai = baterai
        self.layar = layar
        self.ram = ram
        self.processor = processor
        self.harga = harga
        self.benefit = benefit

    def calculate_score(self, dev_scale):
        score = 0
        score += self.kamera * dev_scale['kamera']
        score += self.baterai * dev_scale['baterai']
        score += self.layar * dev_scale['layar']
        score += self.ram * dev_scale['ram']
        score += self.processor * dev_scale['processor']
        score -= self.harga * dev_scale['harga']
        return score

    def __repr__(self):
        return f"Smartphone(type={self.type!r}, kamera={self.kamera!r}, baterai={self.baterai!r}, layar={self.layar!r}, ram={self.ram!r}, processor={self.processor!r}, harga={self.harga!r}, benefit={self.benefit!r})"
