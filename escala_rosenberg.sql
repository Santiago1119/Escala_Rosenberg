-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 12-02-2023 a las 02:56:39
-- Versión del servidor: 5.7.36
-- Versión de PHP: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `escala_rosenberg`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `patient`
--

DROP TABLE IF EXISTS `patient`;
CREATE TABLE IF NOT EXISTS `patient` (
  `id_patient` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) DEFAULT NULL,
  `id_resultado` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_patient`),
  KEY `FK_score` (`id_resultado`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `patient`
--

INSERT INTO `patient` (`id_patient`, `name`, `id_resultado`) VALUES
(2, 'Juanito Juarez', 3),
(6, 'Allison Mitchell', 1),
(8, 'Brayan Andres', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `score_table_rosenberg`
--

DROP TABLE IF EXISTS `score_table_rosenberg`;
CREATE TABLE IF NOT EXISTS `score_table_rosenberg` (
  `id_resultado` int(11) NOT NULL,
  `resultado` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_resultado`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `score_table_rosenberg`
--

INSERT INTO `score_table_rosenberg` (`id_resultado`, `resultado`) VALUES
(1, 'autoestima elevada'),
(2, 'autoestima media'),
(3, 'autoestima baja');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `patient`
--
ALTER TABLE `patient`
  ADD CONSTRAINT `FK_score` FOREIGN KEY (`id_resultado`) REFERENCES `score_table_rosenberg` (`id_resultado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
