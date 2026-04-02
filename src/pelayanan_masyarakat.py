# imprt library
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd

# Menyiapkan Variabel Fuzzy
kejelasan_informasi = ctrl.Antecedent(np.arange(0,101), 'kejelasan_informasi')
kejelasan_persyaratan = ctrl.Antecedent(np.arange(0,101), 'kejelasan_persyaratan')
kemampuan_petugas = ctrl.Antecedent(np.arange(0,101), 'kemampuan_petugas')
ketersediaan_sarpras = ctrl.Antecedent(np.arange(0,101), 'ketersediaan_sarpras')
kepuasan_pelayanan = ctrl.Consequent(np.arange(0,401), 'kepuasan_pelayanan')

# Himpunan Fuzzyy Kejelasan Informasi
kejelasan_informasi['Tidak Memuaskan'] = fuzz.trapmf(kejelasan_informasi.universe, [0,0,60,75])
kejelasan_informasi['Cukup Memuaskan'] = fuzz.trimf(kejelasan_informasi.universe, [60,75,90])
kejelasan_informasi['Memuaskan'] = fuzz.trapmf(kejelasan_informasi.universe, [75,90,100,100])

# Himpunan Fuzzy Kejelasan Persyaratan
kejelasan_persyaratan['Tidak Memuaskan'] = fuzz.trapmf(kejelasan_persyaratan.universe, [0,0,60,75])
kejelasan_persyaratan['Cukup Memuaskan'] = fuzz.trimf(kejelasan_persyaratan.universe, [60,75,90])
kejelasan_persyaratan['Memuaskan'] = fuzz.trapmf(kejelasan_persyaratan.universe, [75,90,100,100])

# Himpunan Fuzzy Kemampuan Petugas
kemampuan_petugas['Tidak Memuaskan'] = fuzz.trapmf(kemampuan_petugas.universe, [0,0,60,75])
kemampuan_petugas['Cukup Memuaskan'] = fuzz.trimf(kemampuan_petugas.universe, [60,75,90])
kemampuan_petugas['Memuaskan'] = fuzz.trapmf(kemampuan_petugas.universe, [75,90,100,100])

# Himpunan Fuzzy Ketersedian Sarpras
ketersediaan_sarpras['Tidak Memuaskan'] = fuzz.trapmf(ketersediaan_sarpras.universe, [0,0,60,75])
ketersediaan_sarpras['Cukup Memuaskan'] = fuzz.trimf(ketersediaan_sarpras.universe, [60,75,90])
ketersediaan_sarpras['Memuaskan'] = fuzz.trapmf(ketersediaan_sarpras.universe, [75,90,100,100])

# Himpunan Fuzzy Kepuasan Pelayanan
kepuasan_pelayanan['Tidak Memuaskan'] = fuzz.trapmf(kepuasan_pelayanan.universe, [0,0,50,75])
kepuasan_pelayanan['Kurang Memuaskan'] = fuzz.trapmf(kepuasan_pelayanan.universe, [50,75,100,150])
kepuasan_pelayanan['Cukup Memuaskan'] = fuzz.trapmf(kepuasan_pelayanan.universe, [100,150,250,275])
kepuasan_pelayanan['Memuaskan'] = fuzz.trapmf(kepuasan_pelayanan.universe, [250,275,325,350])
kepuasan_pelayanan['Sangat Memuaskan'] = fuzz.trapmf(kepuasan_pelayanan.universe, [325,350,400,400])

kejelasan_informasi.view()
kejelasan_persyaratan.view()
kemampuan_petugas.view()
ketersediaan_sarpras.view()
kepuasan_pelayanan.view()
input("Whatever You Want...")

# Import dan Extract Rule
df = pd.read_excel('src/81_fuzzy_rules.xlsx')
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

variabel_fuzzy_dict = {
    'Kejelasan Informasi': kejelasan_informasi,
    'Kejelasan Persyaratan': kejelasan_persyaratan,
    'Kemampuan Petugas': kemampuan_petugas,
    'Ketersediaan Sarpras': ketersediaan_sarpras,
    'Kepuasan Pelayanan': kepuasan_pelayanan
}

rules_list = []

for index, row in df.iterrows():
    antecedent = (
        variabel_fuzzy_dict['Kejelasan Informasi'][row['Kejelasan Informasi']] &
        variabel_fuzzy_dict['Kejelasan Persyaratan'][row['Kejelasan Persyaratan']] &
        variabel_fuzzy_dict['Kemampuan Petugas'][row['Kemampuan Petugas']] &
        variabel_fuzzy_dict['Ketersediaan Sarpras'][row['Ketersediaan Sarpras']]
    )

    consequent = variabel_fuzzy_dict['Kepuasan Pelayanan'][row['Kepuasan Pelayanan']]

    # print(f"{antecedent}, {consequent}")
    rule = ctrl.Rule(antecedent, consequent)
    rules_list.append(rule)


# Inference Engine dan Sistem Fuzzy
engine = ctrl.ControlSystem(rules_list)
system = ctrl.ControlSystemSimulation(engine)

# Pengujian
system.input['kejelasan_informasi'] = 80
system.input['kejelasan_persyaratan'] = 60
system.input['kemampuan_petugas'] = 50
system.input['ketersediaan_sarpras'] = 90
system.compute()
print(system.output['kepuasan_pelayanan'])
kepuasan_pelayanan.view(sim=system)
input("ENTER")