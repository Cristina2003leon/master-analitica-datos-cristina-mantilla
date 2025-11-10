import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#1.Cargamos los CSV necesarios
silver = pd.read_csv('DATOS/3SILVER/mammo_output__dance.csv')
gold = pd.read_csv('DATOS/1CRUDO/mammo_dataset_con_edad_y_dosis.csv')

#2.Identificamos el ID
id_paciente = "PatientID"

#3.Juntamos los dos DataFrames usando el ID común
#Merge combina ambos DataFrames por la columna id_paciente
merged = silver[[id_paciente, "Dg_mGy"]].merge(
    gold[[id_paciente,"Dosis_Glandular_mGy"]],
    on=id_paciente,
    how="inner"   # inner mantiene solo IDs presentes en ambos
)

#4. Renombramos
merged.rename(columns={
    "Dg_mGy": "Dosis_Silver_mGy",
    "Dosis_Glandular_mGy": "Dosis_Gold_mGy"
}, inplace=True) # La modificación se hace directamente sobre el DataFrame merged.

#5.Creamos un gráfico comparativo
plt.figure(figsize=(8, 6))
sns.scatterplot(data=merged, x="Dosis_Silver_mGy", y="Dosis_Gold_mGy", alpha=0.6, color="blue")
plt.title("Comparación de dosis glandular: Silver vs Gold", fontsize=14)
plt.xlabel("Dosis glandular Silver (mGy)")
plt.ylabel("Dosis glandular Gold (mGy)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()



#7.Guardamos los resultados
carpeta_gold= "DATOS/4GOLD"
os.makedirs(carpeta_gold, exist_ok=True)

ruta_salida = os.path.join(carpeta_gold, "mammocalculadoteorico.csv")#une de manera segura la carpeta con el nombre del archivo.
merged.to_csv(ruta_salida, index=False)#con index false evitamos que guarde el índice
print("Cálculo completado")
print(f"Archivo calculado generado: {ruta_salida}")

