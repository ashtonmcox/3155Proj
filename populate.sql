-- Users Table Data
INSERT INTO users (name, email, phone_number, address) VALUES
('John Doe', 'johndoe@example.com', '1234567890', '123 Elm Street'),
('Jane Smith', 'janesmith@example.com', '0987654321', '456 Oak Avenue'),
('Michael Johnson', 'michaelj@example.com', '1122334455', '789 Pine Road');

INSERT INTO resources (name, type, amount, unit) VALUES
('Tomato', 'Vegetable', 50.00, 'kg'),
('Chicken Breast', 'Meat', 20.00, 'kg'),
('Olive Oil', 'Oil', 10.00, 'liters'),
('Cheese', 'Dairy', 15.00, 'kg'),
('Lettuce', 'Vegetable', 15.00, 'kg');

-- MenuItemRecipe Table Data
INSERT INTO recipes (name, price, category, dietary_category, description, instructions, preparation_time, servings, calories) VALUES
('Grilled Chicken Salad', 12.99, 'Salad', 'Gluten Free', 'A healthy salad with grilled chicken breast, lettuce, tomatoes, and dressing.', 'Grill the chicken and assemble the salad with fresh ingredients.', '15 minutes', 2, 350),
('Cheese Pizza', 8.99, 'Pizza', '', 'A classic pizza topped with mozzarella cheese and tomato sauce.', 'Prepare dough, spread sauce, and top with cheese, then bake.', '20 minutes', 1, 600);

-- RecipeIngredients Table Data
-- Mapping of recipes to their resources with quantities
INSERT INTO recipe_ingredients (recipe_id, resource_id, quantity) VALUES
(1, 2, 0.25), -- Grilled Chicken Salad uses 0.25 kg of Chicken Breast
(1, 5, 0.02), -- Grilled Chicken Salad uses 0.02 kg of Lettuce
(1, 1, 0.10), -- Grilled Chicken Salad uses 0.10 kg of Tomato
(2, 4, 0.20), -- Cheese Pizza uses 0.20 kg of Cheese
(2, 1, 0.10); -- Cheese Pizza uses 0.10 kg of Tomato

-- Promotions Table Data
INSERT INTO promotions (promotion_code, description, expiration_date, discount_percent) VALUES
('SAVE10', '10% off on orders above $30', '2024-12-31', 10.00),
('FREESHIP', 'Free shipping on all orders', '2024-12-31', 5.00);

-- Orders Table Data
INSERT INTO orders (user_id, status, date, tracking_number, total_price, order_type) VALUES
(1, 'Completed', '2024-12-01 13:00:00', '12345', 25.98, "delivery"),
(2, 'Pending', '2024-12-02 14:30:00', '12346', 18.99, "takeout"),
(3, 'Completed', '2024-12-03 19:00:00', '12347', 20.99, "takeout");

-- OrderDetails Table Data
INSERT INTO order_details (order_id, menu_item_id, quantity) VALUES
(1, 1, 1),
(1, 2, 1),
(2, 1, 1),
(3, 2, 1);

-- Payments Table Data
INSERT INTO payments (order_id, card_information, transaction_status, payment_type) VALUES
(1, '4111111111111111', 'Success', 'Credit Card'),
(2, '5500000000000004', 'Pending', 'Debit Card'),
(3, '6011514445555550', 'Success', 'Credit Card');

-- Feedback Table Data
INSERT INTO feedback (user_id, content, order_id, score) VALUES
(1, 'Great meal, will order again!', 1, 5),
(2, 'Food was good but delivery was late.', 2, 3),
(3, 'Tasty food, but a little too salty for my taste.', 3, 4);