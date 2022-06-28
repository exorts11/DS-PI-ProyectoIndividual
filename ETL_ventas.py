# %% [markdown]
# Carga de archivos

# %%
import pandas as pd
import io
import os
import numpy as np
import copy as copy
from fuzzywuzzy import fuzz

# %%
# Ruta de los archivos
ruta = "./Datasets/"

# %%
def ls(ruta = "./Datasets"):
    return [arch.name for arch in os.scandir(ruta) if arch.is_file()]

# %%
# Archivos de origen predeterminados
origin = np.array(['Clientes.csv',
 'Compra.csv',
 'Gasto.csv',
 'Localidades.csv',
 'Proveedores.csv',
 'Sucursales.csv',
 'TiposDeGasto.csv',
 'Venta.csv'])
codificacion = np.array(['utf-8','utf-8','utf-8','utf-8','ANSI','utf-8','utf-8','utf-8'])


# %%
# Leer los archivos que existen en el directorio
archivos = np.array(ls())

# %%
# Comprobar que archivos existen
csv_existentes = np.array([False, False, False, False, False, False, False, False])
excel_existe = False

s = ''
for word in archivos:
    s += word

idx = 0
for frame_origin in origin :
    if frame_origin in s:
        csv_existentes[idx] = True
    idx+=1

# Comprobacion del excel
if 'CanalDeVenta.xlsx' in s:
    excel_existe = True

print(csv_existentes)

# %%
data = list(range(0,8))

# %%
# Cargamos las tablas csv en una lista
u = 0
for i in origin:
    if csv_existentes[u]:
        r = ruta+i
        g = open(r,encoding=codificacion[u])
        n = 1
        for i in g:
            #print(i)
            if ',' in i:
                #print('Delimiter coma')
                data[u] = (pd.read_csv(r,encoding=codificacion[u]))
            else:
                #print('delimiter punto y coma')
                data[u] = (pd.read_csv(r,delimiter=';',encoding=codificacion[u]))
            break
        #print(u,r)
        g.close()
    u+=1

print(archivos)


# %%
archivos = copy.copy(origin[csv_existentes == True])

# %%
# Actualizamos la variable archivos

# Cargamos el excel, si existe
if excel_existe:
    data.append(pd.read_excel(ruta+'CanalDeVenta.xlsx'))
    archivos = np.append(archivos,['CanalDeVenta.xls'])
print(archivos)

# %%
data[-1]

# %% [markdown]
# Homogenizar el nombre de los campos ID de cada tabla

# %%
for idx, table in enumerate(data):
    name = 'ID_'+archivos[idx][:-4]
    data[idx].rename(columns={table.columns[0] : name}, inplace=True)

# %% [markdown]
# Homogenizar el nombre de los campos de latitud y longitud

# %%
data[0].rename(columns={data[0].columns[-3] : 'Longitud',data[0].columns[-2] : 'Latitud'}, inplace=True)
data[3].rename(columns={data[3].columns[2] : 'Longitud',data[3].columns[1] : 'Latitud'}, inplace=True)
data[-4].rename(columns={data[-4].columns[6] : 'Longitud',data[-4].columns[5] : 'Latitud'}, inplace=True)

# %% [markdown]
# Convertir las columnas de latitud y longitud a float

# %%
tablas = [0,3,-4]
campos = ['Longitud','Latitud']
for df in tablas:
    for col in campos:
        #df.Y = df.Y.replace(np.nan,80.5)
        #df.Y = df.Y.astype(str)
        data[df][col] = data[df][col].replace(np.nan,80.5).copy()
        data[df][col] = data[df][col].astype(str)

    #for idx in df.index:
    #    if type(df.Y.iloc[idx]) != float:
    #        df.Y.iloc[idx] = float(df.Y.iloc[idx].replace(',','.'))
        for idx in data[df].index:
            try:
                if type(data[df][col].iloc[idx]) != float:
                    data[df][col].iloc[idx] = float(data[df][col].iloc[idx].replace(',','.'))
            except:
                print(df,col,idx)
                break
        
        data[df][col] = data[df][col].astype(float)

