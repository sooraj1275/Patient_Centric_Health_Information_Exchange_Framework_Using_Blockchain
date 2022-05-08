/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - vetapp
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`vetapp` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `vetapp`;

/*Table structure for table `articlelink` */

DROP TABLE IF EXISTS `articlelink`;

CREATE TABLE `articlelink` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `articlelink` */

insert  into `articlelink`(`aid`,`title`,`content`) values 
(1,'hope','hi my name is'),
(4,'aaaa','sd'),
(3,'aaaaa','aaaaaa'),
(5,'aaaa','sd'),
(7,'dgd','ds'),
(8,'adfdsfsfdsfdsf','ds'),
(9,'dgd','ds');

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `bid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `scid` int(11) DEFAULT NULL,
  PRIMARY KEY (`bid`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`bid`,`userid`,`scid`) values 
(1,8,2),
(2,8,2),
(3,8,2),
(4,8,2),
(5,8,2);

/*Table structure for table `comment` */

DROP TABLE IF EXISTS `comment`;

CREATE TABLE `comment` (
  `cmid` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(200) DEFAULT NULL,
  `postid` int(11) DEFAULT NULL,
  `ulid` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`cmid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `comment` */

insert  into `comment`(`cmid`,`comment`,`postid`,`ulid`,`date`) values 
(1,'sgddhd',1,8,'2022-03-30'),
(2,'fggg',1,8,'2022-03-30'),
(3,'gsjdgkdd',3,8,'2022-03-30'),
(4,'dyddydududu',3,8,'2022-03-30'),
(5,'xyddddu',3,8,'2022-03-30'),
(6,'xghdd',4,8,'2022-03-30'),
(7,'ydddydy',4,8,'2022-03-30'),
(8,'ufff cjff ghh hhh hhj huu hhh hhh ',1,8,'2022-03-30'),
(9,'gxhx gjgj kggiv kggiv kiig jgg ',1,8,'2022-03-30'),
(10,'xhkhldf',1,8,'2022-03-30'),
(11,'hduffufup gjjgjg giigjg gigjggi gjjggj',1,8,'2022-03-30'),
(12,'xhfj',1,8,'2022-03-30');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `doctorid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `phonenumber` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `photo` varchar(50) DEFAULT NULL,
  `latitude` varchar(50) DEFAULT NULL,
  `longitude` varchar(50) DEFAULT NULL,
  `qualification` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `pin` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`doctorid`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `doctor` */

insert  into `doctor`(`doctorid`,`lid`,`name`,`gender`,`phonenumber`,`email`,`photo`,`latitude`,`longitude`,`qualification`,`place`,`pin`,`post`,`district`,`status`) values 
(1,3,'hfhf','m','2310','sdfnkjz','/static/doctor/IMG-20211026-WA0038.jpg','saxdx','wsdcds','dcssdc','wced','616312','dcs','sdc','approved'),
(2,2,'admin','mal','51122','eerw','/static/doctor/IMG-20211026-WA0038.jpg','rrer','rede','e45e','rewer','324556','dssa','edsr','pending'),
(3,4,'admin','Male','09207614811','gghjhh','/static/doctor/IMG-20211026-WA0038.jpg','cafgg','fafa','affvs','sfrstf','322','sfsr','asr','approved'),
(4,9,'Likhil','Male','9876542312','tlikhil@gmail.com','/static/doctor/abcd.jpg','11.12','12.12','MBBS','Kizhakkummuri','673611','Kizhakkummuri','Kozhikode','pending'),
(5,10,'Dr Likhil','Male','9876541234','drlikhil@gmail.com','/static/doctor/abcd.jpg','11.11','75.22','Kizhakkummuri','kakkodi','673611','Kakkodi','Kozhikode','approved');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `lid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`lid`,`username`,`password`,`type`) values 
(1,'admin','admin','admin'),
(2,'eerw','aaaa','doctor'),
(3,'gghjhh','ddddd','doctor'),
(4,'afna','ashi','doctor'),
(5,'likhil@gmail.com','9747360170','user'),
(6,'likhil@gmail.com','9747360170','user'),
(7,'likhil@gmail.com','9747360170','user'),
(8,'fg','1','user'),
(9,'tlikhil@gmail.com','123','doctor'),
(10,'drlikhil@gmail.com','123','doctor');

