
create database desk;
use desk;

create table work_space(
work_space_id int auto_increment primary key,
work_space_name varchar(255) not null,
image varchar(255) not null,
address varchar(255) not null
);

create table block(
block_id int auto_increment primary key,
block_name varchar(255) not null,
image varchar(255) not null,
work_space_id int,
foreign key (work_space_id) references work_space(work_space_id) 
);

create table floors(
floor_id int auto_increment primary key,
floor_no varchar(255) not null,
image varchar(255) not null,
block_id int,
foreign key (block_id) references block(block_id) 
);

create table desk(
desk_id int auto_increment primary key,
image varchar(255) not null,
desk_title varchar(255) not null,
charge_per_day varchar(255) not null,
status varchar(255) not null,
floor_id int,
number_of_desks varchar(255) not null,
foreign key (floor_id) references floors(floor_id)
);

create table employee(
employee_id int auto_increment primary key,
employee_name varchar(255) not null,
phone varchar(255) not null,
email varchar(255) not null,
password varchar(255) not null,
address varchar(255) not null,
occuption varchar(255) not null,
gender varchar(255) not null,
age varchar(255) not null
);


create table employee_booking(
employee_booking_id int auto_increment primary key,
status varchar(255) not null,
date varchar(255) not null,
from_date_time varchar(255) not null,
to_date_time varchar(255) not null,
desk_id int,
employee_id int not null not null default '0',
total_amount varchar(255),
foreign key (employee_id) references employee(employee_id),
foreign key (desk_id) references desk(desk_id)
);

create table booking_desk(
booking_desk_id int auto_increment primary key,
employee_booking_id int,
desk_numbers varchar(255),
foreign key (employee_booking_id) references employee_booking(employee_booking_id)
);





