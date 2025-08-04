-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: gridspace
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
-- Table structure for table `apartment`
--

DROP TABLE IF EXISTS `apartment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartment` (
  `ROOM_NO` int NOT NULL,
  `BLOCK_NO` int DEFAULT NULL,
  `RENT_PER_MONTH` int DEFAULT NULL,
  `APT_STATUS` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`ROOM_NO`),
  KEY `BLOCK_NO` (`BLOCK_NO`),
  CONSTRAINT `apartment_ibfk_1` FOREIGN KEY (`BLOCK_NO`) REFERENCES `apartment_block` (`BLOCK_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartment`
--

LOCK TABLES `apartment` WRITE;
/*!40000 ALTER TABLE `apartment` DISABLE KEYS */;
INSERT INTO `apartment` VALUES (1,1,10000,'Occupied'),(2,2,12000,'Unoccupied'),(3,3,11000,'Unoccupied'),(4,4,20000,'unoccupied'),(5,2,5000,'Unoccupied'),(6,5,5000,'Unoccupied'),(7,7,10000,'unoccupied'),(8,8,12000,'Unoccupied'),(9,9,17000,'Unoccupied'),(10,1,15000,'Unoccupied'),(11,2,18000,'Unoccupied'),(12,3,17500,'Unoccupied'),(13,4,16000,'Unoccupied'),(14,5,20000,'Unoccupied'),(15,6,18500,'Unoccupied'),(16,7,17000,'Unoccupied'),(17,8,16500,'Unoccupied'),(18,9,19000,'Unoccupied'),(19,4,15500,'Unoccupied');
/*!40000 ALTER TABLE `apartment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-04 20:20:36
