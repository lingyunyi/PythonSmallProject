/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50547
Source Host           : localhost:3306
Source Database       : libararysystem

Target Server Type    : MYSQL
Target Server Version : 50547
File Encoding         : 65001

Date: 2019-02-22 18:07:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for bookdb
-- ----------------------------
DROP TABLE IF EXISTS `bookdb`;
CREATE TABLE `bookdb` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `bookname` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `descs` varchar(255) DEFAULT NULL,
  `publish_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of bookdb
-- ----------------------------
INSERT INTO `bookdb` VALUES ('2', '1', '1', '1', '1.00', '1', '0000-00-00 00:00:00');

-- ----------------------------
-- Table structure for userdb
-- ----------------------------
DROP TABLE IF EXISTS `userdb`;
CREATE TABLE `userdb` (
  `id` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userdb
-- ----------------------------
INSERT INTO `userdb` VALUES ('0000000001', 'admin', 'admin');
INSERT INTO `userdb` VALUES ('0000000002', 'lingyunyi', '123');
INSERT INTO `userdb` VALUES ('0000000003', 'hello', 'sfasd');
INSERT INTO `userdb` VALUES ('0000000004', '123456', '123');
INSERT INTO `userdb` VALUES ('0000000005', 'wo', 'wo');
INSERT INTO `userdb` VALUES ('0000000006', 'asdf', '');