/*Table structure for table `post` */

DROP TABLE IF EXISTS `post`;

CREATE TABLE `post` (
  `postid` int(11) NOT NULL AUTO_INCREMENT,
  `post` varchar(200) DEFAULT NULL,
  `postdate` date DEFAULT NULL,
  `lid` int(11) DEFAULT NULL,
  PRIMARY KEY (`postid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `post` */

insert  into `post`(`postid`,`post`,`postdate`,`lid`) values 
(1,'hddjldlfjlf','2022-03-29',8),
(2,'hxcjgjgg','2022-03-29',8),
(3,'uffigogoyy','2022-03-29',8),
(4,'fiititiff ipftf hddfuf fjfjjffj fhfjfj','2022-03-29',8);

/*Table structure for table `question` */

DROP TABLE IF EXISTS `question`;

CREATE TABLE `question` (
  `qid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `questions` varchar(500) DEFAULT NULL,
  `reply` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`qid`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `question` */

insert  into `question`(`qid`,`userid`,`questions`,`reply`,`status`,`date`) values 
(1,3,'shit','pending','pending','2021-12-23'),
(2,3,'kooi','done','replied','2021-12-26'),
(3,3,'guys','what','pending','2021-12-28'),
(4,3,'going','free','pending','2021-12-30'),
(5,0,'vdjdjdkdd','pending','pending','2022-03-29'),
(6,0,'bdjdjjdjf','pending','pending','2022-03-29'),
(7,8,'hdhjddd','pending','pending','2022-03-29'),
(8,8,'hdjdjjdjf','pending','pending','2022-03-29'),
(9,8,'gdyddydud','pending','pending','2022-03-29'),
(10,8,'xhdff','pending','pending','2022-03-29');

/*Table structure for table `research` */

DROP TABLE IF EXISTS `research`;

CREATE TABLE `research` (
  `doctorid` int(11) DEFAULT NULL,
  `researchid` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(500) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `picture` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`researchid`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `research` */

insert  into `research`(`doctorid`,`researchid`,`description`,`title`,`content`,`picture`) values 
(NULL,9,'gfbz','vsCXV','xcVbCF\"\"\"\"','/static/flowers.jpg'),
(NULL,7,'hejtm','trejmj','afesgrhd\"\"\"','/static/20211229_122748.230720.jpg');

/*Table structure for table `schedule` */

DROP TABLE IF EXISTS `schedule`;

CREATE TABLE `schedule` (
  `scid` int(11) NOT NULL AUTO_INCREMENT,
  `dlid` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `fr` varchar(10) DEFAULT NULL,
  `tot` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`scid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `schedule` */

insert  into `schedule`(`scid`,`dlid`,`date`,`fr`,`tot`) values 
(2,9,'2022-03-31','14:41','14:46');

/*Table structure for table `tips` */

DROP TABLE IF EXISTS `tips`;

CREATE TABLE `tips` (
  `tipsid` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(50) DEFAULT NULL,
  `image` varchar(50) DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`tipsid`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `tips` */

insert  into `tips`(`tipsid`,`description`,`image`,`title`) values 
(9,'Do what you like most','/static/tips/abcd.jpg','Tip1'),
(10,'Tips2 description','/static/tips/bac.jpg','Tip2');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `phonenumber` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `photo` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`userid`,`lid`,`name`,`gender`,`phonenumber`,`email`,`photo`,`place`,`district`,`pin`) values 
(1,3,'shibu','m',13253132,'khgjtrgu','jhfyuhj','fugkh','jhhgbb',1234),
(2,8,'Likhil','male',2147483647,'likhil@gmail.com','/static/user_image/20220329_185058.jpg','Kakkodi','Kozhikode',673611);

/*Table structure for table `vaccine` */

DROP TABLE IF EXISTS `vaccine`;

CREATE TABLE `vaccine` (
  `vid` int(11) NOT NULL AUTO_INCREMENT,
  `vaccine` varchar(50) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `animal` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`vid`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `vaccine` */

insert  into `vaccine`(`vid`,`vaccine`,`description`,`animal`) values 
(8,'covid','sssssssssss','cat'),
(7,'ashiiique','v jhm','dog'),
(9,'kjhdhfh','kjhkhd','cat');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