# %% [markdown]
# Tabla del precio medio de los productos de la tabla Compra y Ventas

# %%
# Tablas base
t = np.array(['Compra.csv','Venta.csv'])
t1 = [1,-2]
count = 0
for tablas in t:
    if tablas in archivos:
        # Valores unicos en el IdProducto en la tabla compras
        productos = data[t1[count]].IdProducto.unique()
        precio_medio = np.zeros((data[t1[count]].IdProducto.unique().shape[0],1))

        # Obtenemos el precio medio
        for idx, product in enumerate(productos):
            precio_medio[idx] = data[t1[count]].Precio[data[t1[count]].IdProducto == product].median()

        # Sustituimos el nulo por el precio medio
        for i in data[t1[count]][data[t1[count]].Precio.isnull() == True].index:
            data[t1[count]].Precio.iloc[i] = precio_medio[productos == data[t1[count]].IdProducto.iloc[i]]

    count+=1

# %% [markdown]
# Cambiamos el nombre de la columna state a provincia

# %%
data[4].rename(columns={data[4].columns[4] : 'provincia_nombre'}, inplace=True)
data[0].rename(columns={data[0].columns[1] : 'provincia_nombre'}, inplace=True)
data[-4].rename(columns={data[-4].columns[4] : 'provincia_nombre'}, inplace=True)

# %% [markdown]
# Levenshtein para normalizar el nombre de la provincia en todas las tablas

# %%
prov = data[3].provincia_nombre.unique()

# %%
data[0].provincia_nombre = data[0].provincia_nombre.fillna('xxxx')

# %%
t1 = [0,4,-4]
levenshtein = np.zeros((23,1))
levenshtein = levenshtein.sum(axis=1)
for table in t1:
    for row in data[table].index:
        if data[table].provincia_nombre.iloc[row] != 'xxxx':
            for idx, provincia in enumerate(prov):
                levenshtein[idx] = fuzz.token_set_ratio(data[table].provincia_nombre.iloc[row], provincia)
            #print(levenshtein)
            data[table].provincia_nombre.iloc[row] = prov[levenshtein == levenshtein.max()][0]

# %% [markdown]
# Normalizar el campo departamento en proveedores

# %%
#prov = data[3].departamento_nombre.unique()

# %%
#levenshtein = np.zeros((prov.shape[0],1))
#levenshtein = levenshtein.sum(axis=1)
#for row in data[-5].index:
#    for idx, departamento in enumerate(prov):
#        levenshtein[idx] = fuzz.token_set_ratio(data[-5].departamen.iloc[row], departamento)
    #print(levenshtein)
#    data[-5].departamen.iloc[row] = prov[levenshtein == levenshtein.max()][0]

# %% [markdown]
# Normalizar el campo localidad en tabla sucursales

# %%
# Tabla sucursales
prov = data[3].nombre.unique()
levenshtein = np.zeros((prov.shape[0],1))
levenshtein = levenshtein.sum(axis=1)
for row in data[-4].index:
    for idx, localidad in enumerate(prov):
        levenshtein[idx] = fuzz.token_set_ratio(data[-4].Localidad.iloc[row], localidad)
    #print(levenshtein)
    data[-4].Localidad.iloc[row] = prov[levenshtein == levenshtein.max()][0]

# Tabla proveedores
for row in data[-5].index:
    for idx, localidad in enumerate(prov):
        levenshtein[idx] = fuzz.token_set_ratio(data[-5].City.iloc[row], localidad)
    #print(levenshtein)
    data[-5].City.iloc[row] = prov[levenshtein == levenshtein.max()][0]

# %% [markdown]
# Outlayers en las tablas Compra, Venta y Gasto, columna Precio y Monto.

