create table if not exists users
(
    id int auto_increment primary key,
    user_id bigint unsigned not null unique,
    user_name varchar(255) not null,
    use_count int unsigned not null default 0
);