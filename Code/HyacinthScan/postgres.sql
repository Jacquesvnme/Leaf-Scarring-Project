-- This is used to create tables for the database
-- Designed to work with PostgreSQL

CREATE TABLE Details(
	Details_ID Integer PRIMARY KEY,
	ImageLocation VARCHAR (100) ,
	ImageDate DATE
);

CREATE TABLE Images(
	Image_ID SERIAL PRIMARY KEY,
	Details_ID Integer UNIQUE,
	ImagePath VARCHAR (100)  UNIQUE
);

CREATE TABLE ImageData(
	ImageData_ID SERIAL PRIMARY KEY,
	Image_ID Integer UNIQUE,
	ImageLable VARCHAR (100) UNIQUE,
	Lamina_Area DOUBLE PRECISION,
	Lamina_Length DOUBLE PRECISION,
	Lamina_Width DOUBLE PRECISION,
	Scar_Count Integer,
	Scar_Area DOUBLE PRECISION,
	DamagePercentage DOUBLE PRECISION
);

ALTER TABLE Images
ADD CONSTRAINT fk_Details FOREIGN KEY(Details_ID) REFERENCES Details(Details_ID) ON DELETE CASCADE;

ALTER TABLE ImageData
ADD CONSTRAINT fk_Images FOREIGN KEY(Image_ID) REFERENCES Images(Image_ID) ON DELETE CASCADE;

INSERT INTO Details(Details_ID,ImageLocation,ImageDate)
VALUES
	(1,'Johannesburg','2024-02-01'),
	(2,'Cape Town','2023-11-29'),
	(3,'Ethekwini','2024-05-15'),
	(4,'Ekurhuleni','2024-03-24'),
	(5,'Tshwane','2024-08-10'),
	(6,'Benoni','2024-09-26');

INSERT INTO Images(Image_ID, Details_ID, ImagePath)
VALUES
	(1,1,'./image1.png'),
	(2,2,'./image2.png'),
	(3,3,'./image3.png'),
	(4,4,'./image4.png'),
	(5,5,'./image5.png'),
	(6,6,'./image6.png');

INSERT INTO ImageData(ImageData_ID,Image_ID,ImageLable,Lamina_Area,Lamina_Length,Lamina_Width,Scar_Count,Scar_Area,DamagePercentage)
VALUES
	(1,1,'Image1_front',160,10,16,4,20,0.125),
	(2,2,'Image1_back',216,18,12,17,25,0.116),
	(3,3,'Image2_front',240,15,16,8,35,0.146),
	(4,4,'Image2_back',200,10,20,15,23,0.115),
	(5,5,'Image3_front',357,17,21,7,34,0.095),
	(6,6,'Image3_back',330,18,27,5,39,0.057);
	-- area,length & width are of cm & cm^2

-- For testing purposes only
CREATE VIEW viewData
AS
	SELECT imagedata_id, imagelocation, imagedate,
			imagepath, imagelable, lamina_area, lamina_length,
			lamina_width, scar_count, scar_area, damagepercentage
		FROM public.details
			FULL JOIN public.images ON public.details.details_id = public.images.details_id
			FULL JOIN public.imagedata ON public.images.image_id = public.imagedata.image_id;

SELECT * FROM viewData