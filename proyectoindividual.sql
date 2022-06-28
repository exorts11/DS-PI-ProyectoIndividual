create database proyectoIndividual;
use proyectoIndividual;

CREATE TABLE IF NOT EXISTS `CanalDeVenta` (
  `ID_CanalDeVenta`		INTEGER not null,
  `DESCRIPCION` 		varchar(30)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS `Clientes` (
  `ID_Clientes`			INTEGER not null,
  `provincia_nombre` 	varchar(30),
  `Nombre_y_Apellido` 	varchar(30),
  `Domicilio`			varchar(30), 
  `Telefono`			varchar(15),
  `Edad`				INTEGER,
  `Localidad`			varchar(30),
  `Longitud`			FLOAT,
  `Latitud`				FLOAT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS `Proveedores` (
  `ID_Proveedores`		INTEGER not null,
  `Nombre` 				varchar(30),
  `Address` 			varchar(30),
  `Localidad`			varchar(30),
  `Country`				varchar(30),
  `departamen`		varchar(30)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS `Sucursales` (
  `ID_Sucursales`		INTEGER not null,
  `Sucursal` 			varchar(30),
  `Direccion` 			varchar(30),
  `Localidad`			varchar(30),
  `Latitud`				FLOAT,
  `Longitud`			FLOAT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS `TiposDeGasto` (
  `ID_TiposDeGasto`			INTEGER not null,
  `Descripcion` 			integer,
  `Monto_Aproximado` 		float
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
  
CREATE TABLE IF NOT EXISTS `Compra` (
  `ID_Compra`			INTEGER not null,
  `Fecha` 				DATE NOT NULL,
  `Fecha_Año` 			integer,
  `Fecha_Mes`			integer, 
  `Fecha_Periodo`		integer,
  `IdProducto`			INTEGER,
  `Cantidad`			integer,
  `Precio`				FLOAT,
  `IdProveedor`			integer
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS `Venta` (
  `ID_Venta`			INTEGER not null,
  `Fecha` 				DATE NOT NULL,
  `Fecha_Entrega` 		DATE NOT NULL,
  `IdCanal`				integer, 
  `IdCliente`			integer,
  `IdSucursal`			INTEGER,
  `IdEmpleado`			integer,
  `IdProducto`			integer,
  `Precio`				float,
  `Cantidad`			integer
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS `Gasto` (
  `ID_Gasto`			INTEGER not null,
  `IdSucursal` 			integer,
  `IdTipoGasto` 		integer,
  `Fecha`				DATE NOT NULL,
  `Monto`				FLOAT
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
  
ALTER TABLE `Clientes` ADD PRIMARY KEY(`ID_Clientes`);

ALTER TABLE `Compra` ADD PRIMARY KEY(`ID_Compra`);
ALTER TABLE `Compra` ADD INDEX(`IdProveedor`);

ALTER TABLE `Gasto` ADD PRIMARY KEY(`ID_Gasto`);
ALTER TABLE `Gasto` ADD INDEX(`IdSucursal`);
ALTER TABLE `Gasto` ADD INDEX(`IdTipoGasto`);

ALTER TABLE `Proveedores` ADD PRIMARY KEY(`ID_Proveedores`);

ALTER TABLE `Sucursales` ADD PRIMARY KEY(`ID_Sucursales`);

ALTER TABLE `TiposDeGasto` ADD PRIMARY KEY(`ID_TiposDeGasto`);

ALTER TABLE `Venta` ADD PRIMARY KEY(`ID_Venta`);
ALTER TABLE `Venta` ADD INDEX(`IdCanal`);
ALTER TABLE `Venta` ADD INDEX(`IdCliente`);
ALTER TABLE `Venta` ADD INDEX(`IdSucursal`);

ALTER TABLE `CanalDeVenta` ADD PRIMARY KEY(`ID_CanalDeVenta`);

ALTER TABLE Compra ADD CONSTRAINT `compra_fk_provedor` FOREIGN KEY (IdProveedor) REFERENCES Proveedores (ID_Proveedores) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE Gasto ADD CONSTRAINT `gasto_fk_sucursal` FOREIGN KEY (IdSucursal) REFERENCES Sucursales (ID_Sucursales) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE Gasto ADD CONSTRAINT `gasto_fk_tipoGasto` FOREIGN KEY (IdTipoGasto) REFERENCES TiposDeGasto (ID_TiposDeGasto) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE Venta ADD CONSTRAINT `venta_fk_canal` FOREIGN KEY (IdCanal) REFERENCES CanalDeVenta (ID_CanalDeVenta) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE Venta ADD CONSTRAINT `venta_fk_cliente` FOREIGN KEY (IdCliente) REFERENCES Clientes (ID_Clientes) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE Venta ADD CONSTRAINT `venta_fk_sucursal` FOREIGN KEY (IdSucursal) REFERENCES Sucursales (ID_Sucursales) ON DELETE RESTRICT ON UPDATE RESTRICT;

