create database if not exists `bilibili` default character set utf8mb4 collate utf8mb4_general_ci;
use `bilibili`;
set names utf8mb4;

create table if not exists `Guichu_Video`(
		`AvId` int unsigned not null,
		`Title` varchar(200) not null default '' comment '标题',
		`Sub` varchar(100) not null default '' comment '分区',
		`UpId` int unsigned not null,
		`UpName` varchar(255) not null default '' comment 'Up昵称',
		`CreateTime` timestamp not null comment '投稿时间',
		`Play` int unsigned not null default 0 comment '播放次数',
		`Danmaku` int unsigned not null default 0 comment '弹幕数',
		`Coin` int unsigned not null default 0 comment '硬币数',
		`Favourite` int unsigned not null default 0 comment '收藏数',
		`Reply` int unsigned not null default 0 comment '评论数',
		`Share` int unsigned not null default 0 comment '分享数',
		`Duration` int unsigned not null default 0 comment '时长',
		`Tag` varchar(600) not null default '' comment '标签',
		`Description` varchar(800) not null default '' comment '描述',
		`AvPic` varchar(255) not null default '' comment '封面地址',
		`UpFace` varchar(255) not null default '' comment 'Up头像地址',
		`ScrapedTime` timestamp not null comment '爬虫更新时间',
		Primary key(`AvId`)
		) Engine=InnoDB default charset=utf8mb4 collate=utf8mb4_general_ci;