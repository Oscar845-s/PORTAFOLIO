---
title: "Práctica 1"
date: 2025-11-13
draft: false
---

## REPORTE PRACTICA 1

## INGENIERIA EN SOFTWARE Y TECNOLOGIAS EMERGENTES

### PARADIGMAS DE LA PROGRAMACION

### Elementos básicos de los lenguajes de programación

### OSCAR ARMANDO MEDINA GUTIERREZ 376020

### PROF CARLOS GALLEGOS

---

## OBJETIVO

El objetivo de esta práctica es identificar los elementos fundamentales de los lenguajes de programación: nombres, marcos de activación, bloques de alcance, administración de memoria, expresiones, comandos, control de secuencia como lo es; selección, iteración y recursión, subprogramas, y tipos de datos

## DESARROLLO

### 1.NOMBRES

En C, un nombre o identificador es una etiqueta que el programador asigna a un elemento del código, como una variable, una función, un tipo de dato, o una constante, para poder referenciarlo y usarlo fácilmente a lo largo del programa.

En todo el codigo existen diversos nombres que van desde

```c
 book_t *library = NULL;
    member_t *members = NULL;
    int bookCount = 0, memberCount = 0;
    int choice = 0;
```

siendo estos para declarar los nombres de las variables entero y de tipo book_t y member_t.

O otras como serian

```c
void displayBooksRecursive(book_t *library);
void displayBooks(book_t *library);
```

Siendo estas para nombres de funciones que se pueden identificar facilmente por el hecho de que llevan una palabra clave antes como pueden ser

```c
int
float
char
void
```

Entre otros.

### 2.MARCOS DE ACTIVACION

Un marco de activación (también conocido como activation record o stack frame) es una estructura de datos que se coloca en la pila de ejecución (runtime stack) cada vez que se llama a un subprograma (función, procedimiento o método).

Los marcos de activacion generalmente incluyen:

- **Direccion de retorno** Es donde el programa debe de continuar cuando termine la funcion
- **Parametros** Los valores que la funcion recibio al ser llamada
- **Variables locales** Las que se crean dentro del subprograma
- **Espacio Temporal** Para resultados parciales de expresiones
- **Enlace Dinamico/Estatico** Para manejar bloques de alcance y funciones anidadas

Un ejemplo en el programa seria:

```c
void displayMembers(member_t *members, book_t *library) {
    if (!members) {
        printf("\nNo hay miembros disponibles.\n");
        return;
    }

    member_t *current = members;
    printf("\nMiembros disponibles en biblioteca:\n");
    while (current) {
        printf("\nID miembro: %d\nNombre: %s\nCantidad de libros prestados: %d\n",
            current->id, current->name, current->issued_count);
        for (int i = 0; i < current->issued_count; i++) {
            book_t *book = findBookById(library, current->issued_books[i]);
            if (book) {
                printf("  Libro ID: %d\n  Titulo: %s\n  Autor: %s\n", book->id, book->title, book->author);
            }
        }
        current = current->next;
    }
    displayMemoryUsage();
}
```

En este caso cuando el programa entra a displayMembers, en la pila de ejecución se crea un marco con:

- Parametros
  - Members
  - library
- Variables locales
  - current
  - el indice i dentro del for
  - el puntero book dentro del for
- Direccion de retorno

En este caso la direccion de retorno es:

```c
case 6:
    displayMembers(members, library);
    break;
```

Que se encuentra en la funcion main

Dentro de la funcion displaymembers ocurren otras llamadas internas creando marcos adicionales

siendo las funciones

```c
findBookById(library, current->issued_books[i]);
displayMemoryUsage()
```

Todas las funciones generan un marco de activación al ser llamadas.

En el caso de la funcion displayMembers tiene su propio marco de activacion y dentro de ella se generan marcos adicionales cuando se llama a findBookById y displayMemoryUsage.

### 3.BLOQUES DE ALCANCE

Un bloque de alcance (scope block) es la región del programa en la que un nombre (una variable, función, constante, etc.) es visible y accesible.

#### Tipos de alcance en C

1. Alcance global
   - Se declara en cualquier funcion
   - La variable se puede usar en todo el archivo

```c
static int static_var = 0;

int bss_var;
```

Estas dos varibles son accecibles desde todo el proyecto

1. Alcance local
    - Se declara dentro de una funcion o bloque
    - Solo existe y es accesible mientras el bloque se esté ejecutando.

