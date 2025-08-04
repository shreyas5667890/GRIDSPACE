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
-- Table structure for table `apartment_details`
--

DROP TABLE IF EXISTS `apartment_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartment_details` (
  `ROOM_NO` int NOT NULL,
  `APT_TITLE` varchar(200) NOT NULL,
  `AREA` int NOT NULL,
  `APARTMENT_DESC` varchar(1000) NOT NULL,
  PRIMARY KEY (`ROOM_NO`),
  CONSTRAINT `apartment_details_ibfk_1` FOREIGN KEY (`ROOM_NO`) REFERENCES `apartment` (`ROOM_NO`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartment_details`
--

LOCK TABLES `apartment_details` WRITE;
/*!40000 ALTER TABLE `apartment_details` DISABLE KEYS */;
INSERT INTO `apartment_details` VALUES (1,'Sai Krupa Residency',850,'A serene 2BHK flat with a peaceful view, ideal for working professionals and small families.'),(2,'Gokul Heights',1050,'Spacious 3BHK apartment with modular kitchen, pooja room, and nearby temple access.'),(3,'Shanti Niketan',700,'A cozy 1BHK in a gated society with 24x7 security and nearby market.'),(4,'Ashiyana Greens',1200,'Modern 3BHK apartment with garden-facing balcony and kids play area.');
/*!40000 ALTER TABLE `apartment_details` ENABLE KEYS */;
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
