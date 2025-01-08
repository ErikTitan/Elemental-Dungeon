# **Elemental Dungeon - Game Design Document**

Na danom repozitáre sa nachádza implementácia roguelike hry v Pygame, ktorá kombinuje elementárnu mágiu s dynamickým súbojovým systémom a procedurálne generovaným obsahom.

**Autor**: Erik Sháněl

**Vybraná téma**: Four elements (štyri elementy)

---
## **1. Úvod**

**Elemental Dungeon** je roguelike hra s prvkami mágie, kde hráč používa elementárnu mágiu na prežitie v nepriateľskom prostredí dungeonov. Hra kombinuje dynamický súbojový systém založený na elementoch, čím vytvára unikátny herný zážitok pri každom hraní.

### **1.1 Inšpirácia**

Hra čerpá inšpiráciu z nasledujúcich titulov:

<ins>**Vampire Survivors**</ins>

Vampire Survivors prinieslo revolučný systém automatického útočenia a manažmentu veľkého množstva nepriateľov. Môj projekt preberá koncept prežitia proti masívnym vlnám nepriateľov a systém postupného vylepšovania schopností.

<p align="center">
  <img src="" alt="Vampire Survivors">
  <br>
  <em>Obrázok 1 Ukážka hry Vampire Survivors</em>
</p>

<ins>**The Binding of Isaac**</ins>

The Binding of Isaac predstavuje inšpiráciu pre náš dungeonový dizajn a systém postupu hrou. Preberám koncept procedurálne generovaných miestností a rôznorodých nepriateľov s unikátnymi vzorcami správania.

<p align="center">
  <img src="" alt="The Binding of Isaac">
  <br>
  <em>Obrázok 2 Ukážka hry The Binding of Isaac</em>
</p>

<ins>**Shattered Pixel Dungeon**</ins>

Z tejto hry čerpáme inšpiráciu pre pixel art štýl a roguelike mechaniky. Hra ma inšpirovala svojim jednoduchým, ale efektívnym vizuálnym štýlom a systémom elementárnych interakcií.

<p align="center">
  <img src="" alt="Shattered Pixel Dungeon">
  <br>
  <em>Obrázok 3 Ukážka hry Shattered Pixel Dungeon</em>
</p>

### **1.2 Základný koncept**

Hráč ovláda mága, ktorý musí prežiť v dungeone stanovený časový limit, pričom sa bráni proti vlnám nepriateľov pomocou štyroch elementárnych typov mágie. Každý nepriateľ má svoj vlastný element, voči ktorému je zraniteľný špecifickým protikladným elementom.

## **2. Herný dizajn**

### **2.1 Herný štýl**

- **Žaner:** Akčná roguelike
- **Perspektíva:** 2D top-down
- **Herný cieľ:** Prežiť stanovený časový interval (napr. 60 sekúnd) a čeliť narastajúcej vlne nepriateľov.

### **2.2 Základné mechaniky**

1. **Pohyb:** Hrač sa voľne pohybuje po mape pomocou kláves WASD.
2. **Boj:** Hrač vystreľuje elementálne strely na nepriateľov.
3. **Elementárna stratégia:**
   - Hrač môže prepínať medzi štyrmi typmi elementálnych útokov: oheň, voda, zem a vzduch.
   - Každý typ elementu je efektívny proti jednému z iných (napr. oheň je efektívny proti vode).
4. **Nepriatelia:**
   - Nepriatelia sú generovaní v pravidelných intervaloch na náhodných miestach mapy.
   - Pohyb nepriateľov je zameraný na prenasledovanie hrača.
5. **Zdravie:** Hrač má obmedzený počet životov, ktoré stratí po zásahu nepriateľa.

### **2.3 Interpretácia elementárneho systému**
Hra je postavená na súbojovom systéme štyroch elementov, kde každý element má svoj protiklad:
- **Oheň** > **Voda**
- **Voda** > **Oheň**
- **Zem** > **Vzduch**
- **Vzduch** > **Zem**

Správny výber elementu je kľúčový pre efektívne eliminovanie nepriateľov.

