from datetime import datetime

class Memo:
    """Mewakili satu memo dengan judul, konten, dan tanggal pembuatan."""
    def __init__(self, judul, content, created_tanggal=None):
        self.judul = judul
        self.content = content
        if created_tanggal:
            self.created_tanggal = created_tanggal
        else:
            self.created_tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Judul: {self.judul}\nTanggal: {self.created_tanggal}\nKonten:\n{self.content}\n"

    def update_content(self, new_content):
        self.content = new_content

    def update_judul(self, new_judul):
        self.judul = new_judul

    def to_dict(self):
        return {
            "judul": self.judul,
            "content": self.content,
            "created_tanggal": self.created_tanggal
        }

    @staticmethod
    def from_dict(data):
        created_tanggal = data.get("created_tanggal", None)
        return Memo(data["judul"], data["content"], created_tanggal)