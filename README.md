# Reporte de Herramientas y Tecnologías: Markdown, Git, GitHub, Hugo y GitHub Actions

---

## Markdown

### ¿Qué es Markdown?

Markdown es un **lenguaje de marcado ligero** que permite escribir texto con formato de manera sencilla, usando caracteres especiales en lugar de botones complejos como en procesadores de texto.  
Su principal ventaja es que el contenido es **legible en texto plano** y se puede convertir fácilmente a HTML para la web.

### ¿Cómo se utiliza?

Markdown se usa escribiendo texto con símbolos específicos para dar formato. Es muy popular en archivos `README.md`, blogs y documentación.

### Sintaxis básica de Markdown

| Formato | Sintaxis | Ejemplo |
|---------|----------|---------|
| Encabezado | `# Título 1`<br>`## Título 2`<br>`### Título 3` | # Título 1<br>## Título 2 |
| Negrita | `**texto**` o `__texto__` | **Negrita** |
| Cursiva | `*texto*` o `_texto_` | *Cursiva* |
| Listas | `- Item` o `* Item` | - Item 1<br>- Item 2 |
| Listas numeradas | `1. Item` | 1. Paso 1<br>2. Paso 2 |
| Enlaces | `[Texto](URL)` | [Google](https://www.google.com) |
| Imágenes | `![Alt](URL)` | ![Logo](https://example.com/logo.png) |
| Código en línea | `` `codigo` `` | `printf("Hola")` |
| Bloques de código | <pre>```c<br>código<br>```</pre> | ```c<br>int main() { return 0; }<br>``` |

---

## Git y GitHub

### ¿Qué es Git?
Git es un **sistema de control de versiones** que permite llevar un registro de los cambios realizados en archivos y proyectos, facilitando trabajar en equipo y mantener un historial de versiones.

### ¿Qué es GitHub?
GitHub es una **plataforma basada en la nube** que aloja repositorios Git, permitiendo compartir código, colaborar en proyectos y publicar documentación.

### Comandos esenciales de Git
```bash```

# Configurar usuario
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Inicializar repositorio
git init

# Añadir archivos al área de preparación
git add archivo.txt
git add .

# Hacer commit
git commit -m "Mensaje de commit"

# Ver estado
git status

# Ver historial de commits
git log

# Conectar con repositorio remoto
git remote add origin https://github.com/usuario/repositorio.git

# Subir cambios al repositorio remoto
git push -u origin main

1. Inicia sesión en GitHub.
2. Haz clic en **New repository**.
3. Asigna un nombre y decide si será público o privado.
4. Clona el repositorio a tu máquina:
   git clone https://github.com/usuario/repositorio.git
5. Agrega archivos, haz commit y push para subir cambios.


##  Hugo y GitHub Actions

### ¿Qué es Hugo?
Hugo es un **generador de sitios web estáticos** que convierte archivos Markdown en páginas web listas para publicar de manera rápida y eficiente.  
Es muy utilizado para **blogs, documentación y sitios web personales**, porque genera páginas HTML estáticas sin necesidad de base de datos y permite usar **plantillas y temas**.

### ¿Qué son GitHub Actions?
GitHub Actions es un **servicio de integración y despliegue continuo _(CI/CD)** que permite automatizar tareas dentro de GitHub, como:

- Compilar proyectos.
- Ejecutar pruebas.
- Publicar sitios web automáticamente al hacer cambios en un repositorio.

# Instalar Hugo desde su sitio oficial o gestor de paquetes
# Crear un nuevo sitio
hugo new site mi-sitio

# Añadir un tema
cd mi-sitio
git init
git submodule add https://github.com/tema/ejemplo-theme.git themes/ejemplo-theme
echo 'theme = "ejemplo-theme"' >> config.toml

# Crear contenido en Markdown
hugo new posts/primer-articulo.md

# Generar el sitio
hugo

git add .
git commit -m "Agregar sitio Hugo"
git push -u origin main


# .github/workflows/deploy.yml
name: Deploy Hugo site to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: peaceiris/actions-hugo@v2
      with:
        hugo-version: '0.111.3'
    - run: hugo --minify
    - uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: "${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./public"

https://github.com/Oscar845-s/PORTAFOLIO