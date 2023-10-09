from carro_compra import CarroCompras
class Libro:
    def __init__(self, isbn, titulo, precio, existencias):
        self.isbn = isbn
        self.titulo = titulo
        self.precio = precio
        self.existencias = existencias

class LibroError(Exception):
    pass

class LibroExistenteError(LibroError):
    def __init__(self, titulo, isbn):
        message = f"El libro con título {titulo} y ISBN {isbn} ya existe en el catálogo"
        super().__init__(message)

class LibroAgotadoError(LibroError):
    def __init__(self, titulo, isbn):
        message = f"El libro con título {titulo} y ISBN {isbn} está agotado"
        super().__init__(message)

class ExistenciasInsuficientesError(LibroError):
    def __init__(self, titulo, isbn, cantidad_a_comprar, existencias):
        message = f"El libro con título {titulo} y ISBN {isbn} no tiene suficientes existencias para realizar la compra: cantidad a comprar: {cantidad_a_comprar}, existencias: {existencias}"
        super().__init__(message)

class TiendaLibros:
    def __init__(self):
        self.catalogo = {}
        self.carrito = CarroCompras()

    def adicionar_libro_a_catalogo(self, isbn, titulo, precio, existencias):
        if isbn in self.catalogo:
            raise LibroExistenteError(titulo, isbn)
        libro = Libro(isbn, titulo, precio, existencias)
        self.catalogo[isbn] = libro
        return libro

    def agregar_libro_a_carrito(self, isbn, cantidad):
        if isbn not in self.catalogo:
            raise LibroError(f"El libro con ISBN {isbn} no existe en el catálogo")
        libro = self.catalogo[isbn]
        if libro.existencias == 0:
            raise LibroAgotadoError(libro.titulo, isbn)
        if cantidad > libro.existencias:
            raise ExistenciasInsuficientesError(libro.titulo, isbn, cantidad, libro.existencias)

        self.carrito.agregar_item(libro, cantidad)

    def retirar_item_de_carrito(self, isbn):
        self.carrito.quitar_item(isbn)

class UIConsola:
    def retirar_libro_de_carrito_de_compras(self, tienda_libros):
        isbn = input("Ingrese el ISBN del libro que desea retirar del carrito: ")
        try:
            tienda_libros.retirar_item_de_carrito(isbn)
            print("El libro se retiró del carrito con éxito.")
        except LibroError as e:
            print(f"Error: {e}")

    def agregar_libro_a_carrito_de_compras(self, tienda_libros):
        isbn = input("Ingrese el ISBN del libro que desea agregar al carrito: ")
        cantidad = int(input("Ingrese la cantidad de unidades: "))
        try:
            tienda_libros.agregar_libro_a_carrito(isbn, cantidad)
            print("El libro se agregó al carrito con éxito.")
        except LibroError as e:
            print(f"Error: {e}")

    def adicionar_un_libro_a_catalogo(self, tienda_libros):
        isbn = input("Ingrese el ISBN del libro: ")
        titulo = input("Ingrese el título del libro: ")
        precio = float(input("Ingrese el precio del libro: "))
        existencias = int(input("Ingrese las existencias del libro: "))
        try:
            tienda_libros.adicionar_libro_a_catalogo(isbn, titulo, precio, existencias)
            print("El libro se agregó al catálogo con éxito.")
        except LibroError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    tienda = TiendaLibros()
    consola = UIConsola()

    while True:
        print("1. Agregar libro al carrito")
        print("2. Retirar libro del carrito")
        print("3. Adicionar libro al catálogo")
        print("4. Calcular total del carrito")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            consola.agregar_libro_a_carrito_de_compras(tienda)
        elif opcion == "2":
            consola.retirar_libro_de_carrito_de_compras(tienda)
        elif opcion == "3":
            consola.adicionar_un_libro_a_catalogo(tienda)
        elif opcion == "4":
            total = tienda.carrito.calcular_total()
            print(f"Total del carrito: {total}")
        elif opcion == "5":
            break