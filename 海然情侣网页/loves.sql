/*
Navicat MySQL Data Transfer

Source Server         : 47.107.57.166
Source Server Version : 50727
Source Host           : 47.107.57.166:3306
Source Database       : loves

Target Server Type    : MYSQL
Target Server Version : 50727
File Encoding         : 65001

Date: 2020-04-03 13:14:28
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for diary
-- ----------------------------
DROP TABLE IF EXISTS `diary`;
CREATE TABLE `diary` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` varchar(255) DEFAULT NULL,
  `img_path` varchar(255) DEFAULT NULL,
  `create_day` varchar(255) DEFAULT NULL,
  `whois` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for memorial
-- ----------------------------
DROP TABLE IF EXISTS `memorial`;
CREATE TABLE `memorial` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` varchar(255) DEFAULT NULL,
  `img_path` varchar(255) DEFAULT NULL,
  `create_day` varchar(255) DEFAULT NULL,
  `whois` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