# %%
t1 = [1,-2]
zCompra = 0
zVenta = 0
for tabla in t1:
    # Calcular los rangos intercuartilicos para cada IdProducto
    prov = data[tabla].IdProducto.unique()
    rango = np.zeros((data[tabla].IdProducto.unique().shape[0],2))
    for idx, producto in enumerate(prov):
        p25 = np.percentile(data[tabla].Precio[data[tabla].IdProducto == producto],25)
        p75 = np.percentile(data[tabla].Precio[data[tabla].IdProducto == producto],75)
        r = p75-p25
        m = data[tabla].Precio[data[tabla].IdProducto == producto].median()
        
        # Contar el numero de outlayers
        if tabla == 1:
            zCompra += data[tabla].Precio[(data[tabla].IdProducto == producto) & (data[tabla].Precio < p25-1.5*r)].shape[0]
            zCompra += data[tabla].Precio[(data[tabla].IdProducto == producto) & (data[tabla].Precio > p75+1.5*r)].shape[0]
        else:
            zVenta += data[tabla].Precio[(data[tabla].IdProducto == producto) & (data[tabla].Precio < p25-1.5*r)].shape[0]
            zVenta += data[tabla].Precio[(data[tabla].IdProducto == producto) & (data[tabla].Precio > p75+1.5*r)].shape[0]

        data[tabla].Precio[(data[tabla].IdProducto == producto) & (data[tabla].Precio < p25-1.5*r)] = copy.copy(m)
        data[tabla].Precio[(data[tabla].IdProducto == producto) & (data[tabla].Precio > p75+1.5*r)] = copy.copy(m)


# %%
zGasto = 0
tabla = 2
prov = data[tabla].IdTipoGasto.unique()
rango = np.zeros((data[tabla].IdTipoGasto.unique().shape[0],2))
for idx, producto in enumerate(prov):
    p25 = np.percentile(data[tabla].Monto[data[tabla].IdTipoGasto == producto],25)
    p75 = np.percentile(data[tabla].Monto[data[tabla].IdTipoGasto == producto],75)
    r = p75-p25
    m = data[tabla].Monto[data[tabla].IdTipoGasto == producto].median()

    # cantidad de outlayers
    zGasto += data[tabla].Monto[(data[tabla].IdTipoGasto == producto) & (data[tabla].Monto < p25-1.5*r)].shape[0]
    zGasto += data[tabla].Monto[(data[tabla].IdTipoGasto == producto) & (data[tabla].Monto > p75+1.5*r)].shape[0]

    data[tabla].Monto[(data[tabla].IdTipoGasto == producto) & (data[tabla].Monto < p25-1.5*r)] = copy.copy(m)
    data[tabla].Monto[(data[tabla].IdTipoGasto == producto) & (data[tabla].Monto > p75+1.5*r)] = copy.copy(m)

# %%
# Cantidad de outlayers

print(zCompra/data[1].shape[0])
print(zVenta/data[-2].shape[0])
print(zGasto/data[2].shape[0])

# %% [markdown]
# Separar tablas para crear relaciones

# %%
data[3].provincia_nombre.unique()

# %%
# Tabla de provincias
provincias = data[3][['provincia_id','provincia_nombre']]
provincias.drop_duplicates(inplace=True)
print(provincias.provincia_nombre.unique())

# %% [markdown]
# Eliminar columnas innecesarias

# %%
data[0].drop(columns='col10',inplace=True)

# %% [markdown]
# Crear y volver a cargar csv de Canal de venta

# %%
tablas = [data[8],data[0],data[4],data[5],data[6],data[1],data[7],data[2]]

# %% [markdown]
# Cargar las tablas a la base de datos

# %%
# Conectandome a la base de datos
import mysql.connector
from mysql.connector import Error

# %%
conn = mysql.connector.connect(host='localhost',
                                       database='proyectoIndividual',
                                       user='root',
                                       password='root')

cur = conn.cursor()

# %%
# Subir Canal de venta
for idx in tablas[0].index:
    cur.execute('''insert ignore into CanalDeVenta (ID_CanalDeVenta, DESCRIPCION)
        VALUES ( %s, %s )''', ( str(data[8].ID_CanalDeVenta[idx]), data[8].DESCRIPCION[idx] ) )

