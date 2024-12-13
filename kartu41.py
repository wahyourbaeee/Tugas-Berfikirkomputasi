import random

class Kartu:
    def __init__(self, jenis, nilai, simbol):
        self.jenis = jenis
        self.nilai = nilai
        self.simbol = simbol

    def __str__(self):
        return f"{self.simbol} {self.jenis} ({self.nilai})"

    def __eq__(self, other):
        return self.jenis == other.jenis

class Pemain:
    def __init__(self, nama):
        self.nama = nama
        self.kartu = []

    def tambah_kartu(self, kartu):
        self.kartu.append(kartu)

    def hapus_kartu(self, index):
        return self.kartu.pop(index)

    def hitung_total_kartu(self):
        return sum(kartu.nilai for kartu in self.kartu)

    def cek_kartu_sejenis(self):
        # Cek apakah semua kartu memiliki jenis yang sama dan totalnya 41
        if len(set(kartu.jenis for kartu in self.kartu)) == 1 and self.hitung_total_kartu() == 41:
            return True
        return False

class GameKartu41:
    def __init__(self, nama_pemain):
        self.deck = self.buat_deck()
        self.pemain = [Pemain(nama) for nama in nama_pemain]
        self.tumpukan_kartu_buangan = []
        self.kartu_dibuka = None

    def buat_deck(self):
        jenis = ['Sekop', 'Hati', 'Wajik', 'Keriting']
        simbol = ['♠', '♥', '♦', '♣']
        nilai = {
            'As': 11, 'King': 10, 'Queen': 10, 'Jack': 10,
            '10': 10, '9': 9, '8': 8, '7': 7, '6': 6,
            '5': 5, '4': 4, '3': 3, '2': 2
        }
        deck = []
        for j, s in zip(jenis, simbol):
            for n, v in nilai.items():
                deck.append(Kartu(j, v, f"{n}{s}"))
        random.shuffle(deck)
        return deck

    def bagikan_kartu(self):
        for pemain in self.pemain:
            for _ in range(4):
                pemain.tambah_kartu(self.deck.pop())

    def tampilkan_kartu_pemain(self, pemain):
        print(f"\nKartu {pemain.nama}:")
        for i, kartu in enumerate(pemain.kartu):
            print(f"{i+1}. {kartu}")
        print(f"Total: {pemain.hitung_total_kartu()}")

    def mulai_permainan(self):
        self.bagikan_kartu()
        self.kartu_dibuka = self.deck.pop()
        self.tumpukan_kartu_buangan.append(self.kartu_dibuka)

        giliran = 0
        while True:
            pemain_sekarang = self.pemain[giliran]
            print(f"\n--- Giliran {pemain_sekarang.nama} ---")
            print(f"Kartu terakhir di tumpukan: {self.kartu_dibuka}")
            self.tampilkan_kartu_pemain(pemain_sekarang)

            # Pilih kartu untuk diambil
            print("\nPilih kartu untuk diambil:")
            print("1. Kartu terakhir di tumpukan")
            print("2. Kartu baru dari deck")
            pilihan = input("Masukkan pilihan (1/2): ")

            if pilihan == '1':
                pemain_sekarang.tambah_kartu(self.kartu_dibuka)
            else:
                pemain_sekarang.tambah_kartu(self.deck.pop())

            # Tampilkan kartu setelah pengambilan
            self.tampilkan_kartu_pemain(pemain_sekarang)

            # Membuang kartu
            while True:
                try:
                    index_buang = int(input("Pilih nomor kartu untuk dibuang (1-5): ")) - 1
                    self.kartu_dibuka = pemain_sekarang.hapus_kartu(index_buang)
                    self.tumpukan_kartu_buangan.append(self.kartu_dibuka)
                    break
                except (ValueError, IndexError):
                    print("Pilihan tidak valid. Coba lagi.")

            # Cek pemenang (kartu sejenis dan total 41)
            if pemain_sekarang.cek_kartu_sejenis():
                print(f"\n🎉 {pemain_sekarang.nama} MENANG! 🎉")
                print("Kartu pemenang:")
                for kartu in pemain_sekarang.kartu:
                    print(kartu)
                break

            # Cek kartu habis
            if not self.deck:
                print("Deck habis. Permainan berakhir seri.")
                break

            giliran = (giliran + 1) % len(self.pemain)

def main():
    nama_pemain = []
    for i in range(3):
        nama = input(f"Masukkan nama Pemain {i+1}: ")
        nama_pemain.append(nama)

    game = GameKartu41(nama_pemain)
    game.mulai_permainan()

if __name__ == "__main__":
    main()
