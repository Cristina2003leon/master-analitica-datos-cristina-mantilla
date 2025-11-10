import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#1.Cargar
silver = pd.read_csv('DATOS/3SILVER/mammo_output__dance.csv')
gold = pd.read_csv('DATOS/1CRUDO/mammo_dataset_con_edad_y_dosis.csv')

#2.
id_paciente = "PatientID"

#3.Juntamos los dos DataFrames usando el ID común
merged = silver[[id_paciente, "Dg_mGy"]].merge(
    gold[[id_paciente,"Dosis_Glandular_mGy"]],
    on=id_paciente,
    how="inner"   # inner mantiene solo IDs presentes en ambos
)

#4. Renombramos
merged.rename(columns={
    "Dg_mGy": "Dosis_Silver_mGy",
    "Dosis_Glandular_mGy": "Dosis_Gold_mGy"
}, inplace=True)

#5.Creamos un gráfico comparativo
plt.figure(figsize=(8, 6))
sns.scatterplot(data=merged, x="Dosis_Silver_mGy", y="Dosis_Gold_mGy", alpha=0.6, color="teal")
plt.title("Comparación de Dosis Glandular: Silver vs Gold", fontsize=14)
plt.xlabel("Dosis Glandular Silver (mGy)")
plt.ylabel("Dosis Glandular Gold (mGy)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


ruta_salida = "DATOS/4GOLD/mammocalculadoteorico.csv"

# Crear carpeta si no existe
parent = os.path.dirname(ruta_salida)  # esto obtiene DATOS/4GOLD/mammocalculado
if not os.path.exists(parent):
    os.makedirs(parent)

# Guardar archivo
merged.to_csv(ruta_salida, index=False)
print(f"Archivo guardado en: {ruta_salida}")

