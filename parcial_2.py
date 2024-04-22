from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Cargar los datos desde el archivo Excel
df = pd.read_excel('API_SH.IMM.MEAS_DS2_en_excel_v2_50281.xls', sheet_name='Data', header=3, index_col=[0, 1, 2, 3])

@app.route('/')
def index():
    # Renderizar el archivo HTML
    return render_template('index.html')

@app.route('/todos_los_datos')
def obtener_todos_los_datos():
    # Obtener las columnas de los años y los valores
    columnas_anios = df.columns[4:25]  # Columnas de los años desde E4 hasta BP4
    columnas_valores = df.columns[24:]  # Columnas de los valores desde Y4 hasta el final

    # Convertir los datos a un formato JSON
    datos_json = []
    for idx, fila in df.iterrows():
        for anio, valor in zip(columnas_anios, fila[columnas_valores]):
            # Convertir NaN a None para manejarlos en JavaScript
            if pd.isna(valor):
                valor = None
            datos_json.append({
                'Pais': idx[0],
                'Codigo_Pais': idx[1],
                'Nombre_Indicador': idx[2],
                'Codigo_Indicador': idx[3],
                'Anio': anio,
                'Valor': valor
            })

    return jsonify(datos_json)

if __name__ == '__main__':
    app.run(debug=True)