```c
void searchMember(member_t *members, book_t *library) {
    int memberID;
    printf("\nIngresa el ID del miembro: ");
    scanf("%d", &memberID);

    member_t *current = members;
    while (current) {
        if (current->id == memberID) {
            printf("\nID miembro: %d\nNombre: %s\nCantidad de libros prestados: %d\n",
                current->id, current->name, current->issued_count);
            for (int i = 0; i < current->issued_count; i++) {
                book_t *book = findBookById(library, current->issued_books[i]);
                if (book) {
                    printf("  Libro ID: %d\n  Titulo: %s\n  Autor: %s\n", book->id, book->title, book->author);
                }
            }
            displayMemoryUsage();
            return;
        }
        current = current->next;
    }
    printf("\nMiembro no encontrado.\n");
    displayMemoryUsage();
}
```

En este caso las variables memberID,i,*book y otras solo se pueden usar dentro de la funcion y no otras

1. Alcance de bloque anidado
    - Dentro de un bloque {} se puede declarar una variable que oculta otra con el mismo nombre en un nivel superior.

```c
void displayMembers(member_t *members, book_t *library) {
    member_t *current = members;  // alcance: toda la función
    while (current) {
        for (int i = 0; i < current->issued_count; i++) {
            book_t *book = findBookById(library, current->issued_books[i]);
            if (book) {
                printf("Titulo: %s\n", book->title);
            }
        }
        current = current->next;
    }
}
```

las variables members, library y current tienen alcance local de la función.

mientras que I tiene alcance dentro del for

book tiene alcance solo en el if y for

Cuando la funcion termina todas las variables dejan de existir

### 4.ADMINISTRACION DE MEMORIA

La adminstacion de memorias es el proceso de reservar, usar y liberar memoria durante la ejecución de un programa.

En c se organizan la mayoria en los siguientes tipos:

1. Memoria estática (o global):
   1. Para variables globales y variables estáticas.
   2. Se reserva al iniciar el programa y se libera solo cuando termina.

Ejemplo

```c
int contador = 0; // memoria global
static int total; // también se guarda en memoria estática
```

1. Memoria de pila (stack):
   1. Para parámetros de funciones y variables locales.
   2. Se reserva automáticamente al entrar en un bloque de alcance y se libera al salir.

Ejemplo

```c
void funcion() {
    int x = 10; // en la pila
} // aquí x desaparece
```

1. Memoria dinámica (heap):
   1. Se gestiona manualmente con malloc, calloc, realloc y free.
   2. Tú decides cuándo reservar y cuándo liberar.

Ejemplo

```c
int *arr = malloc(5 * sizeof(int)); // reservado en heap
// ... usar arr ...
free(arr); // liberar memoria
```

```c
void displayMembers(member_t *members, book_t *library) {
    member_t *current = members;  
    while (current) {
        for (int i = 0; i < current->issued_count; i++) {
            book_t *book = findBookById(library, current->issued_books[i]);
            if (book) {
                printf("  Libro ID: %d\n  Titulo: %s\n  Autor: %s\n",
                        book->id, book->title, book->author);
            }
        }
        current = current->next;
    }
    displayMemoryUsage();
}
```

En esta funcion podemos observar lo siguiente

- members, library, current, i, book → viven en la pila (stack), porque son parámetros y variables locales.

- Los nodos de member_t y book_t fueron creados con malloc → ellos viven en el heap, hasta que se llame a free.

- displayMemoryUsage() Te muestra cuánta memoria está en uso en ese momento.

Por ultimo es importante Liberar la memoria cuando no lo necesites para evitar fugas de memoria

### 5.EXPRESIONES

Una expresión es una combinación de operadores (como +, -, *, &&, ==), operandos (variables, constantes, literales) y a veces llamadas a funciones, que produce un valor.

#### Tipos de expresiones en c

1. Artimeticas

```c
int x = 5 + 3;      // suma
int y = x * 2;      // multiplicación
int z = y % 3;      // residuo
```

1. Relacionales

```c
if (x > y) { ... }  // "x es mayor que y"
```

1. Logicas

```c
if (x > 0 && y < 10) { ... }  // AND lógico
```

1. Asignacion

```c
total = x + y;  // asignación
```

1. De punteros

```c
int *ptr = &x;   // dirección de x
int val = *ptr;  // valor apuntado por ptr
```

1. De funcion

```c
int len = strlen("Hola");  // devuelve 4
```

Ejemplo

```c
while (current) {                     // expresión lógica (evaluar si current != NULL)
    printf("\nID miembro: %d\n", 
           current->id);              // acceso a estructura → expresión de puntero

    for (int i = 0; i < current->issued_count; i++) {  
        // i < current->issued_count → expresión relacional
        book_t *book = findBookById(library, current->issued_books[i]);
        // llamada a función → expresión de función
        // current->issued_books[i] → expresión de índice en arreglo

        if (book) {                   // expresión lógica (book != NULL)
            printf("Titulo: %s\n", book->title);  
        }
    }
    current = current->next;          // expresión de asignación con puntero
}
```

En la práctica:

- Las expresiones aritméticas aparecen poco (ejemplo: i++).

