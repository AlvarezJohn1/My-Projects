-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 16, 2024 at 11:48 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `entrance_exam`
--

-- --------------------------------------------------------

--
-- Table structure for table `answer_log`
--

CREATE TABLE `answer_log` (
  `answer_id` int(11) NOT NULL,
  `exam_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `answer_value` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `course_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `course_id` int(11) NOT NULL,
  `course_name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`course_id`, `course_name`) VALUES
(2, 'Hotel Management'),
(3, 'Tourism'),
(4, 'Accountancy'),
(5, 'Business Administration');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `question_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `question` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`question_id`, `course_id`, `question`) VALUES
(5, 1, 'How well do you grasp the importance of data structures in programming?'),
(6, 1, 'Rate your familiarity with virtualization and its benefits.'),
(7, 2, 'How effective are you in ensuring excellent customer service in a hotel?'),
(8, 2, 'Rate your understanding of revenue management in the hotel industry.'),
(9, 2, 'How familiar are you with strategies to minimize food wastage in a hotel restaurant?'),
(11, 2, 'How skilled are you in handling guest complaints effectively?'),
(12, 3, 'How well do you understand the impact of sustainable tourism practices?'),
(14, 3, 'How confident are you in planning group tour itineraries?'),
(15, 3, 'Rate your knowledge of ecotourism and its importance.'),
(16, 3, 'How knowledgeable are you about ensuring the safety of tourists during travel?'),
(17, 4, 'Rate your understanding of accrual accounting.'),
(18, 4, 'How comfortable are you with calculating depreciation expense?'),
(19, 4, 'How familiar are you with the difference between financial and management accounting?'),
(21, 4, 'How confident are you in analyzing financial statements?'),
(22, 5, 'How well do you understand the functions of human resource management?'),
(23, 5, 'How familiar are you with different forms of business organization?'),
(24, 5, 'Rate your confidence in identifying key components of a marketing plan.'),
(25, 5, 'How well can you explain the concept of strategic management?'),
(26, 5, 'How proficient are you in evaluating financial performance using ratio analysis?');

-- --------------------------------------------------------

--
-- Table structure for table `result`
--

CREATE TABLE `result` (
  `result_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `course_name` text NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL,
  `account_type` varchar(255) NOT NULL,
  `first_name` varchar(250) DEFAULT NULL,
  `middle_name` varchar(250) DEFAULT NULL,
  `last_name` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `account_type`, `first_name`, `middle_name`, `last_name`) VALUES
(1, 'admin', 'admin', 'Admin', 'Harold', 'Delima', 'Jamisola'),
(2, 'dex', '123', 'User', 'Dexter', 'O', 'Alvarez'),
(21, 'afad', 'ad', 'User', 'adad', 'asdad', 'asd');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `answer_log`
--
ALTER TABLE `answer_log`
  ADD PRIMARY KEY (`answer_id`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`question_id`);

--
-- Indexes for table `result`
--
ALTER TABLE `result`
  ADD PRIMARY KEY (`result_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `answer_log`
--
ALTER TABLE `answer_log`
  MODIFY `answer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2348;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `course_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `result`
--
ALTER TABLE `result`
  MODIFY `result_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
