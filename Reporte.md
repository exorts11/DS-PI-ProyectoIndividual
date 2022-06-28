# Reporte de calidad de los datos 

### Datos nulos
Hay 5 tablas que contienen valores faltantes, la tabla de clientes, compra, localidades, proveedores y venta.
Sin embargo solo son 15 los campos que tienen datos nulos, la mayoria de la tabla de clientes. La tabla de clientes
tiene una columna vacia, 'col10'. Tambien tiene muchos datos duplicados en nombre, sin embargo analizandolos
aunque son los mismos nombres tienen datos diferentes de edad, direccion, etc, por lo que no puedo inferir que
sea el mismo cliente y este duplicado. Por lo tanto, no considero que tenga datos duplicados.

La cantidad de columnas nulas es alta, pero el porcentaje de nulos en cada no es mayor al 5%, por lo que no considero
que haya una mala calidad del dato en general.

Al igual que en los nulos, los datos atipicos no sobrepasan el 5% de los datos, algunos pudieron ser corregidos, por
lo que considero que el data set tiene buena salud.

