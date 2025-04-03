USE base;


CREATE TABLE slides (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    link_url VARCHAR(255),
    order_index INT NOT NULL
);

INSERT INTO slides (title, image_url, link_url, order_index) VALUES
('Slide 1', 'C:/Users/Vimal/OneDrive/Desktop/project/images/slide1.jpg', 'https://w0.peakpx.com/wallpaper/265/481/HD-wallpaper-nature.jpg', 1),
('Slide 2', 'C:/Users/Vimal/OneDrive/Desktop/project/images/slide2.jpg', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRBUydQONe0F9SEbxr3F0f-5fKmEPnX0iNJQ&s', 2),
('Slide 3', 'C:/Users/Vimal/OneDrive/Desktop/project/images/slide3.jpg', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfQmJJe7bY5cIFNHhDuiQQhezFJlwolDYxow&s', 3)