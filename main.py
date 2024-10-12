import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

######################################
# FUNGSI + DATA + DLL
######################################

# Load dataset
hour_df = pd.read_csv('hour.csv')
# Mengembalikan nilai kolom temp, atemp, hum dan windspeed ke nilai aslinya sebelum dinornalisasi. 
max_temp = 39
min_temp = -8
hour_df['temp'] = hour_df['temp'] * (max_temp - min_temp) + min_temp
t_min = -16
t_max = 50
hour_df['atemp'] = hour_df['atemp'] * (t_max - t_min) + t_min
hour_df['hum'] = hour_df['hum'] * 100
hour_df['windspeed'] = hour_df['windspeed'] * 67
# Membuat interval temperatur menjadi 10 bin
hour_df['bins: temp'] = pd.cut(hour_df['temp'], bins=10)
# Membuat interval temperatur dirasakanmenjadi 10 bin
hour_df['bins: atemp'] = pd.cut(hour_df['atemp'], bins=10)
# Membuat interval kelembaban menjadi 10 bin
hour_df['bins: hum'] = pd.cut(hour_df['hum'], bins=10)
# Membuat interval kecepatan angin menjadi 10 bin
hour_df['bins: windspeed'] = pd.cut(hour_df['windspeed'], bins=10)
# Data tambahan
periode = {'season': 'Musim', 'mnth': 'Bulan', 'hr': 'Jam', 'weekday': 'Hari', 'weathersit': 'Kondisi Cuaca', \
           'bins: temp': 'Temperatur', 'bins: hum': 'Kelembaban', 'bins: windspeed': 'Kecepatan Angin'}
dict_season = {1: 'Dingin', 2: 'Semi', 3: 'Panas', 4: 'Gugur'}
list_season = ['Dingin', 'Semi', 'Panas', 'Gugur']
dict_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'}
list_month = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
dict_hour = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19, \
             20:20, 21:21, 22:22, 23:23 }
list_hour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
dict_week = {0: 'Min', 1: 'Sen', 2: 'Sel', 3: 'Rab', 4: 'Kam', 5: 'Jum', 6: 'Sab'}
list_week = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab']
dict_weather = {1:'Cerah', 2: 'Berkabut/Berawan', 3: 'Hujan/Salju Ringan', 4: 'Hujan Deras/Badai Salju'}
list_weather = ['Cerah', 'Berkabut/Berawan', 'Hujan/Salju Ringan', 'Hujan Deras/Badai Salju']
dict_temp = {}
list_temp = []
dict_hum = {}
list_hum = []
dict_wind = {}
list_wind = []