### **2.4 Projektily**
- Každý element má unikátnu vizuálnu reprezentáciu
- Projektily sa pohybujú v smere kliknutia myši
- Cooldown medzi strieľaním bráni spam útokom

### **2.5 Systém zdravia**
- Hráč začína s 3 životmi
- Dočasná nezraniteľnosť po zásahu
- Knockback efekt pri zásahu
- Vizuálna indikácia poškodenia

## **2.6 Herný zážitok**
- **Začiatok hry:** Hra začína obrazovkou s inštrukciami a tlačidlom na spustenie.
- **Intenzita:** Počet nepriateľov narastá s postupujúcim časom.
- **Game Over:** Po strate všetkých životov hra končí, na obrazovke sa zobrazuje možnosť reštartovať alebo ukončiť hru.

### **2.7 Návrh tried**
- **Game**: Hlavná herná slučka, správa herných stavov a obrazoviek
- **Player**: Logika pohybu hráča, zdravia a útokov
- **Projectile**: Systém projektilov a ich elementárnych vlastností
- **Enemy**: Správanie nepriateľov a ich interakcia s hráčom

## **3. Grafika**

### **3.1 Interpretácia štýlu elementov**
Hra využíva pixel art štýl s dôrazom na jasné vizuálne odlíšenie elementov. Každý element má svoju charakteristickú farbu a animácie:

- **Oheň**: Červeno-oranžové projektily s efektom plameňov
- **Voda**: Modré projektily s efektom kvapiek
- **Zem**: Hnedé projektily s efektom kameňov
- **Vzduch**: Biele projektily s efektom vírenia

<p align="center">
  <img src="" alt="Projektily">
  <br>
  <em>Obrázok 5 Ukážka vodného elementu</em>
</p>

### **3.2 Dizajn**
Hra používa 16x16 pixel art assety škálované na 64x64 pre lepšiu viditeľnosť. Mapa je navrhnutá v dungeon štýle s rôznymi typmi prekážok a dekorácií:

- Pevné steny tvoriace hranice mapy
- Interaktívne prekážky poskytujúce strategické možnosti
- Dekoratívne prvky pre atmosféru dungeonu

<p align="center">
  <img src="" alt="Dungeon">
  <br>
  <em>Obrázok 6 Ukážka hernej mapy</em>
</p>

### **3.2 Užívateľské rozhranie**

- Zdravotný bar
- Indikátor aktuálneho elementu
- Časovač pre zostávajúci čas
- Štartovacia a konečná obrazovka

<p align="center">
  <img src="" alt="HUD">
  <br>
  <em>Obrázok 7 Ukážka HUD</em>
</p>

## **4. Zvuk**

### **4.1 Hudba**
Hra obsahuje atmosférickú dungeon hudbu, ktorá dotvára fantasy prostredie. Hudba je dynamicky prispôsobená hernej situácii:

- Atmosférická dungeon hudba
- Prispôsobená hlasitosť pre lepší herný zážitok

### **4.2 Zvuky**
Každý element má svoje charakteristické zvukové efekty:

- Zvuky výstrelov projektilov podľa elementu
- Zvuky zranenia hráča

## **5 Technológie**

- **Engine**: Pygame
- **Jazyk**: Python
- **Rozlíšenie**: Fullscreen
- **Framerate**: 60 FPS

### **5.1 Požiadavky na systém**

- **Minimálne:**
  - OS: Windows/Linux/MacOS
  - Python 3.10+ s knižnicou Pygame
- **Odporúčané:**
  - Procesor s minimálnym taktom 2.5 GHz
  - 4GB RAM
  - Grafická karta s podporou OpenGL 3.0

## **6. Možné budúce vylepšenia**

- Pridanie boss nepriateľov
- Systém levelovania a skill tree
- Nové typy projektilov
- Kolekcia predmetov a power-upov
- Achievementy a štatistiky
- Multiplayer mód

## **7. Inštalácia a spustenie**

Spustenie pomocou .exe súboru v direktórii `build/` alebo:

1. Nainštalujte Python 3.x
2. Nainštalujte Pygame: `pip install pygame`
3. Stiahnite repository
4. Spustite main.py
