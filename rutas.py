import psycopg2

# conexion a base de datos
conn = psycopg2.connect(database="data_analytics", user="postgres", 
                        password="postgres", port="5432")


#endpoints de datos

museo_url="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv"


salacine_url="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/f7a8edb8-9208-41b0-8f19-d72811dcea97/download/cine.csv"
              


bib_url="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"
