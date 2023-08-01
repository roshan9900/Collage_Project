-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 24, 2023 at 11:57 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES
(1, 'roshan', '1234', 'roshan@gmail.com'),
(3, 'karthik', '567', 'karthik@gmail.com'),
(4, 'pawan', '123', 'pawan@gmail.com'),
(5, 'shubham', '1234', 'shubham@gmail.com'),
(7, 'pratham', '123', 'pratham@gmail.com'),
(9, 'deepak', '12', 'deepak@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', '123');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `symbol` varchar(20) DEFAULT NULL,
  `action` varchar(20) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `total_cost` float DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `symbol`, `action`, `quantity`, `price`, `total_cost`, `user_id`, `username`) VALUES
(1, 'bhartiartl.ns', 'buy', 4, '766.50', 3066, 1, 'roshan'),
(2, 'bhartiartl.ns', 'sell', -2, '766.50', 1533, 1, 'roshan'),
(3, 'bhartiartl.ns', 'buy', 5, '767.05', 3835.25, 1, 'admin'),
(4, 'bhartiartl.ns', 'sell', -3, '767.05', 2301.15, 1, 'admin'),
(5, 'ASHOKLEY.NS', 'buy', 34, '138.00', 4692, 1, 'roshan'),
(6, 'RELAXO.NS', 'buy', 53, '815.05', 43197.6, 1, 'admin'),
(7, 'bhartiartl.ns', 'buy', 43, '767.05', 32983.1, 1, 'roshan'),
(8, 'bhartiartl.ns', 'buy', 34, '767.05', 26079.7, 2, 'karthik'),
(9, 'bhartiartl.ns', 'sell', -23, '767.05', 17642.2, 2, 'karthik'),
(10, 'bhartiartl.ns', 'buy', 35, '759.65', 26587.8, 1, 'admin'),
(11, 'relaxo.ns', 'buy', 65, '808.35', 52542.8, 1, 'admin'),
(12, 'bhartiartl.ns', 'buy', 54, '759.65', 41021.1, 1, 'admin'),
(13, 'bhartiartl.ns', 'sell', -40, '759.65', 30386, 1, 'roshan'),
(14, 'relaxo.ns', 'buy', 43, '826.20', 35526.6, 1, 'admin'),
(15, 'BHARTIARTL.NS', 'buy', 38, '765.20', 29077.6, 5, 'shubham'),
(16, 'BHARTIARTL.NS', 'buy', 23, '765.20', 17599.6, 5, 'shubham'),
(17, 'BHARTIARTL.NS', 'sell', -23, '765.20', 17599.6, 5, 'shubham'),
(18, 'AAPL', 'buy', 20, '165.02', 3300.4, 1, 'admin'),
(19, 'GOOG', 'buy', 39, '105.91', 4130.49, 1, 'admin'),
(20, 'AMZN', 'buy', 43, '106.96', 4599.28, 1, 'admin'),
(21, 'aapl', 'buy', 43, '165.02', 7095.86, 1, 'roshan'),
(22, 'goog', 'buy', 56, '105.91', 5930.96, 1, 'roshan'),
(23, 'goog', 'buy', 23, '105.91', 2435.93, 1, 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
