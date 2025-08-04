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
INSERT INTO `apartment_details` VALUES (1,'Sai Krupa Residency',850,'A serene 2BHK flat with a peaceful view, ideal for working professionals and small families.'),(2,'Gokul Heights',1050,'Spacious 3BHK apartment with modular kitchen, pooja room, and nearby temple access.'),(3,'Shanti Niketan',700,'A cozy 1BHK in a gated society with 24x7 security and nearby market.'),(4,'Sukhi niwas',451,'Modern 3BHK apartment with garden-facing balcony and kids play area.'),(5,'Green Valley Residency',900,'Well-ventilated 2BHK with a spacious layout and great connectivity.'),(6,'Lotus Enclave',1100,'Elegant 3BHK apartment with wooden flooring and ample natural light.'),(7,'Gitanjali Niwas',125,'Stylish 2BHK with modern interiors and close proximity to schools.'),(8,'Maple Heights',1250,'Premium 3BHK with modular kitchen and premium fittings in a gated complex.'),(9,'Rosewood Apartments',800,'Compact yet cozy 1BHK ideal for singles or couples, near public transport.'),(10,'Sunrise Residency',1200,'Spacious 2BHK apartment with access to gym, swimming pool, and nearby market. Perfect for families.'),(11,'Greenwood Heights',1100,'Modern apartment featuring in-house gym, children’s park, 24x7 security, and walking distance to supermarket.'),(12,'Bluebell Towers',1000,'Affordable living with WiFi, clubhouse, community hall, and local market nearby.'),(13,'Elite Enclave',1300,'Luxury apartment with rooftop gym, indoor games room, and organic vegetable store within complex.'),(14,'Harmony Homes',1250,'Beautifully designed flat with garden views, jogging track, and access to a nearby shopping mall.'),(15,'Serenity Suites',1150,'Fully furnished unit featuring gym access, reading lounge, and a mini-theatre.'),(16,'Maple Woods',1400,'Premium residence with co-working spaces, yoga center, kids play area, and nearby convenience store.'),(17,'Vista Valley',1350,'Elegant 3BHK with smart home features, central park, and multi-purpose gym.'),(18,'Lakeview Apartments',1500,'Stunning lake view, cycling track, fitness center, and all essential shops in walking distance.'),(19,'Urban Nest',1050,'Compact apartment with community kitchen, high-speed internet, marketplace, and access to fitness studio.');
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

-- Dump completed on 2025-08-04 20:20:35
