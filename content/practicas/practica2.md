---
title: "Práctica 2"
date: 2025-11-13
draft: false
---

## Conceptos de Programación Orientada a Objetos (POO)

Clase
Una clase es un molde o plantilla que define atributos (datos) y métodos (comportamientos).
 Ejemplo:

```py
class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
```

Objeto
Un objeto es una instancia concreta de una clase, es decir, algo real creado a partir del molde.

```py
libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez")
```

Herencia
La herencia permite crear nuevas clases basadas en otras, reutilizando código.

```py
class ItemBiblioteca:
    def __init__(self, id, titulo):
        self.id = id
        self.titulo = titulo

class Libro(ItemBiblioteca):
    def __init__(self, id, titulo, autor):
        super().__init__(id, titulo)
        self.autor = autor
```

Encapsulamiento
El encapsulamiento protege los datos internos de una clase y se accede a ellos mediante métodos controlados:

```py
class Usuario:
    def __init__(self, nombre):
        self.__nombre = nombre  # Atributo privado

    def get_nombre(self):
        return self.__nombre
```

Abstracción
La abstracción consiste en ocultar los detalles innecesarios y mostrar solo lo esencial.

```py
class ItemBiblioteca:
    def mostrar_info(self):
        raise NotImplementedError("Debe implementarse en la subclase")
```

Polimorfismo
El polimorfismo permite usar el mismo método con diferentes comportamientos dependiendo del objeto.

```py
items = [Libro(1, "1984", "Orwell"), Revista(2, "National Geographic", "Enero 2024")]
for item in items:
    item.mostrar_info()  # Cada clase ejecuta su propia versión
```

Comparación entre la versión en C y la versión en Python

Característica
Versión en C
Versión en Python (POO)
Estructura de datos
struct y listas enlazadas
Clases y objetos
Enlace entre datos
Punteros manuales (next)
Referencias automáticas
Gestión de memoria
Manual (malloc, free)
Automática (Garbage Collector)
Persistencia
Archivos de texto simples
Archivos JSON (más flexibles)
Escalabilidad
Limitada, código repetitivo
Alta, gracias a herencia y polimorfismo
Legibilidad
Procedimental y extensa
Clara y modular

Conclusiones
POO facilita la organización del código, separando responsabilidades y evitando duplicación.

Herencia y polimorfismo permiten extender funcionalidades fácilmente sin alterar código existente.

En Python, la memoria se maneja automáticamente, lo que reduce errores comunes del C.

La persistencia en JSON hace que los datos sean más fáciles de guardar, leer y compartir.

Este enfoque es más cercano al mundo real, donde los objetos (libros, usuarios) tienen comportamientos propios.

```py
import json
from abc import ABC, abstractmethod
```

## --- Clases base y herencia ---

