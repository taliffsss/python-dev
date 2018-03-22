-- phpMyAdmin SQL Dump
-- version 4.7.8
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 22, 2018 at 10:13 AM
-- Server version: 10.1.30-MariaDB
-- PHP Version: 7.2.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `python`
--

-- --------------------------------------------------------

--
-- Table structure for table `py_loggedin_activity`
--

CREATE TABLE `py_loggedin_activity` (
  `id` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `loggedin` datetime DEFAULT NULL,
  `loggedout` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `py_loggedin_activity`
--

INSERT INTO `py_loggedin_activity` (`id`, `userid`, `loggedin`, `loggedout`) VALUES
(1, 2, '2018-03-15 14:19:56', '2018-03-15 14:19:56'),
(2, 1, '2018-03-16 12:04:08', '2018-03-16 12:06:54'),
(3, 1, '2018-03-16 12:20:52', '2018-03-16 12:20:52'),
(4, 1, '2018-03-16 12:30:45', '2018-03-16 12:30:45'),
(5, 1, '2018-03-16 12:33:29', '2018-03-16 12:33:29'),
(6, 1, '2018-03-16 14:42:49', '2018-03-16 15:56:42'),
(7, 1, '2018-03-16 15:56:42', '2018-03-16 15:56:42'),
(8, 1, '2018-03-16 15:56:42', '2018-03-16 15:56:42'),
(9, 1, '2018-03-16 15:58:50', '2018-03-22 13:01:50'),
(10, 1, '2018-03-19 09:27:52', '2018-03-22 13:01:50'),
(11, 1, '2018-03-22 08:52:25', '2018-03-22 13:01:50');

-- --------------------------------------------------------

--
-- Table structure for table `py_role`
--

CREATE TABLE `py_role` (
  `roleid` int(11) NOT NULL,
  `rolename` varchar(20) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `py_role`
--

INSERT INTO `py_role` (`roleid`, `rolename`, `description`) VALUES
(1, 'super admin', NULL),
(2, 'admin', NULL),
(3, 'web master', NULL),
(4, 'moderator', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `uid` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `username`, `firstname`, `lastname`, `password`, `email`, `role`, `address`, `date_created`, `update_at`) VALUES
(1, 'taliffsss', 'Mark Anthony', 'Naluz', '$5$rounds=535000$NASH.mWwwExEajTX$PMQ8S92opW6ChOzQEgX9Omy7/3.9v/.2L0yxxJpM3j8', 'anthony.naluz15@gmail.com', 1, NULL, '2018-03-16 11:51:52', NULL),
(2, 'sean', 'Mark Christian', 'Naluz', '$5$rounds=535000$PyaEbmMLauhWbY5q$GS./bMdUTFYfwR7.16D/K1Cr51Ov2Mcoa8C3mh1iDI7', 'aglipaync@gmail.com', 2, '0', '2018-03-16 14:13:41', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `py_loggedin_activity`
--
ALTER TABLE `py_loggedin_activity`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `py_role`
--
ALTER TABLE `py_role`
  ADD PRIMARY KEY (`roleid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `py_loggedin_activity`
--
ALTER TABLE `py_loggedin_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `py_role`
--
ALTER TABLE `py_role`
  MODIFY `roleid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
