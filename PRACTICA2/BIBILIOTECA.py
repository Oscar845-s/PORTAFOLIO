import os

class Genre:
    FICTION = 0
    NON_FICTION = 1
    SCIENCE = 2
    HISTORY = 3
    FANTASY = 4
    BIOGRAPHY = 5
    OTHER = 6

    names = {
        FICTION: "Ficcion",
        NON_FICTION: "No Ficcion",
        SCIENCE: "Ciencia",
        HISTORY: "Historia",
        FANTASY: "Fantasia",
        BIOGRAPHY: "Biografia",
        OTHER: "Otro"
    }

    @staticmethod
    def to_string(genre):
        return Genre.names.get(genre, "Desconocido")

    @staticmethod
    def from_string(text):
        for k, v in Genre.names.items():
            if v.lower() == text.lower():
                return k
        return Genre.OTHER


class Book:
    def __init__(self, book_id, title, author, year, genre, quantity):
        self.id = book_id
        self.title = title
        self.author = author
        self.publication_year = year
        self.genre = genre
        self.quantity = quantity

    def __str__(self):
        return (f"ID: {self.id}\nTitulo: {self.title}\nAutor: {self.author}\n"
                f"Ano: {self.publication_year}\nGenero: {Genre.to_string(self.genre)}\n"
                f"Cantidad: {self.quantity}")


class Member:
    def __init__(self, member_id, name):
        self.id = member_id
        self.name = name
        self.issued_books = []

    def __str__(self):
        return f"ID: {self.id}\nNombre: {self.name}\nLibros prestados: {len(self.issued_books)}"


class LibrarySystem:
    def __init__(self):
        self.books = []
        self.members = []

    # --- Manejo de libros ---
    def add_book(self):
        book_id = int(input("Ingresa ID del libro: "))
        title = input("Ingresa titulo del libro: ")
        author = input("Ingresa nombre del autor: ")
        year = int(input("Ingresa el ano de publicacion: "))
        genre = int(input("Ingresa el genero (0:FIC,1:NF,2:SCI,3:HIS,4:FAN,5:BIO,6:OTRO): "))
        quantity = int(input("Ingresa la cantidad de libros: "))

        book = Book(book_id, title, author, year, genre, quantity)
        self.books.append(book)
        print("\nLibro agregado exitosamente!\n")

    def display_books(self):
        if not self.books:
            print("\nNo hay libros disponibles.\n")
            return
        print("\nLibros disponibles en la biblioteca:\n")
        for book in self.books:
            print(book)
            print("-" * 30)

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    # --- Manejo de miembros ---
    def add_member(self):
        member_id = int(input("Ingresa el ID del miembro: "))
        name = input("Ingresa el nombre del miembro: ")
        member = Member(member_id, name)
        self.members.append(member)
        print("\nMiembro agregado exitosamente!\n")

    def display_members(self):
        if not self.members:
            print("\nNo hay miembros disponibles.\n")
            return
        print("\nMiembros registrados en la biblioteca:\n")
        for member in self.members:
            print(member)
            for book_id in member.issued_books:
                book = self.find_book_by_id(book_id)
                if book:
                    print(f"  -> {book.title} ({book.author})")
            print("-" * 30)

    def search_member(self):
        member_id = int(input("Ingresa el ID del miembro: "))
        for member in self.members:
            if member.id == member_id:
                print(member)
                for book_id in member.issued_books:
                    book = self.find_book_by_id(book_id)
                    if book:
                        print(f"  -> {book.title} ({book.author})")
                return
        print("\nMiembro no encontrado.\n")

    # --- Préstamos ---
    def issue_book(self):
        member_id = int(input("Ingresa el ID del miembro: "))
        book_id = int(input("Ingresa el ID del libro: "))

        member = next((m for m in self.members if m.id == member_id), None)
        book = self.find_book_by_id(book_id)

        if member and book and book.quantity > 0:
            member.issued_books.append(book_id)
            book.quantity -= 1
            print("\nLibro prestado satisfactoriamente!\n")
        else:
            print("\nNo se pudo prestar (verifica disponibilidad y datos).\n")

    def return_book(self):
        member_id = int(input("Ingresa el ID del miembro: "))
        book_id = int(input("Ingresa el ID del libro: "))

        member = next((m for m in self.members if m.id == member_id), None)
        book = self.find_book_by_id(book_id)

        if member and book_id in member.issued_books:
            member.issued_books.remove(book_id)
            book.quantity += 1
            print("\nLibro devuelto satisfactoriamente!\n")
        else:
            print("\nNo se pudo devolver (verifica datos).\n")

    # --- Archivos ---
    def save_to_files(self):
        with open("library.txt", "w", encoding="utf-8") as f:
            for book in self.books:
                f.write(f"{book.id}\n{book.title}\n{book.author}\n{book.publication_year}\n"
                        f"{Genre.to_string(book.genre)}\n{book.quantity}\n")

        with open("members.txt", "w", encoding="utf-8") as f:
            for member in self.members:
                f.write(f"{member.id}\n{member.name}\n{len(member.issued_books)}\n")
                for b in member.issued_books:
                    f.write(f"{b}\n")

    def load_from_files(self):
        if os.path.exists("library.txt"):
            with open("library.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
                for i in range(0, len(lines), 6):
                    try:
                        book_id = int(lines[i])
                        title = lines[i+1]
                        author = lines[i+2]
                        year = int(lines[i+3])
                        genre = Genre.from_string(lines[i+4])
                        quantity = int(lines[i+5])
                        self.books.append(Book(book_id, title, author, year, genre, quantity))
                    except:
                        pass

        if os.path.exists("members.txt"):
            with open("members.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
                idx = 0
                while idx < len(lines):
                    member_id = int(lines[idx]); idx += 1
                    name = lines[idx]; idx += 1
                    issued_count = int(lines[idx]); idx += 1
                    issued_books = []
                    for _ in range(issued_count):
                        issued_books.append(int(lines[idx])); idx += 1
                    member = Member(member_id, name)
                    member.issued_books = issued_books
                    self.members.append(member)


def main():
    system = LibrarySystem()
    system.load_from_files()

    while True:
        print("\n--- Sistema de Biblioteca ---")
        print("1. Agregar libro")
        print("2. Mostrar libros")
        print("3. Agregar miembro")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Mostrar miembros")
        print("7. Buscar miembro")
        print("8. Guardar y salir")

        choice = input("Opcion: ")
        if choice == "1":
            system.add_book()
        elif choice == "2":
            system.display_books()
        elif choice == "3":
            system.add_member()
        elif choice == "4":
            system.issue_book()
        elif choice == "5":
            system.return_book()
        elif choice == "6":
            system.display_members()
        elif choice == "7":
            system.search_member()
        elif choice == "8":
            system.save_to_files()
            print("Datos guardados. Saliendo...")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