def tampil_barchart_pertahun(period, label, change_label = 1):
    # Menghitung rata-rata 'cnt' per period dan per tahun
    avg_cnt_per_period_year = hour_df.groupby([period, 'yr'])['cnt'].mean().reset_index()
    
    # Mengubah kolom 'yr' menjadi nama tahun yang lebih jelas
    avg_cnt_per_period_year['yr'] = avg_cnt_per_period_year['yr'].replace({0: '2011', 1: '2012'})
    
    # Membuat bar chart menggunakan seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(ax=ax, x=period, y='cnt', hue='yr', data=avg_cnt_per_period_year)

    if change_label == 1:
        # Mengubah label pada sumbu x
        period_labels = label
        ax.set_xticklabels([period_labels.get(i, 'Unknown') for i in avg_cnt_per_period_year[period].unique()])
    else:
        ax.tick_params(axis='x', rotation=90)
    # Menambahkan judul dan label
    ax.set_title('Rata-rata Penggunaan Sepeda per ' + periode[period] + ' untuk Tahun 2011 dan 2012', fontsize=16)
    ax.set_xlabel(periode[period], fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Penggunaan Sepeda', fontsize=12)

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

def tampil_barchart_total(period, label, change_label = 1):
    # Menghitung rata-rata 'cnt' per season
    avg_cnt_per_period = hour_df.groupby(period)['cnt'].mean().reset_index()
    
    # Menentukan warna untuk setiap batang
    #colors = ['gray'] * len(avg_cnt_per_period)  # Semua batang berwarna abu-abu
    #max_index = avg_cnt_per_period['cnt'].idxmax()  # Indeks nilai maksimum
    #min_index = avg_cnt_per_period['cnt'].idxmin()  # Indeks nilai minimum
    
    # Mengubah warna batang maksimum dan minimum menjadi biru
    #colors[max_index] = 'cyan'
    #colors[min_index] = 'cyan'
    
    # Membuat bar chart menggunakan seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(ax=ax, x=period, y='cnt', data=avg_cnt_per_period) #, palette=colors)
    
    if change_label == 1:
        # Mengubah label pada sumbu x
        period_labels = label
        ax.set_xticklabels([period_labels[i] for i in avg_cnt_per_period[period]], rotation=0)
    else:
        ax.tick_params(axis='x', rotation=90)
    
    # Menambahkan judul dan label
    ax.set_title('Rata-rata Jumlah Pemakaian Berdasarkan ' + periode[period], fontsize=16)
    ax.set_xlabel(periode[period], fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Pemakaian', fontsize=12)
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    
def tampil_boxplot_pertahun(period, label, change_label = 1):
    # Membuat figure untuk boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Membuat boxplot dengan hue berdasarkan tahun (yr)
    sns.boxplot(x=period, y='cnt', hue='yr', data=hour_df, ax=ax)
    
    # Menambahkan judul dan label pada grafik
    ax.set_title('Penggunaan Sepeda per ' + periode[period] + ' untuk Tahun 2011 dan 2012', fontsize=16)
    ax.set_xlabel(periode[period], fontsize=12)
    ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
    
    if change_label == 1:
        # Mengubah label pada sumbu x 
        ax.set_xticklabels(label)
    else:
        ax.tick_params(axis='x', rotation=90)      
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

def tampil_boxplot_total(period, label, change_label = 1):
    # Membuat figure untuk boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Membuat boxplot
    sns.boxplot(x=period, y='cnt', data=hour_df, ax=ax)
    
    # Menambahkan judul dan label pada grafik
    ax.set_title('Penggunaan Sepeda per ' + periode[period], fontsize=16)
    ax.set_xlabel(periode[period], fontsize=12)
    ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
    
    if change_label == 1:
        # Mengubah label pada sumbu x
        ax.set_xticklabels(label)
    else:
        ax.tick_params(axis='x', rotation=90)
      
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    


######################################################
# WEBPAGE
######################################################

# Mengatur konfigurasi halaman
st.set_page_config(
    page_title="Analisis Data Bike Sharing",
    page_icon="🚲",
    layout="wide",  # Mengatur layout menjadi wide (lebih lebar)
    initial_sidebar_state="expanded"  # Menampilkan sidebar dalam kondisi terbuka
)

with st.sidebar:
    # Menambahkan logo
    st.image("logo.jpg")
    with st.expander('About me'):
        # Menggunakan HTML dan CSS untuk membuat kotak teks dengan latar belakang berwarna
        st.markdown(
            """
            <div>
                <p style="font-size: 16px; color: black;">Anggoro Yudho Nuswantoro</p>
                <p style="font-size: 16px; color: black;">Seorang electrical engineer yang bekerja di perusahaan manufaktur serat polyester di daerah Kaliwungu - Jawa Tengah.</p>
                <p style="font-size: 16px; color: black;">yudho.nuswantoro@gmail.com</p>
                <p style="font-size: 16px; color: black;">0811-5211770</p>

            </div>
            """,
            unsafe_allow_html=True
        )
    with st.expander('About this page'):
        # Menggunakan HTML dan CSS untuk membuat kotak teks dengan latar belakang berwarna
        st.markdown(
            """
            <div>
                <p style="font-size: 16px; color: black;">Dashboard ini adalah tugas akhir Pelatihan Belajar Analisis Data dengan Python, sebagai syarat kelulusan pelatihan.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.title('Analisa Bike Sharing Dataset')

st.markdown(
    """
    <div>
        <p style="font-size: 16px; color: black;">Aplikasi ini melakukan analisa terhadap dataset bike sharing. Dataset yang digunakan menunjukkan pemakaian sepeda pada tahun 2011 dan 2012.</p>
    </div>
    """,
    unsafe_allow_html=True
)

##########################
# MUSIM DAN BULAN
##########################
st.header('Pola Pemakaian Sepeda Berdasar Musim dan Bulan')

pembuka_1 = '''\
Analisa pertama yang akan kita lakukan adalah melihat pola pemakaian sepeda per musim dan bulan. Melalui analisa ini \
kita ingin melihat hubungan antara musim dan bulan dengan tingkat pemakaian sepeda. Manfaat dilakukannya analisa ini adalah kita bisa \
merencakanan penyediaan sepeda secara optimal dan rencana perawatan rutin tahunan. ')\
'''
st.write(pembuka_1)

# Membuat select box dengan beberapa opsi
option_1_1 = st.selectbox(
    'Pilihan analisa : ',
    ['Per tahun','Total'],
    key = 'option_1'
)

if option_1_1 == 'Per tahun':
    tab1, tab2 = st.tabs(['Musim', 'Bulan'])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('season', dict_season)
        with col2:
            tampil_boxplot_pertahun('season', list_season)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('mnth', dict_month)
        with col2:
            tampil_boxplot_pertahun('mnth', list_month)
else:
    tab1, tab2 = st.tabs(['Musim', 'Bulan'])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('season', dict_season)
        with col2:
            tampil_boxplot_total('season', list_season)
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('mnth', dict_month)
        with col2:
            tampil_boxplot_total('mnth', list_month)

hasil_analisa_1 = ''' \
Berdasar visualisasi di atas, kita bisa melihat bahwa terdapat hubungan yang erat antara pemakaian sepeda dan musim serta bulan yang sedang berjalan. \
Kita bisa melihat bahwa pemakaian terendah pada musim dingin, yang berlangsung dari akhir Desember sampai dengan akhir Maret, sedangkan pemakaian \
tertinggi di saat musim panas, berlangsung dari akhir Juni sampai dengan akhir September. Di musim semi dan musim gugur, \
pemakaian relatif tinggi, walaupun tidak setinggi di musim panas.

Visualisasi menggunakan boxplot menunjukkan bahwa ada cukup banyak nilai outlier. Hal ini berarti bahwa di musim dingin, saat pemakaian sepeda \
secara rata-rata rendah, ada saat-saat tertentu di mana ada tingkat pemakaian yang tinggi, bahkan melebihi rata-rata pemakaian di musim semi, \
panas dan gugur. 
'''

rekomendasi_1 ='''\
Berdasarkan temuan di atas, ada beberapa hal yang bisa ditindaklanjuti, yaitu:
1. Memfokuskan perawatan rutin tahunan di musim dingin (terutama di bulan Januari dan Februari) agar saat masuk musim semi, sepeda-sepeda yang akan digunakan sudah kembali \
dalam kondisi bagus dan dapat bertahan hingga musim dingin berikutnya.
2. Mengatur penyediaan sepeda di musim dingin agar tidak terlalu banyak sepeda yang _idle_ tak terpakai, namun tetap memastikan bahwa \
tersedia cukup sepeda jika terjadi lonjakan pemakaian.
3. Mengatur penyediaan sepeda di musim semi hingga musim gugur agar selalu tersedia cukup sepeda untuk digunakan para pengguna yang secara rata-rata cukup tinggi.
'''

st.write(hasil_analisa_1)
st.write(rekomendasi_1)

##########################
# JAM DAN HARI
##########################
st.header('Pola Pemakaian Sepeda Berdasar Jam dan Hari')

pembuka_2 = '''\
Analisa berikutnya yang akan kita lakukan adalah melihat pola pemakaian sepeda berdasarkan jam dan hari pemakaian. Melalui analisa ini \
kita ingin melihat hubungan antara jam dan hari pemakaian dengan tingkat pemakaian sepeda. Manfaat dilakukannya analisa ini adalah kita bisa \
merencakanan penyediaan sepeda secara optimal dan rencana perawatan rutin harian dan mingguan. ')\
'''
st.write(pembuka_2)

# Membuat select box dengan beberapa opsi
option_2_1 = st.selectbox(
    'Pilihan analisa : ',
    ['Per tahun','Total'],
    key='option_2'
)

if option_2_1 == 'Per tahun':
    tabJam, tabHari = st.tabs(['Jam', 'Hari'])
    with tabJam:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('hr', dict_hour)
        with col2:
            tampil_boxplot_pertahun('hr', list_hour)
    with tabHari:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('weekday', dict_week)
        with col2:
            tampil_boxplot_pertahun('weekday', list_week)
else:  # TOTAL
    tabJam, tabHari = st.tabs(['Jam', 'Hari'])
    with tabJam:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('hr', dict_hour)
        with col2:
            tampil_boxplot_total('hr', list_hour)
    with tabHari:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('weekday', dict_week)
        with col2:
            tampil_boxplot_total('weekday', list_week)  

hasil_analisa_2 = ''' \
Berdasar visualisasi jam pemakaian sepeda dengan tingkat pemakaian, kita dapat melihat bahwa ada jam tertentu di mana pemakaian sepeda sangat \
rendah, yaitu pada pada tengah malam hingga dini hari (sekitar jam 11 malam sampai dengan jam 6 pagi). Namun pada jam-jam lain, pemakaian rata-rata \
sangat tinggi, yaitu sekitar jam 8 pagi serta jam 5 sore dan 6 sore, yang mana jam-jam tersebut bertepatan dengan aktivitas orang berangkat ke \
tempat kerja di pagi hari dan pulang kembali ke rumah di sore hari. 

Di luar jam tersebut, pemakaian cukup tinggi sepanjang hari sampai malam dan bisa dikatakan bahwa pemakaiannya relatif stabil. 

Berdasarkan visualisasi boxplot penggunaan per jam, kita melihat bahwa variasi jumlah pengguna per jam cukup besar. Pada beberapa kasus, \
pemakaian mencapai hampir 1000 pemakai per jam, nilai yang cukup tinggi dibandingkan nilai median yang berkisar 400 pemakaian per jam. 

Sedangkan tingkat pemakaian per hari dari Minggu sampai dengan Sabtu tidak menunjukkan perbedaan yang mencolok. Bahkan bisa dikatakan bahwa \
tingkat pemakaian relatif stabil sepanjang minggu. 
'''

rekomendasi_2 ='''\
Berdasarkan temuan di atas, kita dapat mempertimbangkan untuk:
1. Menggunakan jam-jam sepi, yaitu tengan malam sampai dengan dini hari, kurang lebih jam 12 malam sampai jam 5 pagi, untuk melakukan \
perawatan dan perbaikan harian atas sepeda-sepeda yang digunakan di hari itu. Hal ini untuk memastikan bahwa sepeda akan terus dalam \
kondisi prima dan dapat dioperasionalkan sepanjang hari. 
2. Menyiapkan distribusi sepeda secara baik untuk menjamin selalu tersedia sepeda bagi para pengguna sepanjang hari sepanjang minggu. \
Jika jaminan ketersediaan sepeda dapat ditingkatkan maka akan akan semakin banyak orang yang tertarik untuk menggunakan sepeda.
'''

st.write(hasil_analisa_2)
st.write(rekomendasi_2)

##########################
# KONDISI CUACA
##########################
st.header('Pola Pemakaian Sepeda Berdasar Kondisi Cuaca')

pembuka_3 = '''\
Di bagian ketiga, kita akan melihat hubungan antara pemakaian sepeda dengan kondisi cuaca dan tiga \
parameter lingkungan, yaitu temperatur, kelembaban dan kecepatan angin. Hubungan antara pemakaian \
sepeda dan berbagai parameter ini akan divisualisasikan sehingga kita dapat mudah mencerna hubungannya.
'''
st.write(pembuka_3)

# Membuat select box dengan beberapa opsi
option_3_1 = st.selectbox(
    'Pilihan analisa : ',
    ['Per tahun','Total'],
    key='option_3'
)

if option_3_1 == 'Per tahun':
    tabCuaca, tabTemp, tabLembab, tabAngin = st.tabs(['Kondisi Cuaca', 'Temperatur', 'Kelembaban', 'Kecepatan Angin'])
    with tabCuaca:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('weathersit', dict_weather)
        with col2:
            tampil_boxplot_pertahun('weathersit', list_weather)
    with tabTemp:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('bins: temp', dict_temp, 0)
        with col2:
            tampil_boxplot_pertahun('bins: temp', list_temp, 0)
    with tabLembab:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('bins: hum', dict_hum, 0)
        with col2:
            tampil_boxplot_pertahun('bins: hum', list_hum, 0)
    with tabAngin:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('bins: windspeed', dict_wind, 0)
        with col2:
            tampil_boxplot_pertahun('bins: windspeed', list_wind, 0)
else:  # TOTAL
    tabCuaca, tabTemp, tabLembab, tabAngin = st.tabs(['Kondisi Cuaca', 'Temperatur', 'Kelembaban', 'Kecepatan Angin'])
    with tabCuaca:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('weathersit', dict_weather)
        with col2:
            tampil_boxplot_total('weathersit', list_weather)
    with tabTemp:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('bins: temp', dict_temp, 0)
        with col2:
            tampil_boxplot_total('bins: temp', list_temp, 0)
    with tabLembab:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('bins: hum', dict_hum, 0)
        with col2:
            tampil_boxplot_total('bins: hum', list_hum, 0)
    with tabAngin:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('bins: windspeed', dict_wind, 0)
        with col2:
            tampil_boxplot_total('bins: windspeed', list_wind, 0)
hasil_analisa_3 = ''' \
Kita dapat melihat bahwa ada korelasi yang cukup kuat antara kondisi cuaca dengan tingkat pemakaian sepeda. \
Pada kondisi cuaca yang cerah, tingkat pemakaian sepeda paling tinggi dibandingkan dengan kondisi cuaca lainnya. \
Tingkat pemakaian terendah ada pada kondisi cuaca hujan deras atau badai salju. Hal ini dapat dengan mudah kita \
pahami, mengingat pada kondisi ini, tentu sedikit sekali orang yang ingin beraktivitas di luar ruangan. 

temperatur udara juga memiliki korelasi yang kuat dengan tingkat pemakaian sepeda. Pada suhu dingin membeku, pemakaian \
sepeda sangat rendah. Sedangkan pada suhu yang cukup hangat, tingkat pemakaian sepeda cukup tinggi. Pada saat suhu udara \
cukup panas, maka tingkat pemakaian akan turun karena pada kondisi ini orang juga akan cenderung menghindari kegiatan \
di luar ruangan.

Berdasarkan tingkat kelembaban udara, maka pemakaian yang cukup tinggi ada pada saat udara agak kering namun tidak sangat \
kering. Pada saat udara sangat kering pemakaian sepeda sangat rendah. Demikian juga pada saat udara sangat basah, tingkat \
pemakaian juga rendah. 

Kecepatan angin tidak terlalu berpengaruh terhadap tingkat pemakaian sepeda walaupun ada kecenderungan pemakaian akan \
meningkat pada kondisi di mana kecepatan angin tidak terlalu rendah dan tidak terlalu tinggi. Namun perbedaan antara rata-rata \
tertinggi dan terendah tidak terlalu jauh bedanya. 
'''

rekomendasi_3 ='''\
Berbeda dibandingkan korelasi dengan musim, bulan serta jam pemakaian, korelasi dengan kondisi cuaca tidak mudah diprediksi \
kapan terjadinya sehingga sulit digunakan untuk merencanakan program pemeliharaan dan penggantian. Namun kondisi ini perlu terus \
dimonitor dan diperkirakan agar kita dapat merencanakan tindak lanjut yang diperlukan jika kondisi cuaca memburuk. 
'''

st.write(hasil_analisa_3)
st.write(rekomendasi_3)


# Menambahkan footer atau caption di bagian bawah aplikasi
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
