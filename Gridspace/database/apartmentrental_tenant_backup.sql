-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: apartmentrental
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tenant_backup`
--

DROP TABLE IF EXISTS `tenant_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tenant_backup` (
  `FNAME` varchar(25) DEFAULT NULL,
  `LNAME` varchar(15) DEFAULT NULL,
  `T_ID` int NOT NULL AUTO_INCREMENT,
  `PH_NO` varchar(12) DEFAULT NULL,
  `EMAIL` varchar(30) DEFAULT NULL,
  `GENDER` char(1) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `OCCUPATION` varchar(30) DEFAULT NULL,
  `ROOM_NO` int DEFAULT NULL,
  `PSWD` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`T_ID`),
  KEY `ROOM_NO` (`ROOM_NO`),
  CONSTRAINT `tenant_backup_ibfk_1` FOREIGN KEY (`ROOM_NO`) REFERENCES `apartment` (`ROOM_NO`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenant_backup`
--

LOCK TABLES `tenant_backup` WRITE;
/*!40000 ALTER TABLE `tenant_backup` DISABLE KEYS */;
INSERT INTO `tenant_backup` VALUES ('sairaj','naikdhure',2,'7894561230','sairajn@gmail.com','M','2005-02-01','student',4,NULL);
/*!40000 ALTER TABLE `tenant_backup` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-18  8:19:24