- Las expresiones lógicas y relacionales se usan en while, for, if.

- Las expresiones de punteros están en current->id, current->next, book->title.

- Las expresiones de función aparecen en llamadas como findBookById(...) y displayMemoryUsage().

### 6.COMANDOS

En el contexto de los lenguajes de programación, un comando (también llamado sentencia o statement) es una instrucción completa que el programa ejecuta.

#### Tipos de comandos en c

1. Comandos de expresión

Una expresión seguida de ;, que realiza algo.

```c
x = x + 1;         // asignación
funcion();         // llamada a función
```

1. Comandos de selección (control condicional)

if, if...else, switch.

```c
if (x > 0) {
    printf("positivo");
} else {
    printf("no positivo");
}
```

1. Comandos de iteración (bucles)

for, while, do...while.

```c
for (int i = 0; i < 5; i++) {
    printf("%d\n", i);
}
```

1. Comandos de salto

break, continue, return.

```c
return 0;
```

1. Comandos compuestos (bloques)

Un conjunto de comandos encerrados entre { ... }.

```c
{
    int a = 5;
    int b = 10;
    printf("%d\n", a+b);
}
```

Ejemplo

```c
void displayMembers(member_t *members, book_t *library) {
    if (!members) {                               // comando de selección
        printf("\nNo hay miembros disponibles.\n"); // comando de expresión (llamada a función)
        return;                                   // comando de salto
    }

    member_t *current = members;                  // comando de expresión (asignación)
    printf("\nMiembros disponibles en biblioteca:\n"); // comando de expresión

    while (current) {                             // comando de iteración (while)
        printf("\nID miembro: %d\nNombre: %s\nCantidad de libros prestados: %d\n",
            current->id, current->name, current->issued_count); // comando de expresión

        for (int i = 0; i < current->issued_count; i++) {        // comando de iteración (for)
            book_t *book = findBookById(library, current->issued_books[i]); // comando de expresión
            if (book) {                         // comando de selección (if)
                printf("  Libro ID: %d\n  Titulo: %s\n  Autor: %s\n", 
                        book->id, book->title, book->author);    // comando de expresión
            }
        }
        current = current->next;                // comando de expresión
    }

    displayMemoryUsage();                       // comando de expresión
}
```

En la práctica, los comandos que más aparecen son:

- De expresión: asignaciones, llamadas a funciones, incrementos (i++).

- De selección: if (decidir si hay miembros, si existe un libro).

- De iteración: while y for (recorrer la lista y los libros).

- De salto: return (salida temprana de la función).

- Compuestos: los bloques { ... } que agrupan instrucciones.

### 7.CONTROL DE SECUENCIAS

Los controles de secuencia son las estructuras que permiten dirigir el flujo de ejecución de un programa: decidir qué hacer, repetir acciones, o incluso llamar funciones recursivamente.

#### SELECION

Permite elegir entre dos o más caminos.

Ejemplos: if, if...else, switch.

```c
if (x > 0) {
    printf("Positivo");
} else {
    printf("No positivo");
}
```

#### ITERACION

Permite ejecutar un bloque varias veces.

Ejemplos: while, for, do...while.

```c
for (int i = 0; i < 5; i++) {
    printf("%d\n", i);
}
```

#### RECURSION

Una función que se llama a sí misma, en vez de usar un bucle.

