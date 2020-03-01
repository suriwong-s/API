CREATE TABLE estimate_input (
   certificat_id VARCHAR(50) UNIQUE NOT NULL PRIMARY KEY,
   shape VARCHAR (20),
   color VARCHAR (5) NOT NULL,
   sizes DECIMAL(4,2) NOT NULL,
   clarity  VARCHAR (20) NOT NULL
);

CREATE TABLE estimate_output (
   id SERIAL PRIMARY KEY,
   shape VARCHAR (20),
   low_size DECIMAL(4,2) NOT NULL,
   high_size DECIMAL(4,2) NOT NULL,
   color VARCHAR (5) NOT NULL,
   clarity  VARCHAR (20) NOT NULL,
   caratprice INTEGER NOT NULL,
   date DATE NOT NULL,
   certificat_id VARCHAR (50)
);


INSERT INTO estimate_input (certificat_id, shape, color, sizes, clarity, created_at)
VALUES
    ('AB3344556700', 'round', 'E', 2.10,'VS2', NULL);
  