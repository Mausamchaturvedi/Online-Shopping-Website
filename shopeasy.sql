-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 26, 2026 at 11:00 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `shopeasy`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `product_id`, `quantity`) VALUES
(1, 1, 3, 1),
(14, 4, 4, 1),
(15, 4, 3, 1),
(16, 4, 2, 1),
(27, 9, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `category_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `category_name`) VALUES
(1, 'Electronics'),
(2, 'Fashion'),
(3, 'Books'),
(4, 'Sports'),
(5, 'Accessories'),
(6, 'Home & Kitchen'),
(7, 'Beauty & Personal Care'),
(8, 'Sports & Fitness'),
(9, 'Grocery'),
(10, 'Footwear'),
(11, 'Jewellery'),
(12, 'Toys'),
(13, 'Mobiles'),
(14, 'Laptop'),
(15, 'Furniture');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(50) DEFAULT 'Pending',
  `payment_method` varchar(30) DEFAULT NULL,
  `payment_status` varchar(30) NOT NULL DEFAULT 'Pending',
  `razorpay_order_id` varchar(100) DEFAULT NULL,
  `razorpay_payment_id` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `total_amount`, `order_date`, `status`, `payment_method`, `payment_status`, `razorpay_order_id`, `razorpay_payment_id`) VALUES
(1, 1, 3000.00, '2026-10-02 12:01:08', 'Pending', NULL, 'Pending', NULL, NULL),
(2, 2, 450000.00, '2026-10-02 21:03:02', 'Pending', NULL, 'Pending', NULL, NULL),
(3, 2, 900000.00, '2026-10-02 21:07:42', 'Pending', NULL, 'Pending', NULL, NULL),
(4, 2, 935000.00, '2026-10-02 21:12:45', 'Pending', NULL, 'Pending', NULL, NULL),
(5, 4, 928000.00, '2026-10-03 19:26:22', 'Delivered', NULL, 'Pending', NULL, NULL),
(6, 4, 25000.00, '2026-10-03 19:26:39', 'Processing', NULL, 'Pending', NULL, NULL),
(7, 4, 5000.00, '2026-10-03 20:22:16', 'Pending', NULL, 'Pending', NULL, NULL),
(8, 4, 8000.00, '2026-10-03 20:27:07', 'Pending', NULL, 'Pending', NULL, NULL),
(9, 4, 8000.00, '2026-10-03 20:55:10', 'Pending', NULL, 'Pending', NULL, NULL),
(10, 4, 33000.00, '2026-10-03 20:55:33', 'Pending', NULL, 'Pending', NULL, NULL),
(11, 8, 450000.00, '2026-10-26 11:48:35', 'Pending', 'Razorpay', 'Pending', 'order_TsWdg0Zvk4Bde6', NULL),
(12, 8, 450000.00, '2026-10-26 11:51:34', 'Pending', 'COD', 'Pending', NULL, NULL),
(13, 8, 450000.00, '2026-10-26 11:51:59', 'Pending', 'COD', 'Pending', NULL, NULL),
(14, 8, 450000.00, '2026-10-26 11:54:36', 'Pending', 'COD', 'Pending', NULL, NULL),
(15, 8, 450000.00, '2026-10-26 12:03:35', 'Pending', 'COD', 'Pending', NULL, NULL),
(16, 5, 450000.00, '2026-10-26 13:55:43', 'Pending', NULL, 'Pending', NULL, NULL),
(17, 8, 1350000.00, '2026-10-26 14:05:56', 'Pending', NULL, 'Pending', NULL, NULL),
(18, 8, 3175000.00, '2026-10-26 14:39:03', 'Pending', 'COD', 'Pending', NULL, NULL),
(19, 8, 950499.00, '2026-10-26 19:51:29', 'Pending', 'COD', 'Pending', NULL, NULL),
(20, 10, 450000.00, '2026-10-26 19:52:40', 'Pending', 'Razorpay', 'Pending', 'order_Tset1clqF5uM3Y', NULL),
(21, 10, 450000.00, '2026-10-26 19:54:19', 'Pending', 'COD', 'Pending', NULL, NULL),
(22, 10, 475000.00, '2026-10-26 19:55:08', 'Pending', 'COD', 'Pending', NULL, NULL),
(23, 10, 25000.00, '2026-10-26 19:56:29', 'Pending', 'Razorpay', 'Pending', 'order_Tsex21kNMfpVMO', NULL),
(24, 10, 25000.00, '2026-10-26 19:57:53', 'Pending', 'Razorpay', 'Pending', 'order_TseyWdeBw6WXSV', NULL),
(25, 10, 2499.00, '2026-10-26 21:57:17', 'Pending', 'Razorpay', 'Pending', 'order_Tsh0f4Ly2Ra3qb', NULL),
(26, 10, 2499.00, '2026-10-26 21:57:25', 'Pending', 'COD', 'Pending', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`, `price`) VALUES
(1, 3, 1, 1, 450000.00),
(2, 3, 1, 1, 450000.00),
(3, 4, 2, 1, 25000.00),
(4, 4, 1, 1, 450000.00),
(5, 4, 1, 1, 450000.00),
(6, 4, 4, 1, 5000.00),
(7, 4, 4, 1, 5000.00),
(8, 5, 1, 1, 450000.00),
(9, 5, 1, 1, 450000.00),
(10, 5, 2, 1, 25000.00),
(11, 5, 3, 1, 3000.00),
(12, 6, 2, 1, 25000.00),
(14, 9, 4, 1, 5000.00),
(16, 11, 1, 1, 450000.00),
(17, 12, 1, 1, 450000.00),
(18, 13, 1, 1, 450000.00),
(19, 14, 1, 1, 450000.00),
(20, 15, 1, 1, 450000.00),
(21, 16, 1, 1, 450000.00),
(22, 17, 1, 1, 450000.00),
(23, 17, 1, 1, 450000.00),
(24, 17, 1, 1, 450000.00),
(25, 18, 1, 1, 450000.00),
(26, 18, 1, 1, 450000.00),
(27, 18, 1, 1, 450000.00),
(28, 18, 1, 1, 450000.00),
(29, 18, 1, 1, 450000.00),
(30, 18, 1, 1, 450000.00),
(31, 18, 1, 1, 450000.00),
(32, 18, 2, 1, 25000.00),
(33, 19, 1, 1, 450000.00),
(34, 19, 1, 1, 450000.00),
(35, 19, 2, 1, 25000.00),
(36, 19, 5, 1, 499.00),
(37, 19, 2, 1, 25000.00),
(38, 20, 1, 1, 450000.00),
(39, 21, 1, 1, 450000.00),
(40, 22, 2, 1, 25000.00),
(41, 22, 1, 1, 450000.00),
(42, 23, 2, 1, 25000.00),
(43, 24, 2, 1, 25000.00),
(44, 25, 1317, 1, 2499.00),
(45, 26, 1317, 1, 2499.00);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `image`, `stock`, `category_id`) VALUES
(1, 'Laptop', 'A versatile HP laptop suitable for programming, office applications, online classes, web browsing and everyday productivity.', 85000.00, 'laptop.jpg', 50, 1),
(2, 'Mobile', 'A modern IPHONE smartphone designed for everyday communication, social media, photography, video streaming and mobile applications.', 98000.00, 'mobile.jpg', 80, 1),
(3, 'Headphones', 'Enjoy music, podcasts, videos and calls with these stylish headphones designed for comfortable everyday listening.', 3000.00, 'headphone.jpg', 0, 1),
(4, 'Smart Watch', 'A stylish boAt smartwatch for everyday wear. Features depend on the specific model and may include activity tracking and notifications.', 5000.00, 'watch.jpg', 90, 1),
(5, 'Mouse', 'A practical computer mouse for smooth navigation, browsing, office work and study. Suitable for desktop and laptop users.', 499.00, 'mouse.jpg', 110, 1),
(1306, 'Classic Mens Blazer', 'Elegant formal blazer suitable for office wear, meetings and special occasions.', 2499.00, 'blazer.jpg', 15, 2),
(1307, 'Premium Formal Blazer', 'A smart formal blazer designed for professional events and stylish occasions.', 2999.00, 'blazer (2).jpg', 12, 2),
(1308, 'BassPro Headphones', 'Over-ear headphones designed for comfortable listening and everyday entertainment.', 1799.00, 'headphone (2).jpg', 25, 1),
(1309, 'Wireless Headphones Plus', 'Modern headphones for music, calls and daily use.', 1999.00, 'headphone (3).jpg', 20, 1),
(1310, 'Classic Casual Jacket', 'Versatile casual jacket suitable for everyday wear and outings.', 1499.00, 'jacket.jpg', 18, 2),
(1311, 'Premium Winter Jacket', 'A stylish jacket suitable for cool-weather outings and everyday use.', 1999.00, 'jacket (2).jpg', 15, 2),
(1312, 'ProBook Laptop', 'Laptop designed for studying, office work, browsing and everyday computing.', 52999.00, 'laptop (2).jpg', 10, 14),
(1313, 'Nova Smartphone', 'Smartphone suitable for everyday communication, apps and entertainment.', 19999.00, 'smartphone.jpg', 20, 13),
(1314, 'Casual Mens Shirt', 'A versatile shirt suitable for everyday wear and casual occasions.', 799.00, 'shirt.jpg', 30, 2),
(1315, 'Classic Cotton T-Shirt', 'Comfortable everyday T-shirt with a simple and versatile design.', 499.00, 'tshirt.jpg', 40, 2),
(1316, 'Sport Running Shoes', 'Sports shoes suitable for daily activities, walking and exercise.', 1499.00, 'shoes (2).jpg', 20, 10),
(1317, 'Fitness Smartwatch', 'Smartwatch designed to complement an active lifestyle and daily routines.', 2499.00, 'smartwatch (2).jpg', 17, 8),
(1318, 'Studio Bass Headphones', 'Over-ear headphones for music, video calls and everyday listening.', 2199.00, 'headphone (4).jpg', 20, 1),
(1319, 'Comfort Sound Headphones', 'Comfort-focused headphones for studying, working and enjoying music.', 1899.00, 'headphone (5).jpg', 18, 1),
(1320, 'Premium Audio Headphones', 'Stylish headphones suitable for entertainment and daily audio use.', 2499.00, 'headphone (6).jpg', 15, 1),
(1321, 'Urban Style Jacket', 'A versatile jacket for casual outfits and everyday outings.', 1699.00, 'jacket (3).jpg', 15, 2),
(1322, 'Modern Classic Jacket', 'A modern casual jacket designed to complement everyday clothing.', 1899.00, 'jacket (4).jpg', 12, 2),
(1323, 'Student Series Laptop', 'A laptop suited to study, presentations, programming and office tasks.', 42999.00, 'laptop (3).jpg', 8, 14),
(1324, 'Everyday Pro Laptop', 'A versatile laptop for productivity, web browsing and entertainment.', 48999.00, 'laptop (4).jpg', 7, 14),
(1325, 'Performance Laptop', 'A laptop for everyday computing, multitasking and professional work.', 55999.00, 'laptop (5).jpg', 6, 14),
(1326, 'Nova Smartphone Plus', 'A modern smartphone for communication, apps and everyday entertainment.', 21999.00, 'smartphone (2).jpg', 15, 13),
(1327, 'Smartphone Pro Edition', 'A stylish smartphone suitable for daily use and mobile applications.', 24999.00, 'smartphone (3).jpg', 12, 13),
(1328, 'Smartphone Max', 'A versatile smartphone for calls, browsing, photography and streaming.', 27999.00, 'smartphone (4).jpg', 10, 13),
(1329, 'Active Smartwatch', 'A smartwatch for everyday wear and an active lifestyle.', 2299.00, 'smartwatch (3).jpg', 18, 8),
(1330, 'Smartwatch Pro', 'A modern smartwatch with a versatile design for daily routines.', 2999.00, 'smartwatch (4).jpg', 15, 8),
(1331, 'Smartwatch Elite', 'A stylish smartwatch for everyday use and fitness-related activities.', 3499.00, 'smartwatch (5).jpg', 12, 8),
(1332, 'Casual Shirt Edition 2', 'A versatile casual shirt suitable for everyday wear and outings.', 899.00, 'shirt (2).jpg', 25, 2),
(1333, 'Comfort Sneakers', 'Casual shoes suitable for daily activities and relaxed outings.', 1399.00, 'shoes (3).jpg', 20, 10),
(1334, 'Active Sports Shoes', 'Sports-inspired footwear for everyday activities and exercise.', 1599.00, 'shoes (4).jpg', 18, 10),
(1335, 'Classic Walking Shoes', 'Everyday footwear designed for walking and casual use.', 1299.00, 'shoes (5).jpg', 22, 10),
(1336, 'Urban Sneakers', 'Modern sneakers suitable for casual outfits and daily wear.', 1799.00, 'shoes (6).jpg', 16, 10),
(1337, 'Sport Flex Shoes', 'Versatile sports shoes for daily activities and active routines.', 1999.00, 'shoes (7).jpg', 14, 10),
(1338, 'Cotton T-Shirt Edition 3', 'A comfortable T-shirt suitable for casual outfits and everyday wear.', 549.00, 'tshirt (3).jpg', 30, 2),
(1339, 'Classic T-Shirt Edition 4', 'An easy-to-style T-shirt for daily use and relaxed occasions.', 599.00, 'tshirt (4).jpg', 25, 2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(1, 'mausam', 'mausam40@gmail.com', '1234'),
(2, 'mausam', 'mausam@gmail.com', '$2b$12$gJdwB5s47Ch1PLCzR4Q50ujDueUI6yuBfl3LsHygX3zZmJ8.Vdf2S'),
(4, 'mausam', 'mausam4@gmail.com', '$2b$12$iThYmzaPOlVy.79N4zAk9.VuJJShFu/Oh0wimPglEKY6205aL7LOe'),
(5, 'Mausam Chaturvedi', 'mausamchaturvedi40@gmail.com', '$2b$12$EgVkSNDjhBqVw74wYPICQuDITpSnYjiEFnuV2H60dbF1RIh/zgaAG'),
(6, 'samarth', 'samarth@gmail.com', '$2b$12$D6lAF8fCvxUrarzl/vc4YObB5pP6p0l0lp29aWPKjGcx7EZgN9q7K'),
(8, 'mausam', 'mausam42@gmail.com', '$2b$12$o6vDQR3BMpARotmAzq36au6fOGINg8eA0nTGo3TYRWaRkbvO3QqWq'),
(9, 'mausam', 'mausam20@gmail.com', '$2b$12$Yn7uH8Zwa/tI.49zYLRwdOBJAYlZSDq9xzGGIQlzz69rGMsTZNlU6'),
(10, 'varsha', 'varsha@gmail.com', '$2b$12$cjfjHWDr5ySLypgZiJBTVOz7te/c5sEmZombq8soxdQM4eD34B.iS');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_category` (`category_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1340;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
