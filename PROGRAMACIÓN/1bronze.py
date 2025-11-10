
import pandas as pd
from datetime import datetime
import os

#1.Empezamos leyendo el archivo dataset

df_bronze = pd.read_csv('DATOS/1CRUDO/mammo_input_extensive_cristina.csv')
print(f"Datos : {df_bronze.shape}")

#2. Eliminamos las filas completamente vacías
print(f"Filas antes de eliminar nulos: {df_bronze.count()}")
df_silver = df_bronze.dropna(how="all")
print(f"Filas despues de eliminar nulos: {df_silver.count()}")

#3.Eliminamos los duplicados
df_silver = df_silver.drop_duplicates()

#4. Corregimos los nulos
df_silver['AnodeFilter'] = df_silver['AnodeFilter'].fillna("DESCONOCIDO")  
df_silver['kVp'].fillna( df_silver['kVp'].median())
df_silver['PatientID'].fillna( df_silver['PatientID'].fillna("DESCONOCIDO"))
df_silver['ExamDate'].fillna( df_silver['ExamDate'].fillna('DESCONOCIDO'))
df_silver['KermaAir_mGy'].fillna( df_silver['KermaAir_mGy'].median())
df_silver['Thickness_cm'].fillna( df_silver['Thickness_cm'].median())
df_silver['Glandular_pct'].fillna( df_silver['Glandular_pct'].median())
df_silver['mAs'].fillna( df_silver['mAs'].median())
df_silver['Compression_N'].fillna( df_silver['Compression_N'].median())
df_silver['Projection'].fillna( df_silver['Projection'].fillna("DESCONOCIDO"))


#5. Valores lógicos

df_silver = df_silver[df_silver["AnodeFilter"].notna()]  # elimina NaN
df_silver = df_silver[df_silver["AnodeFilter"].str.upper() != "DESCONOCIDO"]

def comprobar_rango_kvp(kvp: float):
    if kvp > 20 or kvp <= 40:
        return kvp
    else:
        return None
    
def comprobar_rango_Examdate(examdate):
    if str(examdate) >= "2010-01-01" or str(examdate) <= str(datetime.now().date()):#extrae solo la parte de la fecha y lo convierte en str
            return examdate
    else:
            return None
            
      
def comprobar_rango_Thickness_cm(Thickness_cm: float):
    if Thickness_cm >= 0.1 or Thickness_cm <= 120:
        return Thickness_cm
    else:
        return None
    
      
def comprobar_rango_KermaAir_mGy(KermaAir_mGy: float):
    if KermaAir_mGy >= 0.1 or KermaAir_mGy <= 15:
        return KermaAir_mGy
    else:
        return None
    
    
 
def comprobar_rango_Compression_N(Compression_N: float):
    if Compression_N >= 40 or Compression_N <= 215:
        return Compression_N
    else:
        return None
    
df_silver['kVp'] = df_silver['kVp'].apply(comprobar_rango_kvp)
df_silver['ExamDate'] = df_silver['ExamDate'].apply(comprobar_rango_Examdate)
df_silver['Thickness_cm'] = df_silver['Thickness_cm'].apply(comprobar_rango_Thickness_cm)
df_silver['KermaAir_mGy'] = df_silver['KermaAir_mGy'].apply(comprobar_rango_KermaAir_mGy)
df_silver['Compression_N'] = df_silver['Compression_N'].apply(comprobar_rango_KermaAir_mGy)


print(f"Datos tras limpieza (silver): {df_silver.shape}")
print(df_silver.head())
print(df_silver.info())

#6.Guardamos los resultados
carpeta_bronze = "DATOS/2BRONZE"
os.makedirs(carpeta_bronze, exist_ok=True)

ruta_salida = os.path.join(carpeta_bronze, "mammo_output_limpio.csv")
df_silver.to_csv(ruta_salida, index=False)

print(f"Archivo limpio generado: {ruta_salida}")


