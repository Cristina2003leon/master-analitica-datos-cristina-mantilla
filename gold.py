import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#1.Cargar
silver = pd.read_csv("mammo_output_dance.csv")
gold = pd.read_csv("mammo_dataset_con_edad_y_dosis.csv")

#2.
id_paciente = "PatientID"

#3.Juntamos los dos DataFrames usando el ID común
merged = silver[[id_paciente, "Dg_mGy"]].merge(
    gold[[id_paciente, "Dosis_Glandular_mGy"]],
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
