
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `survey_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `survey_id` (`survey_id`),
  CONSTRAINT `emails_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `surveys` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `emails` WRITE;
/*!40000 ALTER TABLE `emails` DISABLE KEYS */;
INSERT INTO `emails` VALUES (4,'e@mail.ru',1),(5,'email@email.com',1),(6,'dev@email.org',1),(11,'e@mail.com',2),(12,'customer@email.com',2);
/*!40000 ALTER TABLE `emails` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `survey_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `result` json NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `survey_results` WRITE;
/*!40000 ALTER TABLE `survey_results` DISABLE KEYS */;
/*!40000 ALTER TABLE `survey_results` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `surveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `surveys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `survey` json NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `surveys` WRITE;
/*!40000 ALTER TABLE `surveys` DISABLE KEYS */;
INSERT INTO `surveys` VALUES (1,'Профессиональный опрос',1,'\"{\\\"questions\\\": [{\\\"title\\\": \\\"\\\\u0412\\\\u0432\\\\u0435\\\\u0434\\\\u0438\\\\u0442\\\\u0435 \\\\u0432\\\\u0430\\\\u0448\\\\u0443 \\\\u0441\\\\u0442\\\\u0440\\\\u0430\\\\u043d\\\\u0443\\\", \\\"type\\\": \\\"text\\\", \\\"isRequired\\\": false, \\\"validateAs\\\": \\\"string\\\"}, {\\\"title\\\": \\\"\\\\u0421\\\\u043a\\\\u043e\\\\u043b\\\\u044c\\\\u043a\\\\u043e \\\\u0432\\\\u0430\\\\u043c \\\\u043b\\\\u0435\\\\u0442?\\\", \\\"type\\\": \\\"radio\\\", \\\"isRequired\\\": false, \\\"answerOptions\\\": [\\\"< 20\\\", \\\"21 -30\\\", \\\"31 - 40\\\", \\\"> 40\\\"]}, {\\\"title\\\": \\\"\\\\u041a\\\\u0430\\\\u043a\\\\u043e\\\\u0439 \\\\u0443 \\\\u0432\\\\u0430\\\\u0441 \\\\u043e\\\\u043f\\\\u044b\\\\u0442 \\\\u0440\\\\u0430\\\\u0431\\\\u043e\\\\u0442\\\\u044b?\\\", \\\"type\\\": \\\"radio\\\", \\\"isRequired\\\": true, \\\"answerOptions\\\": [\\\"< 1 \\\\u0433\\\\u043e\\\\u0434\\\\u0430\\\", \\\"1 - 4 \\\\u0433\\\\u043e\\\\u0434\\\\u0430\\\", \\\"5 - 10 \\\\u043b\\\\u0435\\\\u0442\\\", \\\"> 10 \\\\u043b\\\\u0435\\\\u0442\\\"]}, {\\\"title\\\": \\\"\\\\u041a\\\\u0430\\\\u043a\\\\u0438\\\\u0435 \\\\u044f\\\\u0437\\\\u044b\\\\u043a\\\\u0438 \\\\u043f\\\\u0440\\\\u043e\\\\u0433\\\\u0440\\\\u0430\\\\u043c\\\\u043c\\\\u0438\\\\u0440\\\\u043e\\\\u0432\\\\u0430\\\\u043d\\\\u0438\\\\u044f \\\\u0432\\\\u044b \\\\u0438\\\\u0441\\\\u043f\\\\u043e\\\\u043b\\\\u044c\\\\u0437\\\\u0443\\\\u0435\\\\u0442\\\\u0435?\\\", \\\"type\\\": \\\"checkbox\\\", \\\"isRequired\\\": true, \\\"answerOptions\\\": [\\\"JavaScript\\\", \\\"Python\\\", \\\"Java\\\", \\\"C#\\\", \\\"PHP\\\", \\\"Ruby\\\", \\\"\\\\u0414\\\\u0440\\\\u0443\\\\u0433\\\\u043e\\\\u0435\\\"]}, {\\\"title\\\": \\\"\\\\u041a\\\\u0430\\\\u043a\\\\u0438\\\\u0435 \\\\u0411\\\\u0414 \\\\u0432\\\\u044b \\\\u0438\\\\u0441\\\\u043f\\\\u043e\\\\u043b\\\\u044c\\\\u0437\\\\u0443\\\\u0435\\\\u0442\\\\u0435?\\\", \\\"type\\\": \\\"checkbox\\\", \\\"isRequired\\\": true, \\\"answerOptions\\\": [\\\"Oracle\\\", \\\"MySQL\\\", \\\"Microsoft SQL Server\\\", \\\"PostgreSQL\\\", \\\"MongoDB\\\", \\\"\\\\u0414\\\\u0440\\\\u0443\\\\u0433\\\\u043e\\\\u0435\\\"]}]}\"'),(2,'Продуктовый опрос',0,'\"{\\\"questions\\\": [{\\\"title\\\": \\\"\\\\u0421\\\\u043a\\\\u043e\\\\u043b\\\\u044c\\\\u043a\\\\u043e \\\\u0432\\\\u044b \\\\u0438\\\\u0441\\\\u043f\\\\u043e\\\\u043b\\\\u044c\\\\u0437\\\\u0443\\\\u0435\\\\u0442\\\\u0435 \\\\u043d\\\\u0430\\\\u0448 \\\\u043f\\\\u0440\\\\u043e\\\\u0434\\\\u0443\\\\u043a\\\\u0442\\\", \\\"type\\\": \\\"radio\\\", \\\"isRequired\\\": false, \\\"answerOptions\\\": [\\\"< 1 \\\\u0433\\\\u043e\\\\u0434\\\\u0430\\\", \\\"1 - 2 \\\\u0433\\\\u043e\\\\u0434\\\\u0430\\\", \\\"> 2 \\\\u043b\\\\u0435\\\\u0442\\\"]}, {\\\"title\\\": \\\"\\\\u041c\\\\u043e\\\\u0436\\\\u043d\\\\u043e \\\\u043b\\\\u0438 \\\\u0441\\\\u0432\\\\u044f\\\\u0437\\\\u0430\\\\u0442\\\\u044c\\\\u0441\\\\u044f \\\\u0441 \\\\u0432\\\\u0430\\\\u043c\\\\u0438 \\\\u0434\\\\u043b\\\\u044f \\\\u0440\\\\u0430\\\\u0437\\\\u044a\\\\u044f\\\\u0441\\\\u043d\\\\u0435\\\\u043d\\\\u0438\\\\u044f \\\\u043e\\\\u0442\\\\u0432\\\\u0435\\\\u0442\\\\u043e\\\\u0432?\\\", \\\"type\\\": \\\"radio\\\", \\\"isRequired\\\": true, \\\"answerOptions\\\": [\\\"\\\\u0414\\\\u0430\\\", \\\"\\\\u041d\\\\u0435\\\\u0442\\\"]}, {\\\"title\\\": \\\"\\\\u0427\\\\u0442\\\\u043e \\\\u043d\\\\u0430\\\\u043c \\\\u0441\\\\u0442\\\\u043e\\\\u0438\\\\u0442 \\\\u0443\\\\u043b\\\\u0443\\\\u0447\\\\u0448\\\\u0438\\\\u0442\\\\u044c \\\\u0432 \\\\u043f\\\\u0435\\\\u0440\\\\u0432\\\\u0443\\\\u044e \\\\u043e\\\\u0447\\\\u0435\\\\u0440\\\\u0435\\\\u0434\\\\u044c?\\\", \\\"type\\\": \\\"checkbox\\\", \\\"isRequired\\\": true, \\\"answerOptions\\\": [\\\"\\\\u041f\\\\u0440\\\\u043e\\\\u0438\\\\u0437\\\\u0432\\\\u043e\\\\u0434\\\\u0438\\\\u0442\\\\u0435\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\\\u0441\\\\u0442\\\\u044c\\\", \\\"\\\\u0414\\\\u043e\\\\u0441\\\\u0442\\\\u0443\\\\u043f\\\\u043d\\\\u043e\\\\u0441\\\\u0442\\\\u044c\\\", \\\"\\\\u0421\\\\u043e\\\\u0432\\\\u043c\\\\u0435\\\\u0441\\\\u0442\\\\u0438\\\\u043c\\\\u043e\\\\u0441\\\\u0442\\\\u044c\\\", \\\"\\\\u0411\\\\u0435\\\\u0437\\\\u043e\\\\u043f\\\\u0430\\\\u0441\\\\u043d\\\\u043e\\\\u0441\\\\u0442\\\\u044c\\\"]}]}\"');
/*!40000 ALTER TABLE `surveys` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `survey_result_id` int(11) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `survey_result_id` (`survey_result_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`survey_result_id`) REFERENCES `survey_results` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','a@mail.ru','pbkdf2:sha256:260000$WTPrphTAm0FnoBeG$4d2bb71848f1bbdba1b2eb93030ada2ed91a348479ffb093aea7cf907e854388',1,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