```c
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

Ejemplo

```c
void displayMembers(member_t *members, book_t *library) {
    if (!members) {                                  // Selección
        printf("\nNo hay miembros disponibles.\n");  // Secuencia simple
        return;                                      // Salto
    }

    member_t *current = members;
    printf("\nMiembros disponibles en biblioteca:\n");

    while (current) {                                // Iteración (while)
        printf("\nID miembro: %d\nNombre: %s\nCantidad de libros prestados: %d\n",
            current->id, current->name, current->issued_count);

        for (int i = 0; i < current->issued_count; i++) {   // Iteración (for)
            book_t *book = findBookById(library, current->issued_books[i]); // Secuencia simple
            if (book) {                                    // Selección (if)
                printf("  Libro ID: %d\n  Titulo: %s\n  Autor: %s\n",
                        book->id, book->title, book->author);
            }
        }
        current = current->next;                           // Secuencia simple
    }

    displayMemoryUsage();                                 // Secuencia simple
}
```

En la práctica aparecen estos controles de secuencia:

- Secuencia simple: ejecución de asignaciones y llamadas (current = current->next;, printf(...)).

- Selección: if (!members), if (book).

- Iteración: while (current), for (int i = 0; i < current->issued_count; i++).

- Salto: return; (termina temprano si no hay miembros).

- Recursión: en esta función no aparece, pero podrías encontrarla en otras funciones (ej. para recorrer estructuras recursivas).

### 8.SUBPROGRAMAS

Un subprograma es un bloque de código con un nombre propio, diseñado para realizar una tarea específica y que se puede invocar (llamar) desde otro punto del programa.

En C, los subprogramas se implementan como:

- Funciones (devuelven un valor con return)

- Procedimientos (funciones void, que no devuelven nada)

#### Caracteristicas

1. Nombre → cómo lo invocas (displayMembers, findBookById, etc.).

2. Parámetros → valores que recibe para trabajar.

3. Cuerpo → el bloque de instrucciones que ejecuta.

4. Valor de retorno (opcional) → el resultado que entrega a quien lo llamó.

5. Encapsulación → permite reutilizar código sin repetirlo.

Ejemplo

```c
void displayMembers(member_t *members, book_t *library) {
    if (!members) {
        printf("\nNo hay miembros disponibles.\n");
        return;
    }

    member_t *current = members;
    printf("\nMiembros disponibles en biblioteca:\n");

    while (current) {
        printf("\nID miembro: %d\nNombre: %s\nCantidad de libros prestados: %d\n",
               current->id, current->name, current->issued_count);

        for (int i = 0; i < current->issued_count; i++) {
            book_t *book = findBookById(library, current->issued_books[i]);
            if (book) {
                printf("  Libro ID: %d\n  Titulo: %s\n  Autor: %s\n",
                        book->id, book->title, book->author);
            }
        }
        current = current->next;
    }

    displayMemoryUsage();
}
```

Subprogramas en la practica

- displayMembers

  - Tipo: procedimiento (void).

  - Parámetros: members, library.

  - Cuerpo: recorre la lista de miembros y muestra sus datos.

- findBookById

  - Tipo: función (probablemente devuelve un book_t*).

  - Parámetros: library, id.

  - Uso: localizar un libro por su ID.

- displayMemoryUsage

  - Tipo: procedimiento (void).

  - Sin parámetros.

  - Uso: mostrar estadísticas de memoria.

### 9.TIPOS DE DATOS

Los tipos de datos son la base de cualquier lenguaje de programación: definen qué clase de valores puede almacenar una variable y qué operaciones se pueden realizar sobre esos valores.

#### Tipos de datos en c

1. Primitivos (básicos):

- int → números enteros (-5, 42, 1000).

- float → números reales de precisión simple.

- double → números reales de doble precisión.

- char → un carácter ('a', 'Z').

- void → ausencia de valor (usado en funciones).

1. Derivados:

- Arreglos → colección de datos del mismo tipo.

```c
int numeros[5] = {1, 2, 3, 4, 5};
```

- Punteros → almacenan direcciones de memoria.

```c
int *p;
p = &numeros[0]; // apunta al primer elemento
```

- Funciones → también son tipos de datos en C.

1. Definidos por el usuario

- struct → agrupa diferentes tipos de datos.

```c
typedef struct {
    int id;
    char title[50];
    char author[50];
} book_t;
```

- typedef → alias para tipos ya definidos.
- enum → enumeraciones, listas de valores simbólicos.

Ejemplo

```c
void displayMembers(member_t *members, book_t *library) {
    member_t *current = members;   // current es un puntero a struct member_t
    while (current) {
        printf("\nID miembro: %d\nNombre: %s\nCantidad de libros prestados: %d\n",
            current->id,           // int
            current->name,         // char[]
            current->issued_count  // int
        );

        for (int i = 0; i < current->issued_count; i++) {  // i es int
            book_t *book = findBookById(library, current->issued_books[i]);
            // book es un puntero a struct book_t
            // issued_books[i] es un int (ID de libro)
            
            if (book) {
                printf("  Libro ID: %d\n  Titulo: %s\n  Autor: %s\n",
                    book->id,       // int
                    book->title,    // char[]
                    book->author);  // char[]
            }
        }
        current = current->next;   // current es puntero a siguiente miembro
    }
    displayMemoryUsage();          // no devuelve nada (void)
}
```

En la practica hay

- Primitivos:

  - int → IDs, contadores (id, issued_count, i).

  - char[] → cadenas de caracteres (name, title, author).

- Derivados:

  - int issued_books[] → arreglo con IDs de libros.

  - member_t * y book_t  → punteros a estructuras.

- Definidos por el usuario:

  - struct member_t y struct book_t (tipos definidos con typedef).

- Especial:

  - void en la definición de displayMembers (no retorna valor).

## CONCLUCION

Podemos concluir que es importante conocer como se compone los proyectos que los programadores realizan sin dar nada por conocer a fondo como funcionan es importante ya que asi podremos encotrar fallos en nuevos programas como tambien nos ayuda a ser mejores programadores ya que tenemos una comprension mayor de como funciona y de que esta compuesto los proyectos no solo de nuestros propios proyectos sino tambien de proyectos de otros programadores.
