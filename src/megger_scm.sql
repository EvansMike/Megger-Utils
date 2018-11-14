-- MySQL dump 10.16  Distrib 10.2.18-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: megger
-- ------------------------------------------------------
-- Server version	10.2.18-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assets`
--

DROP TABLE IF EXISTS `assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets` (
  `asset_num` int(11) NOT NULL,
  `site` int(11) DEFAULT NULL,
  `asset_id` varchar(100) NOT NULL,
  `test` varchar(100) DEFAULT NULL,
  `serial` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `test_date` date DEFAULT NULL,
  `next_date` date DEFAULT NULL,
  `test_interval` varchar(100) DEFAULT NULL,
  `VA` int(11) DEFAULT NULL,
  `m1` int(11) DEFAULT NULL,
  PRIMARY KEY (`asset_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients` (
  `client_num` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `addr1` varchar(100) DEFAULT NULL,
  `addr2` varchar(100) DEFAULT NULL,
  `addr3` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`client_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `faults`
--

DROP TABLE IF EXISTS `faults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faults` (
  `fault_num` varchar(100) NOT NULL,
  `descrip` varchar(255) NOT NULL,
  `repair_num` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`fault_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `repairs`
--

DROP TABLE IF EXISTS `repairs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `repairs` (
  `repair_num` int(11) NOT NULL AUTO_INCREMENT,
  `fault_num` varchar(100) NOT NULL,
  `descrip` varchar(255) DEFAULT NULL,
  `asset_id` varchar(12) NOT NULL,
  PRIMARY KEY (`repair_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `results` (
  `asset_num` int(11) DEFAULT NULL,
  `test_date` date NOT NULL,
  `test_num` int(11) NOT NULL,
  `user_num` int(11) DEFAULT NULL,
  `m1` int(11) DEFAULT NULL,
  `m2` int(11) DEFAULT NULL,
  `e_bond_1` double DEFAULT NULL,
  `e_bond_2` double DEFAULT NULL,
  `m3` varchar(100) DEFAULT NULL,
  `insulation` double DEFAULT NULL,
  `VA` double DEFAULT NULL,
  `e_leakage` double NOT NULL,
  `m4` varchar(100) DEFAULT NULL,
  `fault_num` varchar(100) DEFAULT NULL,
  `repair_num` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`test_date`,`test_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sites` (
  `site_num` int(11) NOT NULL,
  `client_num` int(11) DEFAULT NULL,
  `m1` varchar(100) DEFAULT NULL,
  `site_name` varchar(100) DEFAULT NULL,
  `m2` varchar(100) DEFAULT NULL,
  `m3` varchar(100) DEFAULT NULL,
  `m4` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`site_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-14 10:36:17
