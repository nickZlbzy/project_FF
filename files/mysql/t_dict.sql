create table t_log(
    id int primary key auto_increment COMMENT '唯一id',
    url varchar(50) not null COMMENT '请求路径',
    request_name varchar(50) COMMENT '请求模块名称',
    operation_type enum('i','u','d') COMMENT '操作类型',
    content varchar(80) COMMENT '操作内容',
    operation_user varchar(32) COMMENT '操作用户',
    operation_date datetime default now() COMMENT '操作时间',
    address varchar(32) not null COMMENT '操作用户ip',
    index(`operation_date`)
);

create table t_dict(
    id int primary key auto_increment,
    type varchar (10) not null comment "类型或标签类别",
    valid tinyint not null comment "key",
    value varchar (32) comment "value",
    sort int comment "排序,预留字段",
    remark varchar(50) comment "备注",
    create_time datetime default now() comment "创建时间",
    create_user varchar (32) comment "创建人",
    index(`valid`),
    index(`type`)
);

create table t_title_address(
    id int primary key auto_increment,
    url varchar(100),
    title varchar(50) not null,
    type varchar(20) not null comment "标题类别",
    sort int,
    parent_id int default 0 comment "父标题id",
    comment varchar(50) comment "备注",
    create_time datetime default now() comment "创建时间",
    create_user varchar (32) comment "创建人",
    index(`type`)
);














