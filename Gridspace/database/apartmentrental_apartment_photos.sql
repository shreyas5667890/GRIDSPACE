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
-- Table structure for table `apartment_photos`
--

DROP TABLE IF EXISTS `apartment_photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartment_photos` (
  `ROOM_NO` int NOT NULL,
  `PATHNAME` varchar(100) NOT NULL,
  `PHOTO1` varchar(50) NOT NULL,
  `PHOTO2` varchar(50) NOT NULL,
  `PHOTO3` varchar(50) NOT NULL,
  `PHOTO4` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ROOM_NO`),
  CONSTRAINT `apartment_photos_ibfk_1` FOREIGN KEY (`ROOM_NO`) REFERENCES `apartment` (`ROOM_NO`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartment_photos`
--

LOCK TABLES `apartment_photos` WRITE;
/*!40000 ALTER TABLE `apartment_photos` DISABLE KEYS */;
INSERT INTO `apartment_photos` VALUES (1,'images/Apartment1','Bedroom.jpg','Diningroom.jpg','Hall.jpg','Kitchen.jpg'),(2,'images/Apartment2','Bedroom.jpg','Diningroom.jpg','Hall.jpg','Kitchen.jpg'),(3,'images/Apartment3','Bedroom.jpg','Diningroom.jpg','Hall.jpg','Kitchen.jpg'),(4,'images/Apartment4','Bedroom.jpg','Diningroom.jpg','Hall.jpg','Kitchen.jpg');
/*!40000 ALTER TABLE `apartment_photos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-18  8:19:26
