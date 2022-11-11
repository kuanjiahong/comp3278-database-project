-- MySQL dump 10.13  Distrib 8.0.30, for macos12 (x86_64)
--
-- Host: localhost    Database: comp3278
-- ------------------------------------------------------
-- Server version	8.0.30

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

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add course',1,'add_course'),(2,'Can change course',1,'change_course'),(3,'Can delete course',1,'delete_course'),(4,'Can view course',1,'view_course'),(5,'Can add staff',2,'add_staff'),(6,'Can change staff',2,'change_staff'),(7,'Can delete staff',2,'delete_staff'),(8,'Can view staff',2,'view_staff'),(9,'Can add teaching',3,'add_teaching'),(10,'Can change teaching',3,'change_teaching'),(11,'Can delete teaching',3,'delete_teaching'),(12,'Can view teaching',3,'view_teaching'),(13,'Can add class',4,'add_class'),(14,'Can change class',4,'change_class'),(15,'Can delete class',4,'delete_class'),(16,'Can view class',4,'view_class'),(17,'Can add enrolment',5,'add_enrolment'),(18,'Can change enrolment',5,'change_enrolment'),(19,'Can delete enrolment',5,'delete_enrolment'),(20,'Can view enrolment',5,'view_enrolment'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add log entry',7,'add_logentry'),(26,'Can change log entry',7,'change_logentry'),(27,'Can delete log entry',7,'delete_logentry'),(28,'Can view log entry',7,'view_logentry'),(29,'Can add permission',8,'add_permission'),(30,'Can change permission',8,'change_permission'),(31,'Can delete permission',8,'delete_permission'),(32,'Can view permission',8,'view_permission'),(33,'Can add group',9,'add_group'),(34,'Can change group',9,'change_group'),(35,'Can delete group',9,'delete_group'),(36,'Can view group',9,'view_group'),(37,'Can add content type',10,'add_contenttype'),(38,'Can change content type',10,'change_contenttype'),(39,'Can delete content type',10,'delete_contenttype'),(40,'Can view content type',10,'view_contenttype'),(41,'Can add session',11,'add_session'),(42,'Can change session',11,'change_session'),(43,'Can delete session',11,'delete_session'),(44,'Can view session',11,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'admin','logentry'),(9,'auth','group'),(8,'auth','permission'),(10,'contenttypes','contenttype'),(4,'schedule','class'),(1,'schedule','course'),(5,'schedule','enrolment'),(2,'schedule','staff'),(3,'schedule','teaching'),(11,'sessions','session'),(6,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'schedule','0001_initial','2022-11-11 16:15:38.913407'),(2,'contenttypes','0001_initial','2022-11-11 16:15:38.929965'),(3,'contenttypes','0002_remove_content_type_name','2022-11-11 16:15:38.957029'),(4,'auth','0001_initial','2022-11-11 16:15:39.048126'),(5,'auth','0002_alter_permission_name_max_length','2022-11-11 16:15:39.070532'),(6,'auth','0003_alter_user_email_max_length','2022-11-11 16:15:39.077014'),(7,'auth','0004_alter_user_username_opts','2022-11-11 16:15:39.084149'),(8,'auth','0005_alter_user_last_login_null','2022-11-11 16:15:39.090885'),(9,'auth','0006_require_contenttypes_0002','2022-11-11 16:15:39.093596'),(10,'auth','0007_alter_validators_add_error_messages','2022-11-11 16:15:39.100630'),(11,'auth','0008_alter_user_username_max_length','2022-11-11 16:15:39.106946'),(12,'auth','0009_alter_user_last_name_max_length','2022-11-11 16:15:39.115040'),(13,'auth','0010_alter_group_name_max_length','2022-11-11 16:15:39.129176'),(14,'auth','0011_update_proxy_permissions','2022-11-11 16:15:39.139401'),(15,'auth','0012_alter_user_first_name_max_length','2022-11-11 16:15:39.146927'),(16,'users','0001_initial','2022-11-11 16:15:39.309405'),(17,'admin','0001_initial','2022-11-11 16:15:39.365397'),(18,'admin','0002_logentry_remove_auto_add','2022-11-11 16:15:39.373029'),(19,'admin','0003_logentry_add_action_flag_choices','2022-11-11 16:15:39.381339'),(20,'schedule','0002_enrolment_course_students','2022-11-11 16:15:39.446132'),(21,'schedule','0003_alter_class_class_day_alter_class_zoom_link','2022-11-11 16:15:39.458774'),(22,'sessions','0001_initial','2022-11-11 16:15:39.475284'),(23,'users','0002_alter_user_managers','2022-11-11 16:15:39.487036'),(24,'users','0003_remove_user_courses','2022-11-11 16:15:39.506675'),(25,'users','0004_alter_user_email','2022-11-11 16:15:39.540674');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('jjeq0q6kvdvu2fcml26ut713fwuohsc8','.eJxVjEEOwiAQRe_C2jQDrVDc6cIDeAEyMwxCTGgi7cp4dyXpQpfv___-SwXc1hy2Js9Qojopow6_GSE_pPaiYxt2Hq7IchNe7rWsZannr3DZp39-xpb764iMIhMlZ9m66Glyhv0IaKJm8IJsZuMkibNEGsgjzQkENBwRiNX7A-DjOLM:1otWiZ:zdSNfU-Sa5OkxZdHtkcJu-YZCmCbkX6q7t_KqxEcdc4','2022-11-25 16:17:23.977546');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_class`
--

DROP TABLE IF EXISTS `schedule_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule_class` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `class_id` int NOT NULL,
  `location` varchar(100) NOT NULL,
  `class_day` varchar(3) NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `class_type` varchar(1) NOT NULL,
  `zoom_link` varchar(200) NOT NULL,
  `teacher_message` varchar(1000) NOT NULL,
  `course_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `schedule_class_course_id_class_id_66799124_uniq` (`course_id`,`class_id`),
  CONSTRAINT `schedule_class_course_id_422e370d_fk_schedule_course_id` FOREIGN KEY (`course_id`) REFERENCES `schedule_course` (`id`),
  CONSTRAINT `valid_start_end_time` CHECK ((`start_time` < `end_time`))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_class`
--

LOCK TABLES `schedule_class` WRITE;
/*!40000 ALTER TABLE `schedule_class` DISABLE KEYS */;
INSERT INTO `schedule_class` VALUES (1,1,'MWT2','1','14:30:00.000000','15:20:00.000000','L','https://hku.zoom.us/j/96226740999?pwd=ZER1UUdxSVVhQzNXbXFkUDd3WjRBdz09','',1),(2,2,'MWT2','4','13:30:00.000000','15:20:00.000000','L','https://hku.zoom.us/j/96226740999?pwd=ZER1UUdxSVVhQzNXbXFkUDd3WjRBdz09','',1),(3,1,'CPD-LG.18','1','15:30:00.000000','17:20:00.000000','L','https://hku.zoom.us/j/3869089913','',2),(4,2,'CPD-LG.18','5','15:30:00.000000','17:20:00.000000','L','https://hku.zoom.us/j/3869089913','lab on every Friday',2),(5,1,'CPD-LG.01','2','10:30:00.000000','12:20:00.000000','L','','',3),(6,2,'CPD-LG.01','4','10:30:00.000000','12:20:00.000000','L','','',3),(7,1,'CYPP2','2','09:30:00.000000','10:20:00.000000','T','','',4),(8,2,'CYPP2','5','09:30:00.000000','11:20:00.000000','L','','',4),(9,1,'MB167','2','13:30:00.000000','15:20:00.000000','L','https://hku.zoom.us/j/97158080302?pwd=NWViaUw1V3FYT1Y4NWxsT0ZXWENBUT09','',5),(10,2,'MB167','5','14:30:00.000000','15:20:00.000000','T','https://hku.zoom.us/j/94959382241?pwd=ZHJVaXIxS1pZSEEyOEtNK3g5Sys5UT09','',5),(11,1,'CPD-G.03','2','10:30:00.000000','12:20:00.000000','L','','',6),(12,2,'CPD-G.03','5','11:30:00.000000','12:20:00.000000','L','','',6);
/*!40000 ALTER TABLE `schedule_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_course`
--

DROP TABLE IF EXISTS `schedule_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule_course` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `offered` tinyint(1) NOT NULL,
  `moodle_link` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_course`