conn.commit()

# %%
# Update Clientes
for idx in tablas[1].index:
    values = tablas[1].iloc[idx]
    for idx,i in enumerate(values):
        values[idx] = str(i)
    cur.execute('''insert ignore into Clientes (ID_Clientes,provincia_nombre,Nombre_y_Apellido,Domicilio,Telefono,Edad,Localidad,Longitud,Latitud)
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s)   ''', list(values.values))

conn.commit()

# %%
# Update Proveedores
#['ID_Proveedores', 'Nombre', 'Address', 'Localidad', 'Country', 'departamen']
for idx in tablas[2].index:
    values = tablas[2].iloc[idx]
    for idx,i in enumerate(values):
        if idx == 0:
            values[idx] = str(i)
    try :cur.execute('''insert ignore into Proveedores (ID_Proveedores,Nombre,Address,Localidad,Country,departamen)
        values (%s,%s,%s,%s,%s,%s)   ''', list(values.values))
    except:
        pass

conn.commit()

# %%
# Update Sucursales
#['ID_Sucursales', 'Sucursal', 'Direccion', 'Localidad', 'Latitud', 'Longitud']
for idx in tablas[3].index:
    values = tablas[3].iloc[idx]
    for idx,i in enumerate(values):
        values[idx] = str(i)
    cur.execute('''insert ignore into Sucursales (ID_Sucursales,Sucursal,Direccion,Localidad,Latitud,Longitud)
        values (%s,%s,%s,%s,%s,%s)   ''', list(values.values))

conn.commit()

# %%
# Update TiposDeGasto
# ['ID_TiposDeGasto', 'Descripcion', 'Monto_Aproximado']

for idx in tablas[4].index:
    values = tablas[4].iloc[idx]
    for idx,i in enumerate(values):
        values[idx] = str(i)
    cur.execute('''insert ignore into TiposDeGasto (ID_TiposDeGasto,Descripcion,Monto_Aproximado)
        values (%s,%s,%s)   ''', list(values.values))
conn.commit()

# %%
# Update Compra
# ['ID_Compra', 'Fecha', 'Fecha_Año', 'Fecha_Mes', 'Fecha_Periodo', 'IdProducto', 'Cantidad', 'Precio', 'IdProveedor']

for idx in tablas[5].index:
    values = tablas[5].iloc[idx]
    for idx,i in enumerate(values):
        values[idx] = str(i)
    cur.execute('''insert ignore into Compra (ID_Compra,Fecha,Fecha_Año,Fecha_Mes,Fecha_Periodo,IdProducto,Cantidad,Precio,IdProveedor)
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s)   ''', list(values.values))

# %%
conn.commit()

# %%
# Update Venta
# ['ID_Venta', 'Fecha', 'Fecha_Entrega', 'IdCanal', 'IdCliente', 'IdSucursal', 'IdEmpleado', 'IdProducto', 'Precio', 'Cantidad']

for idx in tablas[6].index:
    values = tablas[6].iloc[idx]
    for idx,i in enumerate(values):
        values[idx] = str(i)
    cur.execute('''insert ignore into Venta (ID_Venta, Fecha, Fecha_Entrega, IdCanal, IdCliente, IdSucursal, IdEmpleado, IdProducto, Precio, Cantidad)
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)   ''', list(values.values))
conn.commit()

# %%
conn.commit()

# %%
# Update Gasto
# ['ID_Gasto', 'IdSucursal', 'IdTipoGasto', 'Fecha', 'Monto']

for idx in tablas[7].index:
    values = tablas[7].iloc[idx]
    for idx,i in enumerate(values):
        values[idx] = str(i)
    cur.execute('''insert ignore into Gasto (ID_Gasto,IdSucursal,IdTipoGasto,Fecha,Monto)
        values (%s,%s,%s,%s,%s)   ''', list(values.values))
conn.commit()

# %%
conn.close()

# %%
#archivos

# %%
#for idx, table in enumerate(data):
#    print(list(table.columns))


