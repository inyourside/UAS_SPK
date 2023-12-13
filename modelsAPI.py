from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
import numpy as np
import pandas as pd

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


class Movie():
    def __init__(self) -> None:
        self.movies = pd.read_csv('ml-latest-small/movies.csv')
        self.matrix = pd.read_csv('ml-latest-small/matrix_by_id.csv')
        self.films = np.array(self.movies)

    @property
    def film_data(self):
        data = []
        for film in self.films:
            data.append({'movie_id': film[0], 'movie_title': film[1]})
        return data

    @property
    def film_data_dict(self):
        data = {}
        for film in self.films:
            data[film[0]] = film[1]
        return data

    def pearson(self, s1, s2):
        s1_c = s1-s1.mean()
        s2_c = s2-s2.mean()
        return np.sum(s1_c*s2_c)/np.sqrt(np.sum(s1_c**2)*np.sum(s2_c**2))

    def get_recs(self, movie_id, num):
        reviews = []
        movie_id = str(movie_id)
        for id in self.matrix.columns:
            if id == movie_id:
                continue
            cor = self.pearson(self.matrix[movie_id], self.matrix[id])
            if np.isnan(cor):
                continue
            else:
                reviews.append((id, cor))
            reviews.sort(key=lambda tup: tup[1], reverse=True)
        return reviews[:num]


class Xiaomi():
    def __init__(self) -> None:
        self.xiaomi = pd.read_csv('ml-latest-small/xiaomi.csv')
        self.matrix_xiaomi = pd.read_csv(
            'ml-latest-small/matrix_by_id_xiaomi.csv')
        self.hps = np.array(self.xiaomi)

    @property
    def hp_data(self):
        data = []
        for hp in self.hps:
            data.append({'No': hp[0], 'type': hp[2],
                        'Battery': hp[4], 'RAM': hp[6], 'WP Score': hp[10], 'SAW Score': hp[11]})
        return data

    @property
    def hp_data_dict(self):
        data = {}
        for hp in self.hps:
            data[hp[0]] = hp[2]
        return data

    def pearson(self, s1, s2):
        s1_c = s1-s1.mean()
        s2_c = s2-s2.mean()
        return np.sum(s1_c*s2_c)/np.sqrt(np.sum(s1_c**2)*np.sum(s2_c**2))

    def get_recs(self, ID, num):
        reviews = []
        ID = str(ID)
        for ID in self.matrix_xiaomi.columns:
            if ID == ID:
                continue
            cor = self.pearson(
                self.matrix_xiaomi[ID], self.matrix_xiaomi[ID])
            if np.isnan(cor):
                continue
            else:
                reviews.append((ID, cor))
            reviews.sort(key=lambda tup: tup[0], reverse=True)
        return reviews[:num]
