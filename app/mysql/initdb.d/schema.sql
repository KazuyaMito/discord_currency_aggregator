create table if not exists users
(
    id int auto_increment primary key,
    user_id bigint unsigned not null unique,
    use_count int unsigned not null default 0
);