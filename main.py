import random, os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import QLabel
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

# --- BASE DE DATOS MUNDIAL AMPLIADA (175 PAÍSES) ---
PAISES = {
    "España": ["Madrid", "Barcelona", "Valencia"], "Francia": ["París", "Marsella", "Lyon"],
    "Italia": ["Roma", "Milán", "Nápoles"], "Alemania": ["Berlín", "Hamburgo", "Múnich"],
    "Portugal": ["Lisboa", "Oporto", "Braga"], "Grecia": ["Atenas", "Tesalónica", "Patras"],
    "Reino Unido": ["Londres", "Manchester", "Liverpool"], "Irlanda": ["Dublín", "Cork", "Galway"],
    "Bélgica": ["Bruselas", "Amberes", "Gante"], "Países Bajos": ["Ámsterdam", "Rotterdam", "Utrecht"],
    "Suiza": ["Berna", "Zúrich", "Ginebra"], "Austria": ["Viena", "Salzburgo", "Innsbruck"],
    "Suecia": ["Estocolmo", "Gotemburgo", "Malmö"], "Noruega": ["Oslo", "Bergen", "Stavanger"],
    "Dinamarca": ["Copenhague", "Aarhus", "Odense"], "Finlandia": ["Helsinki", "Espoo", "Tampere"],
    "Polonia": ["Varsovia", "Cracovia", "Lodz"], "Rumanía": ["Bucarest", "Cluj", "Iasi"],
    "Hungría": ["Budapest", "Debrecen", "Szeged"], "República Checa": ["Praga", "Brno", "Ostrava"],
    "Ucrania": ["Kiev", "Járkov", "Odesa"], "Croacia": ["Zagreb", "Split", "Rijeka"],
    "Bulgaria": ["Sofía", "Plovdiv", "Varna"], "Serbia": ["Belgrado", "Novi Sad", "Nis"],
    "EE.UU.": ["Washington D.C.", "Nueva York", "Chicago"], "Canadá": ["Ottawa", "Toronto", "Montreal"],
    "México": ["CDMX", "Guadalajara", "Monterrey"], "Brasil": ["Brasilia", "Sao Paulo", "Río"],
    "Argentina": ["Buenos Aires", "Córdoba", "Rosario"], "Chile": ["Santiago", "Valparaíso", "Concepción"],
    "Colombia": ["Bogotá", "Medellín", "Cali"], "Perú": ["Lima", "Arequipa", "Trujillo"],
    "Uruguay": ["Montevideo", "Salto", "Maldonado"], "Paraguay": ["Asunción", "Encarnación", "Villarrica"],
    "Bolivia": ["Sucre", "La Paz", "Santa Cruz"], "Ecuador": ["Quito", "Guayaquil", "Cuenca"],
    "Venezuela": ["Caracas", "Maracaibo", "Valencia"], "Panamá": ["Panamá", "Colón", "David"],
    "Costa Rica": ["San José", "Alajuela", "Cartago"], "Guatemala": ["Guatemala", "Antigua", "Mixco"],
    "Honduras": ["Tegucigalpa", "San Pedro", "La Ceiba"], "Nicaragua": ["Managua", "León", "Granada"],
    "Japón": ["Tokio", "Osaka", "Kioto"], "China": ["Pekín", "Shanghái", "Cantón"],
    "Corea del Sur": ["Seúl", "Busán", "Incheon"], "India": ["Nueva Delhi", "Bombay", "Calcuta"],
    "Australia": ["Canberra", "Sídney", "Melbourne"], "Egipto": ["El Cairo", "Alejandría", "Guiza"],
    "Sudáfrica": ["Pretoria", "Ciudad del Cabo", "Durban"], "Marruecos": ["Rabat", "Casablanca", "Marrakech"],
    "Tailandia": ["Bangkok", "Phuket", "Chiang Mai"], "Vietnam": ["Hanói", "Saigón", "Da Nang"],
    "Indonesia": ["Yakarta", "Surabaya", "Bandung"], "Filipinas": ["Manila", "Quezón", "Davao"],
    "Israel": ["Jerusalén", "Tel Aviv", "Haifa"], "Arabia Saudita": ["Riad", "Yeda", "Dammam"],
    "Turquía": ["Ankara", "Estambul", "Esmirna"], "Nueva Zelanda": ["Wellington", "Auckland", "Christchurch"],
    "Nigeria": ["Abuya", "Lagos", "Kano"], "Argelia": ["Argel", "Orán", "Constantina"],
    "Islandia": ["Reikiavik", "Akureyri", "Kópavogur"], "Mónaco": ["Mónaco", "Montecarlo", "Fontvieille"],
    "Andorra": ["Andorra la Vella", "Encamp", "Escaldes"], "Malta": ["La Valeta", "Sliema", "Mosta"],
    "Singapur": ["Singapur", "Jurong", "Changi"], "Malasia": ["Kuala Lumpur", "George Town", "Ipoh"],
    "Cuba": ["La Habana", "Santiago", "Camagüey"], "Jamaica": ["Kingston", "Montego Bay", "Spanish Town"],
    "Etiopía": ["Adís Abeba", "Dire Dawa", "Gondar"], "Ghana": ["Acra", "Kumasi", "Tamale"],
    "Kenia": ["Nairobi", "Mombasa", "Kisumu"], "Senegal": ["Dakar", "Touba", "Thiès"],
    "Paquistán": ["Islamabad", "Karachi", "Lahore"], "Irak": ["Bagdad", "Basora", "Erbil"],
    "Irán": ["Teherán", "Mashhad", "Isfahán"], "Afganistán": ["Kabul", "Herat", "Kandahar"],
    "Nepal": ["Katmandú", "Pojara", "Lalitpur"], "Líbano": ["Beirut", "Trípoli", "Sidón"],
    "Jordania": ["Amán", "Zarqa", "Irbid"], "Kuwait": ["Ciudad de Kuwait", "Jahra", "Ahmadi"]
}

