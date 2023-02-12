-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `admin_id` varchar(8) DEFAULT NULL,
  `admin_name` varchar(20) DEFAULT NULL,
  `password` varchar(9) DEFAULT NULL,
  `right` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('xz3165','Xintong Zhan','123','root'),('fz2348','Feitong Zhu','123','root');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book` (
  `isbn` varchar(13) DEFAULT NULL,
  `book_name` varchar(40) DEFAULT NULL,
  `author` varchar(23) DEFAULT NULL,
  `press` varchar(30) DEFAULT NULL,
  `class_name` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES ('978704015109X','ERP Principle and Application Training','Qingming Wang','Higher Education Press','Management Social Sciences'),('9787040273243','Management Information System','Tiyun Huang','Higher Education Press','Management Social Sciences'),('9787115335500','node.js Tutorial','Ling Pak','Posts and Telecommunications Press','Computer Technology'),('9787121204869','Mobile Design','Xiaozhen Fu','Electronic Industry Press','Automation Technology'),('9787302292609','Experiment Course of ERP Production Management System','Lili Zhang','Tsinghua University Press','Management Social Sciences'),('978710800982x','Fifteen Years of Wanli','Renyu Huang','Joint Publishing','Chinese history'),('9787115488763','Python Deep Learning','Francois Scholet','Posts and Telecommunications Press','Computer Technology'),('9787226044094','Dictionary of Music','Tiankang Gao','Gansu Press','Music'),('9787115275790','JavaScript Advanced Programming - Version 3','Nicholas C. Zakas','Peking University Press','Computer Technology'),('9787302423287','Machine Learning','Zhihua Zhou','Tsinghua University Press','Computer Technology'),('9787543862326','The End of Chinese Zhiqin','Xian Deng','Hunan Press','Chinese Literature'),('9787810823620','ERP Principle and Practice','Dan Chang','Beijing Jiaotong University Press','Management Social Sciences'),('9787115373991','Flask Web Development','Green Boog','Posts and Telecommunications Press','Computer Technology');
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory` (
  `barcode` mediumint(9) DEFAULT NULL,
  `isbn` varchar(13) DEFAULT NULL,
  `storage_date` bigint(20) DEFAULT NULL,
  `location` varchar(13) DEFAULT NULL,
  `withdraw` tinyint(4) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL,
  `admin` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (102341,'9787302423287',1514736000000,'1 floor,02 shelf,3 row,4 column',0,0,'xz3165'),(102342,'9787302423287',1514736000000,'1 floor,02 shelf,3 row,4 column',0,1,'xz3165'),(102343,'9787302423287',1514736000000,'1 floor,02 shelf,3 row,4 column',0,1,'xz3165'),(102344,'9787302423287',1514736000000,'1 floor,02 shelf,3 row,4 column',0,1,'xz3165'),(211411,'9787302292609',1514736000000,'2 floor,11 shelf,4 row,1 column',0,1,'xz3165'),(211412,'9787302292609',1514736000000,'2 floor,11 shelf,4 row,1 column',0,1,'xz3165'),(211413,'9787302292609',1514736000000,'2 floor,11 shelf,4 row,1 column',0,1,'xz3165'),(201231,'978704015109X',1515168000000,'2 floor,01 shelf,2 row,3 column',0,1,'xz3165'),(201232,'978704015109X',1515168000000,'2 floor,01 shelf,2 row,3 column',0,1,'xz3165'),(201233,'978704015109X',1515168000000,'2 floor,01 shelf,2 row,3 column',0,1,'xz3165'),(202331,'9787040273243',1515772800000,'2 floor,02 shelf,3 row,3 column',0,0,'fz2348'),(202332,'9787040273243',1515772800000,'2 floor,02 shelf,3 row,3 column',0,1,'fz2348'),(104341,'9787115335500',1514995200000,'1 floor,04 shelf,3 row,4 column',0,1,'xz3165'),(104342,'9787115335500',1514995200000,'1 floor,04 shelf,3 row,4 column',0,1,'xz3165'),(104343,'9787115335500',1514995200000,'1 floor,04 shelf,3 row,4 column',0,1,'xz3165'),(104344,'9787121204869',1546358400000,'1 floor,04 shelf,3 row,4 column',0,1,'xz3165'),(104345,'9787121204869',1514822400000,'1 floor,04 shelf,3 row,4 column',0,1,'xz3165'),(310321,'978710800982x',1517587200000,'3 floor,10 shelf,3 row,2 column',0,1,'fz2348'),(310322,'978710800982x',1517587200000,'3 floor,10 shelf,3 row,2 column',0,1,'fz2348'),(310323,'978710800982x',1517587200000,'3 floor,10 shelf,3 row,2 column',0,1,'fz2348'),(309331,'9787115488763',1515081600000,'3 floor,09 shelf,3 row,3 column',0,1,'xz3165'),(309332,'9787115488763',1515081600000,'3 floor,09 shelf,3 row,3 column',0,1,'xz3165'),(309333,'9787115488763',1515081600000,'3 floor,09 shelf,3 row,3 column',0,1,'xz3165'),(401281,'9787226044094',1515772800000,'4 floor,01 shelf,2 row,8 column',0,1,'xz3165'),(401282,'9787226044094',1515772800000,'4 floor,01 shelf,2 row,8 column',0,1,'xz3165'),(308371,'9787115275790',1516377600000,'3 floor,08 shelf,3 row,7 column',0,1,'xz3165'),(308372,'9787115275790',1516377600000,'3 floor,08 shelf,3 row,7 column',0,1,'xz3165'),(308373,'9787115275790',1516377600000,'3 floor,08 shelf,3 row,7 column',0,1,'xz3165'),(411361,'9787543862326',1516982400000,'4 floor,11 shelf,3 row,6 column',0,1,'xz3165'),(411362,'9787543862326',1516982400000,'4 floor,11 shelf,3 row,6 column',0,1,'xz3165'),(203771,'9787810823620',1517328000000,'2 floor,03 shelf,7 row,7 column',0,1,'fz2348'),(203772,'9787810823620',1517328000000,'2 floor,03 shelf,7 row,7 column',0,1,'fz2348'),(203773,'9787810823620',1517328000000,'2 floor,03 shelf,7 row,7 column',0,1,'fz2348'),(102345,'9787302423287',1547130451000,'1 floor,02 shelf,3 row,4 column',0,1,'xz3165'),(102346,'9787115373991',1547222400000,'1 floor,02 shelf,3 row,4 column',0,0,'xz3165'),(102347,'9787115373991',1547222400000,'1 floor,02 shelf,3 row,4 column',0,0,'xz3165'),(102348,'9787115373991',1547222400000,'1 floor,02 shelf,3 row,4 column',0,1,'xz3165');
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `readbook`
--

DROP TABLE IF EXISTS `readbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `readbook` (
  `id` mediumint(9)  primary key auto_increment,
  `barcode` mediumint(9) DEFAULT NULL,
  `card_id` varchar(20) DEFAULT NULL,
  `start_date` bigint(20) DEFAULT NULL,
  `borrow_admin` varchar(20) DEFAULT NULL,
  `end_date` varchar(13) DEFAULT NULL,
  `return_admin` varchar(20) DEFAULT NULL,
  `due_date` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `readbook`
--

LOCK TABLES `readbook` WRITE;
/*!40000 ALTER TABLE `readbook` DISABLE KEYS */;
INSERT INTO `readbook` VALUES (1,102341,16000001,1544371200000,'xz3165','1546704000000','xz3165',1547827200000),(2,102342,16000002,1545926400000,'xz3165','1546876800000','xz3165',1549382400000),(3,310321,16000001,1546012800000,'xz3165','1546790400000','xz3165',1549468800000),(4,203773,16000001,1546012800000,'xz3165','1546790400000','fz2348',1549468800000),(5,310322,16000002,1546012800000,'xz3165','1546876800000','fz2348',1549468800000),(7,309333,16000001,1546358400000,'xz3165','1547222400000','xz3165',1549814400000),(8,102341,16000001,1547222400000,'xz3165','','',1550678400000),(9,211411,16000003,1547222400000,'xz3165','','',1550678400000),(10,202331,16000003,1547222400000,'xz3165','','',1550678400000),(11,102347,16000001,1547222400000,'xz3165','','',1550678400000);
/*!40000 ALTER TABLE `readbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `card_id` varchar(15) DEFAULT NULL,
  `student_id` varchar(15) DEFAULT NULL,
  `student_name` varchar(20) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `telephone` bigint(20) DEFAULT NULL,
  `enroll_date` bigint(20) DEFAULT NULL,
  `valid_date` bigint(20) DEFAULT NULL,
  `loss` tinyint(4) DEFAULT NULL,
  `debt` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('fz2348','fz2348','Feitong Zhu','Female',18921902722,1544371200000,2644371200000,0,0),('dq1232','dq1232','Dan Qing','Female',1593446400000,1544371200000,2564371200000,0,0),('ka4634','ka4634','Kris Alex','Male',1593446400000,1544371200000,2644371200000,0,0),('xz3165','xz3165','Xintong Zhan','Male',9291212291,1544371200000,2644371200000,0,0);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-22 15:20:25
