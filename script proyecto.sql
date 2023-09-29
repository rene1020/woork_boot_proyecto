create database if not exists workbot;
use workbot;

create table if not exists usuarios(
id_usuario int auto_increment primary key,
nombre_usuario varchar(50) not null,
password varchar (255) not null,
email varchar(255) not null,
perfil_imagen varchar(255)
);

create table if not exists servidores(
id_server int auto_increment primary key,
nombre varchar(50) not null,
description text,
icon varchar(255)
);

create table if not exists canales(
id_canal int auto_increment primary key,
nombre varchar(100),
fk_server int not null,
foreign key (fk_server) references servidores (id_server) on delete cascade
);

create table if not exists mensajes(
id_mensaje int auto_increment primary key,
contenido text,
fk_usuario int not null,
foreign key (fk_usuario) references usuarios (id_usuario) on delete cascade,
fk_canal int not null,
foreign key (fk_canal) references canales (id_canal) on delete cascade
);

create table if not exists server_miembros(
fk_usuario int not null,
foreign key (fk_usuario) references usuarios (id_usuario) on delete cascade,
fk_server int not null,
foreign key (fk_server) references servidores (id_server) on delete cascade
);



