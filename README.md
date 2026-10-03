# Erkam-inci-BOZ213d01u01

A Dota-inspired jungle farming simulator using Q-learning to learn and visualize efficient farming routes.

## Language

[English](#english) | [Türkçe](#türkçe)

---

# English

## Dota Farming RL

A simple Dota-inspired jungle farming simulator built with Python and Tkinter.

The project uses **Q-learning** to learn jungle farming routes and compares the learned strategy with a simple **nearest-camp heuristic**.

The goal is to experiment with reinforcement learning, route selection, and game AI in a small visual environment.

## Features

- Dota-inspired jungle farming simulation
- Tabular Q-learning agent
- Nearest-camp baseline strategy
- Adjustable hero damage
- Small, Medium, Large, and Ancient camps
- Camp respawn system
- Travel and combat time simulation
- Real-time Tkinter visualization
- Background AI training
- Training progress display
- Gold, camps cleared, GPM, time, and target statistics

## How It Works

The map contains 28 simplified jungle camps.

Each camp has:

- A position
- A camp type
- A health value
- A respawn timer

The hero moves between camps, clears them, and receives **100 gold** for each completed camp.

Combat duration depends on the hero's damage and the camp's health.

The simulation lasts **300 simulated seconds**.

## Q-Learning

The AI uses tabular Q-learning.

The state is represented as:

```text
(
    last_camp,
    time_bucket,
    available_camps_mask
)
```

Where:

- `last_camp` is the previously cleared camp
- `time_bucket` represents the current simulation time
- `available_camps_mask` represents which camps are currently available

The action is simply:

```text
Choose the next jungle camp.
```

The agent receives a reward when it successfully clears a camp.

The Q-learning update is:

```text
Q(s, a) ← Q(s, a) + α [r + γ max Q(s', a') - Q(s, a)]
```

The default parameters are:

```python
EPISODES = 12000
ALPHA = 0.15
GAMMA = 0.98

EPS_START = 1.0
EPS_MIN = 0.05
EPS_DECAY = 0.9995
```

An epsilon-greedy strategy is used during training so that the agent gradually moves from exploration toward learned decisions.

## Decision Modes

### Nearest Camp

The baseline strategy always selects the closest currently available camp.

### Learned AI

The Q-learning agent selects the next camp according to its learned Q-values.

The AI is trained for the currently selected hero damage.

If the damage value is changed, the AI must be trained again.

## Running the Project

Clone the repository:

```bash
git clone https://github.com/radagaserkam/Erkam-inci-BOZ213d01u01.git
cd Erkam-inci-BOZ213d01u01
```

Run the program:

```bash
python "dota 2 AI train.py"
```

or:

```bash
python3 "dota 2 AI train.py"
```

## Requirements

- Python 3
- Tkinter

No machine learning libraries such as TensorFlow or PyTorch are required.

The reinforcement learning algorithm is implemented directly in Python.

> On some Linux distributions, Tkinter may need to be installed separately.

## Usage

1. Start the program.
2. Select the hero damage.
3. Use **Nearest Camp** to run the baseline strategy.
4. Click **Train AI**.
5. Wait for the Q-learning training to finish.
6. Select **Learned AI**.
7. Reset and start the simulation.
8. Compare the resulting route and GPM.

## Simplifications

This is not intended to reproduce Dota gameplay accurately.

The simulator does not include mechanics such as:

- Real map geometry
- Trees and cliffs
- Pathfinding
- Vision
- Neutral creep abilities
- Camp stacking
- Pulling
- Hero abilities
- Real combat mechanics

Movement between camps is calculated using straight-line distance.

The project is primarily an experiment in **reinforcement learning and route optimization**.

## Possible Improvements

Future additions could include:

- More accurate map geometry
- Pathfinding
- Different rewards for different camp types
- Saving and loading trained Q-tables
- Training performance graphs
- Camp stacking
- Multiple heroes
- More realistic combat
- Comparison with other reinforcement learning algorithms

## Disclaimer

This is an unofficial educational project inspired by Dota-style jungle farming mechanics.

Dota and related names are the property of their respective owners.

This project is not affiliated with or endorsed by Valve Corporation.

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

See the `LICENSE` file for details.

---

# Türkçe

## Dota Farming RL

Python ve Tkinter kullanılarak geliştirilmiş, Dota'dan esinlenen basit bir jungle farming simülatörüdür.

Proje, jungle farming rotalarını öğrenmek için **Q-learning** kullanır ve öğrenilmiş stratejiyi basit bir **en yakın kamp sezgiseli** ile karşılaştırır.

Projenin amacı; reinforcement learning, rota seçimi ve oyun yapay zekâsı konularını küçük ve görsel bir simülasyon ortamında deneyimlemektir.

## Özellikler

- Dota'dan esinlenen jungle farming simülasyonu
- Tabular Q-learning ajanı
- En yakın kamp tabanlı temel strateji
- Ayarlanabilir kahraman hasarı
- Small, Medium, Large ve Ancient kampları
- Kamp yeniden doğma sistemi
- Hareket ve savaş süresi simülasyonu
- Tkinter ile gerçek zamanlı görselleştirme
- Arka planda AI eğitimi
- Eğitim ilerleme göstergesi
- Altın, temizlenen kamp, GPM, süre ve hedef istatistikleri

## Nasıl Çalışır?

Harita, basitleştirilmiş **28 jungle kampından** oluşur.

Her kampın:

- Bir konumu
- Bir kamp türü
- Bir can değeri
- Bir yeniden doğma süresi

vardır.

Kahraman kamplar arasında hareket eder, kampları temizler ve tamamladığı her kamp için **100 gold** kazanır.

Savaş süresi, kahramanın hasarına ve kampın can değerine bağlıdır.

Simülasyon toplam **300 simülasyon saniyesi** sürer.

## Q-Learning

Yapay zekâ, tabular Q-learning kullanır.

State şu şekilde temsil edilir:

```text
(
    last_camp,
    time_bucket,
    available_camps_mask
)
```

Burada:

- `last_camp`, son temizlenen kampı temsil eder.
- `time_bucket`, mevcut simülasyon zamanını temsil eder.
- `available_camps_mask`, hangi kampların şu anda kullanılabilir olduğunu temsil eder.

Aksiyon ise basitçe:

```text
Bir sonraki jungle kampını seç.
```

Ajan, bir kampı başarıyla temizlediğinde ödül alır.

Q-learning güncelleme formülü:

```text
Q(s, a) ← Q(s, a) + α [r + γ max Q(s', a') - Q(s, a)]
```

Varsayılan parametreler:

```python
EPISODES = 12000
ALPHA = 0.15
GAMMA = 0.98

EPS_START = 1.0
EPS_MIN = 0.05
EPS_DECAY = 0.9995
```

Eğitim sırasında epsilon-greedy stratejisi kullanılır.

Bu sayede ajan başlangıçta farklı rotaları keşfeder ve eğitim ilerledikçe öğrendiği kararları daha fazla kullanmaya başlar.

## Karar Modları

### Nearest Camp

Temel strateji, her zaman o anda kullanılabilir olan en yakın kampı seçer.

### Learned AI

Q-learning ajanı, eğitim sırasında öğrendiği Q değerlerine göre bir sonraki kampı seçer.

AI, seçili kahraman hasar değerine göre eğitilir.

Hasar değeri değiştirilirse AI'ın yeniden eğitilmesi gerekir.

## Projeyi Çalıştırma

Repository'yi klonlayın:

```bash
git clone https://github.com/radagaserkam/Erkam-inci-BOZ213d01u01.git
cd Erkam-inci-BOZ213d01u01
```

Programı çalıştırın:

```bash
python "dota 2 AI train.py"
```

veya:

```bash
python3 "dota 2 AI train.py"
```

## Gereksinimler

- Python 3
- Tkinter

TensorFlow veya PyTorch gibi herhangi bir machine learning kütüphanesi gerekli değildir.

Reinforcement learning algoritması doğrudan Python ile uygulanmıştır.

> Bazı Linux dağıtımlarında Tkinter'ın ayrıca kurulması gerekebilir.

## Kullanım

1. Programı başlatın.
2. Kahramanın hasar değerini seçin.
3. Temel stratejiyi görmek için **Nearest Camp** modunu çalıştırın.
4. **Train AI** butonuna basın.
5. Q-learning eğitiminin tamamlanmasını bekleyin.
6. **Learned AI** modunu seçin.
7. Simülasyonu sıfırlayıp yeniden başlatın.
8. Oluşan rotayı ve GPM değerini karşılaştırın.

## Basitleştirmeler

Bu proje gerçek Dota oynanışını birebir simüle etmeyi amaçlamaz.

Simülatörde aşağıdaki mekanikler bulunmaz:

- Gerçek harita geometrisi
- Ağaçlar ve uçurumlar
- Pathfinding
- Görüş sistemi
- Neutral creep yetenekleri
- Camp stacking
- Pulling
- Kahraman yetenekleri
- Gerçek Dota savaş mekanikleri

Kamplar arasındaki hareket, düz çizgi mesafesi kullanılarak hesaplanır.

Projenin temel amacı **reinforcement learning ve rota optimizasyonu** üzerine deney yapmaktır.

## Gelecekte Eklenebilecekler

Projeye ileride şu özellikler eklenebilir:

- Daha doğru harita geometrisi
- Pathfinding
- Farklı kamp türleri için farklı ödüller
- Eğitilmiş Q-table'ları kaydetme ve yükleme
- Eğitim performans grafikleri
- Camp stacking
- Birden fazla kahraman
- Daha gerçekçi savaş sistemi
- Farklı reinforcement learning algoritmalarıyla karşılaştırma

## Yasal Uyarı

Bu proje, Dota tarzı jungle farming mekaniklerinden esinlenmiş bağımsız ve eğitim amaçlı bir projedir.

Dota ve ilişkili isimler ilgili hak sahiplerine aittir.

Bu proje Valve Corporation ile bağlantılı değildir ve Valve Corporation tarafından desteklenmemektedir.

## Lisans

Bu proje **GNU General Public License v3.0 (GPL-3.0)** altında lisanslanmıştır.

Detaylar için `LICENSE` dosyasına bakınız.
