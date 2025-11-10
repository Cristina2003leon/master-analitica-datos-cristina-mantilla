
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#1.Empezamos leyendo el archivo dataset ya limpio, SILVER
df = pd.read_csv("mammo_input_extensive.csv")


print("Columnas encontradas en el archivo:")
print(df.columns.tolist())




#2.Definimos la función que simula el método de cálculo "Dance"
def metodo_dance(row):
    """
    Calcula la dosis glandular media Dg usando el método de Dance.
    Fórmula: Dg = K * g * c * s
    donde:
      - K: kerma en aire incidente (mGy)
      - g: factor de conversión g
      - c: factor por composición tisular
      - s: factor de espectro/anodo-filtro
    """
    #esto de try lo consulté con chatgpt porque sabia que existía pero no me acordaba 
    try:
        kvp = float(row["kVp"])
        espesorescsv = float(row["Thickness_cm"])
        anodo_filtro = str(row["AnodeFilter"])#esta  columna se trata de una palabra
        k = float(row["KermaAir_mGy"])
    except KeyError as i:
        raise KeyError("Falta una columna necesaria en el CSV: {i}")

    #3.Datos teóricos que se pueden encontrar en Internet para este método (g, c, s)
 
    g_valores = {
        #mirar si esto esta bien expresado así
        #argumento de la izq se llama clave
        "Mo/Mo": {25: 0.165, 28: 0.170, 30: 0.175},
        "Mo/Rh": {28: 0.180, 30: 0.185},
        "Rh/Rh": {28: 0.190, 30: 0.195},
        "W/Rh":  {28: 0.200, 30: 0.205},
        "W/Ag":  {28: 0.210, 30: 0.215},
    }

    c_valores = {
        20: 1.02, 30: 1.00, 40: 0.98, 50: 0.96, 60: 0.94
    }

    s_valores = {
        "Mo/Mo": 1.00, "Mo/Rh": 1.02, "Rh/Rh": 1.03, "W/Rh": 1.04, "W/Ag": 1.05
    }

    #4.Realizamos interpolaciones para no limitarnos únicamente a cálculos con los valores aportados
    
    #Calcular el valor aproximado de una magnitud en un intervalo cuando se conocen algunos de los valores que
    #toma a uno y otro lado de dicho intervalo
    def interp(tabla, clave, valor):
    #tabla=conjuntos valores; clave= argumento izq string; 
    #valor= el/los numero/s para el cual/es no tengo info.(por eso interpolo) 
        if clave not in tabla:
            return "no está la clave utilizada"
        
        clavs = list(tabla[clave].keys() ) #para obtener las claves 
        vals = list(tabla[clave].values() )#para obtener los valores
        return np.interp(valor, clavs, vals)

    # g-factor
    g = interp(g_valores, anodo_filtro, kvp)

    # c-factor (según espesor)
    espesoresdec = list(c_valores.keys())#las claves
    c_vals = list(c_valores.values())#los valores de c
    c =np.interp(espesorescsv, espesoresdec, c_vals) 

    # s-factor
    if anodo_filtro in s_valores:
        s = s_valores[anodo_filtro]
    else:
        print("no está la clave utilizada")



    #5.Hacemos el cálculo final
    Dg = k * g * c * s
    return Dg


#6.Aplicamos el método a todo el csv
df["Dg_mGy"] = df.apply(metodo_dance, axis=1)# axis para aplicarlo sobre las filas

#7.Guardamos los resultados
df.to_csv("mammo_output_dance.csv", index=False)# con index false evitamos que guarde el índice
print("Cálculo completado")
print("Archivo guardado: mammo_output_dance.csv")

#8.Mostramos la dosis media
print(f"Dosis glandular media promedio: {df['Dg_mGy'].mean():.3f} mGy")#1º f empleada para insertar los valores en la frase
#2º f empleada para elegir el número de decimales






#9.Realizamos las gráficas, voy a emplear matplotlib

# Activar estilo de Seaborn
sns.set(style="whitegrid")

#Gráfico 1: Dosis vs kVp
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="kVp", y="Dg_mGy", color="blue", alpha=0.7)
plt.title("Dosis glandular vs kVp")
plt.xlabel("kVp")
plt.ylabel("Dosis glandular media (mGy)")
plt.tight_layout()
plt.show()

#Gráfico 2: Dosis vs Espesor de la mama
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Thickness_cm", y="Dg_mGy", color="red", alpha=0.7)
plt.title("Dosis glandular vs Espesor de la mama")
plt.xlabel("Espesor de la mama (cm)")
plt.ylabel("Dosis glandular media (mGy)")
plt.tight_layout()
plt.show()

#Gráfico 3: Dosis media por tipo de ánodo/filtro
plt.figure(figsize=(8, 6))
sns.barplot(
    data=df, 
    x="AnodeFilter", 
    y="Dg_mGy", 
    color="purple", 
    edgecolor="black", 
    estimator="mean",    
)

plt.title("Dosis glandular media para cada tipo de ánodo/filtro")
plt.xlabel("Tipo de ánodo/filtro")
plt.ylabel("Dosis glandular media (mGy)")
plt.tight_layout()
plt.show()