```py
class ItemBiblioteca(ABC):
    """Clase abstracta que representa un ítem genérico."""
    def __init__(self, id, titulo, anio):
        self._id = id
        self._titulo = titulo
        self._anio = anio
        self._prestado = False

    @abstractmethod
    def mostrar_info(self):
        pass

    def prestar(self):
        if not self._prestado:
            self._prestado = True
            return True
        return False

    def devolver(self):
        if self._prestado:
            self._prestado = False
            return True
        return False

    def to_dict(self):
        return {
            "id": self._id,
            "titulo": self._titulo,
            "anio": self._anio,
            "prestado": self._prestado,
            "tipo": self.__class__.__name__
        }


class Libro(ItemBiblioteca):
    def __init__(self, id, titulo, anio, autor, genero):
        super().__init__(id, titulo, anio)
        self._autor = autor
        self._genero = genero

    def mostrar_info(self):
        print(f"[Libro] {self._titulo} - {self._autor} ({self._anio}) | Genero: {self._genero}")


class Revista(ItemBiblioteca):
    def __init__(self, id, titulo, anio, numero):
        super().__init__(id, titulo, anio)
        self._numero = numero

    def mostrar_info(self):
        print(f"[Revista] {self._titulo} - Numero {self._numero} ({self._anio})")


# --- Clase Usuario ---

class Usuario:
    def __init__(self, id, nombre):
        self._id = id
        self._nombre = nombre
        self._prestamos = []

    def prestar_item(self, item):
        if item.prestar():
            self._prestamos.append(item._id)
            print(f"Item '{item._titulo}' prestado a {self._nombre}.")
        else:
            print("El ítem ya está prestado.")

    def devolver_item(self, item):
        if item._id in self._prestamos and item.devolver():
            self._prestamos.remove(item._id)
            print(f"Item '{item._titulo}' devuelto por {self._nombre}.")
        else:
            print("No tiene este ítem prestado.")

    def to_dict(self):
        return {"id": self._id, "nombre": self._nombre, "prestamos": self._prestamos}


# --- Clase principal Biblioteca (gestor) ---

class Biblioteca:
    def __init__(self):
        self.items = []
        self.usuarios = []
        self.archivo_datos = "biblioteca.json"

    def registrar_item(self, item):
        self.items.append(item)
        print(f"Ítem '{item._titulo}' registrado correctamente.")

    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)
        print(f"Usuario '{usuario._nombre}' registrado correctamente.")

    def buscar_item(self, id):
        return next((i for i in self.items if i._id == id), None)

    def buscar_usuario(self, id):
        return next((u for u in self.usuarios if u._id == id), None)

    def mostrar_items(self):
        print("\n--- Ítems en biblioteca ---")
        for i in self.items:
            i.mostrar_info()

    def mostrar_usuarios(self):
        print("\n--- Usuarios registrados ---")
        for u in self.usuarios:
            print(f"ID: {u._id} | Nombre: {u._nombre} | Préstamos: {len(u._prestamos)}")

    def guardar(self):
        data = {
            "items": [i.to_dict() for i in self.items],
            "usuarios": [u.to_dict() for u in self.usuarios]
        }
        with open(self.archivo_datos, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Datos guardados correctamente en JSON.")

    def cargar(self):
        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                data = json.load(f)
                for i in data.get("items", []):
                    if i["tipo"] == "Libro":
                        item = Libro(i["id"], i["titulo"], i["anio"], "Desconocido", "General")
                    else:
                        item = Revista(i["id"], i["titulo"], i["anio"], "N/A")
                    item._prestado = i["prestado"]
                    self.items.append(item)
                for u in data.get("usuarios", []):
                    user = Usuario(u["id"], u["nombre"])
                    user._prestamos = u["prestamos"]
                    self.usuarios.append(user)
            print("Datos cargados desde JSON.")
        except FileNotFoundError:
            print("No existe archivo previo, iniciando base vacía.")
```

## --- Menú principal ---

```py
def main():
    biblio = Biblioteca()
    biblio.cargar()

    while True:
        print("\n--- MENÚ BIBLIOTECA ---")
        print("1. Registrar libro")
        print("2. Registrar revista")
        print("3. Registrar usuario")
        print("4. Mostrar ítems")
        print("5. Mostrar usuarios")
        print("6. Prestar ítem")
        print("7. Devolver ítem")
        print("8. Guardar y salir")

        op = input("Opción: ")

        if op == "1":
            id = int(input("ID: "))
            titulo = input("Título: ")
            anio = int(input("Año: "))
            autor = input("Autor: ")
            genero = input("Género: ")
            biblio.registrar_item(Libro(id, titulo, anio, autor, genero))
        elif op == "2":
            id = int(input("ID: "))
            titulo = input("Título: ")
            anio = int(input("Año: "))
            numero = input("Número de edición: ")
            biblio.registrar_item(Revista(id, titulo, anio, numero))
        elif op == "3":
            id = int(input("ID usuario: "))
            nombre = input("Nombre: ")
            biblio.registrar_usuario(Usuario(id, nombre))
        elif op == "4":
            biblio.mostrar_items()
        elif op == "5":
            biblio.mostrar_usuarios()
        elif op == "6":
            id_user = int(input("ID usuario: "))
            id_item = int(input("ID ítem: "))
            user = biblio.buscar_usuario(id_user)
            item = biblio.buscar_item(id_item)
            if user and item:
                user.prestar_item(item)
            else:
                print("Datos inválidos.")
        elif op == "7":
            id_user = int(input("ID usuario: "))
            id_item = int(input("ID ítem: "))
            user = biblio.buscar_usuario(id_user)
            item = biblio.buscar_item(id_item)
            if user and item:
                user.devolver_item(item)
            else:
                print("Datos inválidos.")
        elif op == "8":
            biblio.guardar()
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
```
