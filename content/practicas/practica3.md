---
title: "Práctica 3"
date: 2025-11-13
draft: false
---

## Reporte: Instalación del entorno y funcionamiento de la aplicación TODO en Haskell

## Introducción

En este reporte se describe el proceso para instalar el entorno de desarrollo de Haskell utilizando Stack y la implementación de una aplicación TODO basada en la guía publicada en DEV:

How to use Haskell to build a todo app with Stack

La aplicación ejemplifica el uso de Haskell para crear programas de consola funcionales que manipulan listas y reciben comandos del usuario.

___

### 1. Requisitos previos

Para continuar, se necesita:

* Sistema operativo Windows, Linux o macOS

* Conexión a internet

* Terminal o consola de comandos

* Editor de código (Visual Studio Code recomendado)

### Instalar Stack

En Linux/macOS:

```bash
curl -sSL https://get.haskellstack.org/ | sh
```

En Windows: descargar el instalador desde la web oficial de Stack.

### 2. Crear el proyecto con Stack

En una terminal, crear un nuevo proyecto:

```bash
stack new todo
```

Esto generará un directorio con estructura de proyecto Haskell, incluyendo:

```css
todo/
 ├─ app/Main.hs
 ├─ src/Lib.hs
 ├─ test/Spec.hs
 ├─ package.yaml
 └─ stack.yaml

```

Acceder al proyecto:

``` bash
    cd todo
```

### 3. Configurar dependencias

Editar package.yaml y asegurar que contenga al menos:

```yaml
dependencies:
  - base >= 4.7 && < 5
```

(Opcional) si se desean funcionalidades extra como variables de entorno o navegador:

```yaml
  - dotenv
  - open-browser
```

Comprobar que todo compila:

```bash
stack build
```

### 4. Implementación de la aplicación TODO

Editar app/Main.hs

```haskell
module Main where

import Lib (prompt)

main :: IO ()
main = do
  putStrLn "Commands:"
  putStrLn "+ <String> - Add a TODO entry"
  putStrLn "- <Int>    - Delete the numbered entry"
  putStrLn "s <Int>    - Show the numbered entry"
  putStrLn "e <Int>    - Edit the numbered entry"
  putStrLn "l          - List todo"
  putStrLn "r          - Reverse todo"
  putStrLn "c          - Clear todo"
  putStrLn "q          - Quit"
  prompt []
```

Editar src/Lib.hs

Código base del sistema TODO:

```haskel
module Lib
  ( prompt,
    editIndex
  )
where

import Data.List

putTodo :: (Int, String) -> IO ()
putTodo (n, todo) = putStrLn (show n ++ ": " ++ todo)

prompt :: [String] -> IO ()
prompt todos = do
  command <- getLine
  interpret command todos

interpret :: String -> [String] -> IO ()
interpret ('+' : ' ' : todo) todos = prompt (todo : todos)
interpret ('-' : ' ' : num) todos =
  case deleteOne (read num) todos of
    Nothing -> do putStrLn "Invalid number"; prompt todos
    Just todos' -> prompt todos'
interpret ('s' : ' ' : num) todos =
  case showOne (read num) todos of
    Nothing -> do putStrLn "Invalid number"; prompt todos
    Just todo -> do print todo; prompt todos
interpret "l" todos = do
  mapM_ putTodo (zip [0 ..] todos)
  prompt todos
interpret "r" todos = do
  let reversedTodos = reverse todos
  mapM_ putTodo (zip [0 ..] reversedTodos)
  prompt todos
interpret "c" todos = prompt []
interpret "q" todos = return ()
interpret command todos = do
  putStrLn ("Invalid command: " ++ command)
  prompt todos

deleteOne :: Int -> [a] -> Maybe [a]
deleteOne 0 (_ : xs) = Just xs
deleteOne n (x : xs) = do xs' <- deleteOne (n - 1) xs; return (x : xs')
deleteOne _ [] = Nothing

showOne :: Int -> [a] -> Maybe a
showOne n xs = if n < length xs then Just (xs !! n) else Nothing

editIndex :: Int -> a -> [a] -> [a]
editIndex i x xs = take i xs ++ [x] ++ drop (i + 1) xs

```

### 5. Pruebas opcionales

Modificar test/Spec.hs:

```haskell
import Control.Exception
import Lib (editIndex)

main :: IO ()
main = do
  let result = editIndex 1 "two" ["Write","a","blog"] == ["Write","two","blog"]
  putStrLn $ assert result "editIndex worked."
```

Ejecutar pruebas:

```bash
stack test
```

### 6. Ejecutar la aplicación

``` bash
stack run
```

Ejemplos de uso interactivo:

| Comando         | Acción           |
| --------------- | ---------------- |
| `+ Comprar pan` | Agrega una tarea |
| `l`             | Lista tareas     |
| `- 0`           | Elimina tarea 0  |
| `q`             | Salir            |

## CONCLUCIONES

La implementación de esta aplicación TODO permite:

* Practicar conceptos funcionales de Haskell

* Usar listas, recursión y monadas de entrada/salida (IO)

* Desarrollar una interfaz de comando con un ciclo de lectura de usuario

* Realizar pruebas y compilar mediante Stack

Este ejercicio es ideal para introducirse al desarrollo práctico en Haskell, demostrando cómo un lenguaje funcional puede crear aplicaciones reales y mantenibles.

OSCAR ARMANDO MEDINA GUTIERREZ.
