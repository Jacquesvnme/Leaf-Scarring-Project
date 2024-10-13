CREATE TABLE ImageData(
	ImageData_ID SERIAL PRIMARY KEY,
	Image_ID Integer UNIQUE,
	ImageLable VARCHAR (100) UNIQUE,
	Lamina_Area DOUBLE PRECISION,
	Lamina_Length DOUBLE PRECISION,
	Lamina_Width DOUBLE PRECISION,
	Scar_Count Integer,
	Scar_Area DOUBLE PRECISION,
	DamagePercentage DOUBLE PRECISION,
	Petiole_Length DOUBLE PRECISION,
	CONSTRAINT fk_Images
		FOREIGN KEY(Image_ID)
			REFERENCES Images(Image_ID)
			ON DELETE CASCADE
);

CREATE TABLE Details(
	Details_ID Integer PRIMARY KEY,
	ImageLocation VARCHAR (100) ,
	ImageDate DATE
);

CREATE TABLE Images(
	Image_ID SERIAL PRIMARY KEY,
	Details_ID Integer UNIQUE,
	ImagePathBack VARCHAR (100)  UNIQUE,
	ImagePathFront VARCHAR (100) UNIQUE,
	CONSTRAINT fk_Details
		FOREIGN KEY(Details_ID)
			REFERENCES Details(Details_ID)
			ON DELETE CASCADE
);

INSERT INTO ImageData(ImageData_ID,Image_ID,ImageLable,Lamina_Area,Lamina_Length,Lamina_Width,Scar_Count,Scar_Area,DamagePercentage,Petiole_Length)
VALUES
	(1,1,'Image1',160,10,16,4,20,0.125,4),
	(2,2,'Image2',216,18,12,17,25,0.116,5),
	(3,3,'Image3',240,15,16,8,35,0.146,7),
	(4,4,'Image4',200,10,20,15,23,0.115,8),
	(5,5,'Image5',357,17,21,7,34,0.095,5);
	-- area,length & width are of cm & cm^2

INSERT INTO Images(Image_ID, Details_ID, ImagePathBack, ImagePathFront)
VALUES
	(1,1,'./image1_back.png','./image1_front.png'),
	(2,2,'./image2_back.png','./image2_front.png'),
	(3,3,'./image3_back.png','./image3_front.png'),
	(4,4,'./image4_back.png','./image4_front.png'),
	(5,5,'./image5_back.png','./image5_front.png');

INSERT INTO Details(Details_ID,ImageLocation,ImageDate)
VALUES
	(1,'Johannesburg','01/02/2024'),
	(2,'Cape Town','29/11/2023'),
	(3,'Ethekwini','15/05/2024'),
	(4,'Ekurhuleni','24/03/2024'),
	(5,'Tshwane','10/08/2024');