-- MySQL dump 10.13  Distrib 5.7.18, for macos10.12 (x86_64)
--
-- Host: localhost    Database: dota2
-- ------------------------------------------------------
-- Server version	5.7.18

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
-- Table structure for table `games_high`
--

DROP TABLE IF EXISTS `games_high`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `games_high` (
  `hero_id` int(4) NOT NULL,
  `win` bigint(32) DEFAULT NULL,
  `lose` bigint(32) DEFAULT NULL,
  PRIMARY KEY (`hero_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games_high`
--

LOCK TABLES `games_high` WRITE;
/*!40000 ALTER TABLE `games_high` DISABLE KEYS */;
/*!40000 ALTER TABLE `games_high` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `games_normal`
--

DROP TABLE IF EXISTS `games_normal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `games_normal` (
  `hero_id` int(4) NOT NULL,
  `win` bigint(32) DEFAULT NULL,
  `lose` bigint(32) DEFAULT NULL,
  PRIMARY KEY (`hero_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games_normal`
--

LOCK TABLES `games_normal` WRITE;
/*!40000 ALTER TABLE `games_normal` DISABLE KEYS */;
/*!40000 ALTER TABLE `games_normal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `games_veryhigh`
--

DROP TABLE IF EXISTS `games_veryhigh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `games_veryhigh` (
  `hero_id` int(4) NOT NULL,
  `win` bigint(32) DEFAULT NULL,
  `lose` bigint(32) DEFAULT NULL,
  PRIMARY KEY (`hero_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games_veryhigh`
--

LOCK TABLES `games_veryhigh` WRITE;
/*!40000 ALTER TABLE `games_veryhigh` DISABLE KEYS */;
/*!40000 ALTER TABLE `games_veryhigh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches_high`
--

DROP TABLE IF EXISTS `matches_high`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `matches_high` (
  `match_id` bigint(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches_high`
--

LOCK TABLES `matches_high` WRITE;
/*!40000 ALTER TABLE `matches_high` DISABLE KEYS */;
/*!40000 ALTER TABLE `matches_high` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches_normal`
--

DROP TABLE IF EXISTS `matches_normal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `matches_normal` (
  `match_id` bigint(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches_normal`
--

LOCK TABLES `matches_normal` WRITE;
/*!40000 ALTER TABLE `matches_normal` DISABLE KEYS */;
/*!40000 ALTER TABLE `matches_normal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches_veryhigh`
--

DROP TABLE IF EXISTS `matches_veryhigh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `matches_veryhigh` (
  `match_id` bigint(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches_veryhigh`
--

LOCK TABLES `matches_veryhigh` WRITE;
/*!40000 ALTER TABLE `matches_veryhigh` DISABLE KEYS */;
/*!40000 ALTER TABLE `matches_veryhigh` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-09 19:53:10
