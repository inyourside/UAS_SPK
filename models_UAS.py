from sqlalchemy import String, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


class Base(declarative_base):
    pass


class Smartphone(Base):
    __tablename__ = "tbl_xiaomi"
    no = Mapped[Integer] = mapped_column(primary_key=True)
    type = Mapped[String] = mapped_column()
    kamera = Mapped[String] = mapped_column()
    baterai = Mapped[String] = mapped_column()
    layar = Mapped[String] = mapped_column()
    ram = Mapped[String] = mapped_column()
    processor = Mapped[String] = mapped_column()
    harga = Mapped[String] = mapped_column()
    benefit = Mapped[String] = mapped_column()

    def __repr__(self):
        return f"Smartphone(type={self.type!r}, kamera={self.kamera!r}, baterai={self.baterai!r}, layar={self.layar!r}, ram={self.ram!r}, processor={self.processor!r}, harga={self.harga!r}, benefit={self.benefit!r})"
