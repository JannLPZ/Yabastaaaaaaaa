from .entities.Autor import Autor
from .entities.Libro import Libro
from .entities.libroC import LibroC

class ModeloLibro():
    @classmethod
    def listar_libros(self,db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT LIB.isbn, LIB.titulo, LIB.anoedicion, LIB.precio,
                    AUT.apellidos, AUT.nombres
                    FROM libro LIB JOIN autor AUT ON LIB.autor_id = AUT.id 
                    ORDER BY LIB.titulo ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            libros=[]
            for row in data:
                aut=Autor(0, row[4], row[5])
                lib=Libro(row[0],row[1],aut,row[2],row[3])
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)
        


    @classmethod
    def lista_libros(self,db):
        try:
            cursor = db.connection.cursor()
            cursor.callproc('obtener_libros')
            cursor.execute( 'SELECT * FROM vistalibros;')
            data = cursor.fetchall()

            
            librosc=[]
            for row in data:
                lib=LibroC(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                librosc.append(lib)
            return librosc
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def leer_libro(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT isbn, titulo, anoedicion, precio
                    FROM libro WHERE isbn = '{0}'""".format(isbn)
            cursor.execute(sql)
            data= cursor.fetchone()
            libro=Libro(data[0],data[1], None, data[2], data[3])
            return libro
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def listar_libros_vendidos(self,db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT COM.libro_isbn, LIB.titulo, LIB.precio,
                    COUNT(COM.libro_isbn) AS Unidades_Vendidas 
                    FROM compra COM JOIN libro LIB ON COM.libro_isbn = LIB.isbn
                    GROUP BY COM.libro_isbn ORDER BY 4 DESC, 2 ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            libros=[]
            for row in data:
                lib=Libro(row[0],row[1],None, None,row[2])
                lib.unidades_vendidas=int(row[3])
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)
        


    @classmethod
    def registrar(self, db, isbn,titulo,autor,anoedicion,precio,descripcion,filename):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO libro (isbn, titulo, autor_id, anoedicion, precio, descripcion, imagen_portada) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (isbn, titulo, autor, anoedicion, precio, descripcion, filename))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def edit(self,db,isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT * FROM libro WHERE isbn = %s"""
            cursor.execute(sql, (isbn,))
            libro = cursor.fetchone()
            if libro:
                return libro  # Devuelve la tupla del libro encontrado
            return None  # Si no se encuentra el libro, retorna None
        except Exception as ex:
            raise Exception(f"Error al cargar el libro: {str(ex)}")


    @classmethod
    def actualizarCON(self, db, isbn,titulo,autor,anoedicion,precio,descripcion,filename):
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE libro SET titulo = %s, autor_id= %s, anoedicion=%s, precio=%s, descripcion = %s, imagen_portada=%s WHERE isbn = %s """
            cursor.execute(sql, (titulo, autor, anoedicion, precio, descripcion, filename, isbn))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def actualizarSIN(self, db, isbn,titulo,autor,anoedicion,precio,descripcion):
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE libro SET titulo = %s, autor_id= %s, anoedicion=%s, precio=%s, descripcion = %s WHERE isbn = %s """
            cursor.execute(sql, (titulo, autor, anoedicion, precio, descripcion, isbn))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def borrarlibro(self, db, isbn):
        try:
        

            cursor = db.connection.cursor()
            sql = """DELETE FROM libro WHERE isbn = %s"""
            cursor.execute(sql, (isbn,))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)