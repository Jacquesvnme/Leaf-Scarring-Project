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
	ImagePath VARCHAR (100) UNIQUE
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

CREATE VIEW viewData
AS
	SELECT imagedata_id, imagelocation, imagedate,
			imagepath, imagelable, lamina_area, lamina_length,
			lamina_width, scar_count, scar_area, damagepercentage
		FROM public.details
			FULL JOIN public.images ON public.details.details_id = public.images.details_id
			FULL JOIN public.imagedata ON public.images.image_id = public.imagedata.image_id;

SELECT * FROM viewData

INSERT INTO Details(Details_ID,ImageLocation,ImageDate)
VALUES
	(1,'Nothing','2024-02-01'),

INSERT INTO Images(Image_ID, Details_ID, ImagePath)
VALUES
	(1,1,'./DummyImage.png'),

INSERT INTO ImageData(ImageData_ID,Image_ID,ImageLable,Lamina_Area,Lamina_Length,Lamina_Width,Scar_Count,Scar_Area,DamagePercentage)
VALUES
	(1,1,'DummyImage',1,1,1,1,1,0.001)
	-- area,length & width are of cm & cm^2