--

LOCK TABLES `schedule_course` WRITE;
/*!40000 ALTER TABLE `schedule_course` DISABLE KEYS */;
INSERT INTO `schedule_course` VALUES (1,'COMP3278_1A','Introduction to database management systems',1,'https://moodle.hku.hk/course/view.php?id=96513'),(2,'COMP3322_1A','Modern Technologies on World Wide Web',1,'https://moodle.hku.hk/course/view.php?id=96523'),(3,'COMP3230_1A','Principles of Operating Systems',1,'https://moodle.hku.hk/course/view.php?id=96625'),(4,'COMP3297_1A','Software Engineering',1,'https://moodle.hku.hk/course/view.php?id=96515'),(5,'COMP3258_1A','Functional Programming',1,'https://moodle.hku.hk/course/view.php?id=96637'),(6,'CAES9542_1F','Technical English for Computer Science',1,'https://moodle.hku.hk/course/view.php?id=100843');
/*!40000 ALTER TABLE `schedule_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_enrolment`
--

DROP TABLE IF EXISTS `schedule_enrolment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule_enrolment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `course_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schedule_enrolment_course_id_1911c4d5_fk_schedule_course_id` (`course_id`),
  KEY `schedule_enrolment_student_id_7024ab50_fk_users_user_id` (`student_id`),
  CONSTRAINT `schedule_enrolment_course_id_1911c4d5_fk_schedule_course_id` FOREIGN KEY (`course_id`) REFERENCES `schedule_course` (`id`),
  CONSTRAINT `schedule_enrolment_student_id_7024ab50_fk_users_user_id` FOREIGN KEY (`student_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_enrolment`
--

LOCK TABLES `schedule_enrolment` WRITE;
/*!40000 ALTER TABLE `schedule_enrolment` DISABLE KEYS */;
INSERT INTO `schedule_enrolment` VALUES (1,1,2),(2,1,3),(3,2,3),(4,3,3),(5,4,3),(6,6,2),(7,5,2);
/*!40000 ALTER TABLE `schedule_enrolment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_staff`
--

DROP TABLE IF EXISTS `schedule_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule_staff` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_staff`
--

LOCK TABLES `schedule_staff` WRITE;
/*!40000 ALTER TABLE `schedule_staff` DISABLE KEYS */;
INSERT INTO `schedule_staff` VALUES (1,'Ping Luo'),(2,'Yao Mu'),(3,'Yao Lai'),(4,'Yizhou Li'),(5,'Xiaoyang Zhao'),(6,'Shiwei Zhang'),(7,'Leo Yeung'),(8,'Chenshu Wu'),(9,'Chuan Wu'),(10,'Bruno Oliveira'),(11,'Xu Xue'),(12,'Mable Choi');
/*!40000 ALTER TABLE `schedule_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_teaching`
--

DROP TABLE IF EXISTS `schedule_teaching`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule_teaching` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(1) NOT NULL,
  `course_id` bigint NOT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schedule_teaching_course_id_eea830ca_fk_schedule_course_id` (`course_id`),
  KEY `schedule_teaching_staff_id_fe4b8ee3_fk_schedule_staff_id` (`staff_id`),
  CONSTRAINT `schedule_teaching_course_id_eea830ca_fk_schedule_course_id` FOREIGN KEY (`course_id`) REFERENCES `schedule_course` (`id`),
  CONSTRAINT `schedule_teaching_staff_id_fe4b8ee3_fk_schedule_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `schedule_staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_teaching`
--

LOCK TABLES `schedule_teaching` WRITE;
/*!40000 ALTER TABLE `schedule_teaching` DISABLE KEYS */;
INSERT INTO `schedule_teaching` VALUES (1,'L',1,1),(2,'T',1,2),(3,'T',1,3),(4,'T',1,4),(5,'T',2,5),(6,'T',2,6),(7,'L',2,9),(8,'L',3,8),(9,'L',4,7),(10,'L',6,12),(11,'L',5,10),(12,'T',5,11);
/*!40000 ALTER TABLE `schedule_teaching` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'pbkdf2_sha256$390000$YB4vgqYNKvmCI5UrpRBj4Y$Noe12WjYSL3J9CcO+PxK6P2ys2JWjbTP3UWuWvCnxfo=','2022-11-11 16:17:01.698112',1,'','',1,1,'2022-10-10 10:32:10.772000','admin@cs.hku.hk'),(2,'pbkdf2_sha256$390000$Kyv8QwYFECxtKigic8xfIs$/gHPVCzrL9T+wPlpiJy7OJqXywQiLNAkv7j8Odd/lG8=','2022-11-11 16:17:23.976077',0,'','',0,1,'2022-10-10 10:43:00.788000','huanpham@connect.hku.hk'),(3,'pbkdf2_sha256$390000$mbyOFcRfSTQw3zO5fcF5Uo$MvcQHSUCDTzteIsqrp+7HlsRLI1qjt2SGjSlRTHX9Tw=','2022-11-11 15:50:03.701000',0,'','',0,1,'2022-11-11 15:17:28.405000','benwu013@connect.hku.hk');
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_groups`
--

DROP TABLE IF EXISTS `users_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_user_permissions`
--

DROP TABLE IF EXISTS `users_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-12  0:19:39
