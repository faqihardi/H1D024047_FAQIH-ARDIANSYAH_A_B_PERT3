# imprt library
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Menyiapkan Variabel Fuzzy
barang_terjual = ctrl.Antecedent(np.arange(0,101), 'barang_terjual')
permintaan = ctrl.Antecedent(np.arange(0,301), 'permintaan')
harga_per_item = ctrl.Antecedent(np.arange(0,100001), 'harga_per_item')
profit = ctrl.Antecedent(np.arange(0,4000001), 'profit')
stok_makanan = ctrl.Consequent(np.arange(0,1001), 'stok_makanan')

# Himpunan Fuzzy Barang Terjual
# barang_terjual['Rendah'] = fuzz.trapmf(barang_terjual.universe, [0,0,0,40])
barang_terjual['Rendah'] = fuzz.trimf(barang_terjual.universe, [0,0,40])
barang_terjual['Sedang'] = fuzz.trimf(barang_terjual.universe, [30,50,70])
# barang_terjual['Tinggi'] = fuzz.trapmf(barang_terjual.universe, [60,100,100,100])
barang_terjual['Tinggi'] = fuzz.trimf(barang_terjual.universe, [60,100,100])

# Himpunan Fuzzy Permintaan
permintaan['Rendah'] = fuzz.trimf(permintaan.universe, [0,0,100])
permintaan['Sedang'] = fuzz.trimf(permintaan.universe, [50,150,250])
permintaan['Tinggi'] = fuzz.trimf(permintaan.universe, [200,300,300])
# permintaan['Tinggi'] = fuzz.trapmf(permintaan.universe, [200,300,300,300])

# Himpunan Fuzzy Harga per Item
harga_per_item['Murah'] = fuzz.trimf(harga_per_item.universe, [0,0,40000])
harga_per_item['Sedang'] = fuzz.trimf(harga_per_item.universe, [30000,50000,80000])
harga_per_item['Mahal'] = fuzz.trimf(harga_per_item.universe, [60000,100000,100000])

# Himpunan Fuzzy Profit
profit['Rendah'] = fuzz.trimf(profit.universe, [0,0,1000000])
profit['Sedang'] = fuzz.trimf(profit.universe, [1000000,2000000,2500000])
profit['Banyak'] = fuzz.trapmf(profit.universe, [1500000,2500000,4000000,4000000])

# Himpunan Fuzzy Stok Makanan
stok_makanan['Sedang'] = fuzz.trimf(stok_makanan.universe, [100,500,900])
stok_makanan['Banyak'] = fuzz.trimf(stok_makanan.universe, [600,1000,1000])

# Rule-base
rule1 = ctrl.Rule(barang_terjual['Tinggi'] & permintaan['Tinggi'] & harga_per_item['Murah'] & profit['Banyak'], stok_makanan['Banyak'])
rule2 = ctrl.Rule(barang_terjual['Tinggi'] & permintaan['Tinggi'] & harga_per_item['Murah'] & profit['Sedang'], stok_makanan['Sedang'])
rule3 = ctrl.Rule(barang_terjual['Tinggi'] & permintaan['Sedang'] & harga_per_item['Murah'] & profit['Sedang'], stok_makanan['Sedang'])
rule4 = ctrl.Rule(barang_terjual['Sedang'] & permintaan['Tinggi'] & harga_per_item['Murah'] & profit['Sedang'], stok_makanan['Sedang'])
rule5 = ctrl.Rule(barang_terjual['Sedang'] & permintaan['Tinggi'] & harga_per_item['Murah'] & profit['Banyak'], stok_makanan['Banyak'])
rule6 = ctrl.Rule(barang_terjual['Rendah'] & permintaan['Rendah'] &harga_per_item['Sedang'] & profit['Sedang'], stok_makanan['Sedang'])


# barang_terjual.view()
# permintaan.view()
# harga_per_item.view()
# profit.view()
# stok_makanan.view()

# Inference Engine dan Sistem fuzzy
engine = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6])
system = ctrl.ControlSystemSimulation(engine)

# Pengujian
system.input['barang_terjual'] = 80
system.input['permintaan'] = 255
system.input['harga_per_item'] = 25000
system.input['profit'] = 3500000
system.compute()
print(system.output['stok_makanan'])
stok_makanan.view(sim=system)
input("Tekan ENTER untuk melanjutkan")