class QuizApp(App):
    def build(self):
        self.score, self.lives = 0, 5
        self.current_sound = None
        self.playlist = ["musica_fondo.mp3"] + [f"musica_fondo{i}.mp3" for i in range(2, 7)]
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # BCN Info
        self.info = QLabel(text="BCN: --:--:-- | 8°C ☀", color=get_color_from_hex("#FFFF00"), size_hint_y=0.1)
        layout.addWidget(self.info)
        Clock.schedule_interval(self.update_info, 1)

        # Pregunta
        self.q_label = QLabel(text="DESAFÍO 175 PAÍSES", font_size='20sp', halign='center', size_hint_y=0.2)
        layout.addWidget(self.q_label)

        # Barra
        self.pb = ProgressBar(max=1000, value=0, size_hint_y=0.05)
        layout.addWidget(self.pb)

        # Botones
        self.btns = []
        for _ in range(3):
            btn = Button(text="-", background_color=get_color_from_hex("#000044"), size_hint_y=0.15)
            btn.bind(on_release=self.check)
            self.btns.append(btn)
            layout.addWidget(btn)

        # Shuffle & Stats
        bot_box = BoxLayout(size_hint_y=0.1)
        self.shuffle_btn = Button(text="SHUFFLE >>", background_color=get_color_from_hex("#004400"))
        self.shuffle_btn.bind(on_release=lambda x: self.play_music())
        self.score_label = QLabel(text="PTS: 0")
        bot_box.addWidget(self.score_label)
        bot_box.addWidget(self.shuffle_btn)
        layout.addWidget(bot_box)

        self.lives_label = QLabel(text="VIDAS: ❤❤❤❤❤", color=(1,0,0,1), size_hint_y=0.1)
        layout.addWidget(self.lives_label)
        
        self.msg = QLabel(text="¡BUENA SUERTE!", size_hint_y=0.1)
        layout.addWidget(self.msg)

        self.play_music()
        self.next_q()
        return layout

    def update_info(self, dt):
        self.info.text = f"BCN: {datetime.now().strftime('%H:%M:%S')} | 8°C ☀"

    def play_music(self):
        if self.current_sound: self.current_sound.stop()
        track = random.choice(self.playlist)
        self.current_sound = SoundLoader.load(track)
        if self.current_sound:
            self.current_sound.loop = True
            self.current_sound.play()
            self.msg.text = f"PLAYING: {track}"

    def next_q(self):
        self.pais = random.choice(list(PAISES.keys()))
        self.correcta = PAISES[self.pais][0]
        ops = list(PAISES[self.pais]); random.shuffle(ops)
        self.q_label.text = f"¿CAPITAL DE {self.pais.upper()}?"
        for i in range(3): self.btns[i].text = ops[i]

    def check(self, instance):
        if instance.text == self.correcta:
            self.score += 25
            self.score_label.text = f"PTS: {self.score}"
            self.pb.value = min(self.score, 1000)
            self.msg.text = "¡EXCELENTE!"
            self.next_q()
        else:
            self.lives -= 1
            self.lives_label.text = f"VIDAS: {'❤'*self.lives}"
            if self.lives <= 0:
                self.msg.text = "FIN DEL JUEGO"
                self.score, self.lives = 0, 5
                self.score_label.text = "PTS: 0"
                self.lives_label.text = "VIDAS: ❤❤❤❤❤"
            else:
                self.msg.text = f"ERROR, ERA {self.correcta}"
            self.next_q()

if __name__ == '__main__':
    QuizApp().run()