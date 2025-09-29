-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: trive
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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `account_type` enum('Custmer','Admin') NOT NULL DEFAULT 'Custmer',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,'Harry','harry@gmail.com','112233','Admin'),(2,'ben','ben@gmail','112233','Custmer');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking_table`
--

DROP TABLE IF EXISTS `booking_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking_table` (
  `booking_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `flight_id` int DEFAULT NULL,
  `seats_booked` int NOT NULL DEFAULT '0',
  `booking_date` timestamp NULL DEFAULT NULL,
  `booking_status` varchar(45) NOT NULL DEFAULT 'Not booked',
  PRIMARY KEY (`booking_id`),
  KEY `fk_user_id` (`user_id`),
  KEY `fk_flight_id` (`flight_id`),
  CONSTRAINT `fk_flight_id` FOREIGN KEY (`flight_id`) REFERENCES `flight_info1` (`idAir_jorneys`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking_table`
--

LOCK TABLES `booking_table` WRITE;
/*!40000 ALTER TABLE `booking_table` DISABLE KEYS */;
INSERT INTO `booking_table` VALUES (1,1,3,2,NULL,'Not booked');
/*!40000 ALTER TABLE `booking_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight_info1`
--

DROP TABLE IF EXISTS `flight_info1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_info1` (
  `idAir_jorneys` int NOT NULL AUTO_INCREMENT,
  `Depart` varchar(45) NOT NULL,
  `Time_depart` varchar(45) NOT NULL,
  `Arrive` varchar(45) NOT NULL,
  `Time_arrive` varchar(45) NOT NULL,
  `total_seats` int DEFAULT '130',
  `Seat cost` decimal(10,2) DEFAULT '100.00',
  `date_picked` datetime DEFAULT NULL,
  PRIMARY KEY (`idAir_jorneys`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_info1`
--

LOCK TABLES `flight_info1` WRITE;
/*!40000 ALTER TABLE `flight_info1` DISABLE KEYS */;
INSERT INTO `flight_info1` VALUES (1,'Newcastle','17:45','Bristol','19:00',130,100.00,NULL),(2,'Bristol','09:00','Newcastle','10:15',130,100.00,NULL),(3,'Cardiff','07:00','Edinburgh','08:30',130,100.00,NULL),(4,'Bristol','12:30','Manchester','13:30',130,100.00,NULL),(5,'Manchester','13:20','Bristol','14:20',130,100.00,NULL),(6,'Bristol','07:40','London','08:20',130,100.00,NULL),(7,'London','13:00','Manchester','14:00',130,100.00,NULL),(8,'Bristol','08:40','Glasgow','08:45',130,100.00,NULL),(9,'Glasgow','14:30','Newcastle','15:45',130,100.00,NULL),(10,'Newcastle','16:15','Manchester','17:05',130,100.00,NULL),(11,'Manchester','18:25','Bristol','19:30',130,100.00,NULL),(12,'Bristol','06:20','Manchester','07:20',130,100.00,NULL),(13,'Portsmouth','12:00','Dundee','14:00',130,100.00,NULL),(14,'Dundee','10:00','Portsmouth','12:00',NULL,100.00,NULL),(15,'Edinburgh','18:30','Cardiff','20:00',NULL,100.00,NULL),(16,'Southampton','12:00','Manchester','13:30',NULL,100.00,NULL),(17,'Manchester','19:00','Southampton','20:30',NULL,100.00,NULL),(18,'Birmingham','17:00','Newcastle','17:45',NULL,100.00,NULL),(19,'Newcastle','07:00','Birmingham','07:45',NULL,100.00,NULL),(20,'Aberdeen','08:00','Portsmouth','09:30',NULL,100.00,NULL);
/*!40000 ALTER TABLE `flight_info1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_table`
--

DROP TABLE IF EXISTS `payments_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_table` (
  `payment_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `booking_id` int DEFAULT NULL,
  `amount_paid` decimal(10,2) DEFAULT NULL,
  `payment_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `fk_payment_user_id` (`user_id`),
  KEY `fk_booking_id` (`booking_id`),
  CONSTRAINT `fk_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `booking_table` (`booking_id`),
  CONSTRAINT `fk_payment_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_table`
--

LOCK TABLES `payments_table` WRITE;
/*!40000 ALTER TABLE `payments_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receips_table`
--

DROP TABLE IF EXISTS `receips_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receips_table` (
  `receipt_id` int NOT NULL,
  `booking_id` int DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `receipt_data` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`receipt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receips_table`
--

LOCK TABLES `receips_table` WRITE;
/*!40000 ALTER TABLE `receips_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `receips_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'trive'
--

--
-- Dumping routines for database 'trive'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-19 15:49:22
