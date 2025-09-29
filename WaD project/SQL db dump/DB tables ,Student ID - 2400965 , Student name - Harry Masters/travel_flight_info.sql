CREATE DATABASE  IF NOT EXISTS `travel` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `travel`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: travel
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `flight_info`
--

DROP TABLE IF EXISTS `flight_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_info` (
  `idAir_jorneys` int NOT NULL AUTO_INCREMENT,
  `Depart` varchar(45) NOT NULL,
  `Time_depart` varchar(45) NOT NULL,
  `Arrive` varchar(45) NOT NULL,
  `Time_arrive` varchar(45) NOT NULL,
  `total_seats` int DEFAULT '130',
  `Seat_cost` decimal(10,2) DEFAULT '100.00',
  `date_picked` datetime DEFAULT NULL,
  PRIMARY KEY (`idAir_jorneys`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_info`
--

LOCK TABLES `flight_info` WRITE;
/*!40000 ALTER TABLE `flight_info` DISABLE KEYS */;
INSERT INTO `flight_info` VALUES (1,'Newcastle','17:45','Bristol','19:00',130,90.00,NULL),(2,'Bristol','09:00','Newcastle','10:15',130,90.00,NULL),(3,'Cardiff','07:00','Edinburgh','08:30',130,90.00,NULL),(4,'Bristol','12:30','Manchester','13:30',130,80.00,NULL),(5,'Manchester','13:20','Bristol','14:20',130,90.00,NULL),(6,'Bristol','07:40','London','08:20',130,80.00,NULL),(7,'London','13:00','Manchester','14:00',130,100.00,NULL),(8,'Bristol','08:40','Glasgow','08:45',130,110.00,NULL),(9,'Glasgow','14:30','Newcastle','15:45',130,100.00,NULL),(10,'Newcastle','16:15','Manchester','17:05',130,100.00,NULL),(11,'Manchester','18:25','Bristol','19:30',130,80.00,NULL),(12,'Bristol','06:20','Manchester','07:20',130,80.00,NULL),(13,'Portsmouth','12:00','Dundee','14:00',130,120.00,NULL),(14,'Dundee','10:00','Portsmouth','12:00',130,120.00,NULL),(15,'Edinburgh','18:30','Cardiff','20:00',130,90.00,NULL),(16,'Southampton','12:00','Manchester','13:30',130,90.00,NULL),(17,'Manchester','19:00','Southampton','20:30',130,90.00,NULL),(18,'Birmingham','17:00','Newcastle','17:45',130,100.00,NULL),(19,'Newcastle','07:00','Birmingham','07:45',130,100.00,NULL),(20,'Aberdeen','08:00','Portsmouth','09:30',130,100.00,NULL);
/*!40000 ALTER TABLE `flight_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-01 12:53:40
