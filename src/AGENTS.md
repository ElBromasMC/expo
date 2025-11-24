# Constructor de presentación en formato Beamer

## Plan base

### Análisis del documento

- Comprender y analizar el documento `DOCUMENT.txt` para armar la presentación.
- Establecer las secciones en las que se va a dividir la presentación.
- Usar el título proporcionado por el documento para la presentación, si no se
  especifica un título proponer uno llamativo.
- Considerar también la información del o los autores, universidad, etc.

### Construcción de la presentación

- Definir el header del documento, con los paquetes y estílos que se van a
  usar.
- Armar la primera diapositiva, donde se presenta el título de la presentación,
  subtítulo si está presente, autor o autores, universidad, año, etc.
- Armar las secciones de la presentación, no incluir demasiado texto y dejar
  placeholders donde sea conveniente poner una imagen indicando con comentarios
  lo que debe representar dicha imagen.
- Armar la diapositiva de Bibliografía con las 6 fuentes más importantes.
- Armar la diapositiva de despedida.

## Información importante

- El lenguaje del documento debe ser Español.

## Tips para desarrollo

- Usar `make` para construir el documento.
- El documento principal debe ser `presentation.tex` y las secciones deben
  estar en la carpeta `sections`
- Dividir la presentación en varios archivos. Usar una secuencia de números al
  inicio del nombre de cada archivo `03-seccion.txt`.
- Los archivos estáticos como imágenes se van a incluir en la carpeta `./img`
- Usar `\documentclass[aspectratio=169]{beamer}`.
- Incluir `\usepackage[utf8]{inputenc}` en el header de la presentación para
  poder usar directamente algunos caracteres UTF-8 en la presentación como
  palabras con tilde.
- Las comillas dobles deben escribirse en el código fuente usando `` y '' para
  que se rendericen correctamente, no se debe usar directamente las comillas
  dobles ".
- Asegurarse de que se usen caracteres UTF-8 válidos para Latex. Tener cuidado
  con las secuencias de escape Unicode.
- Asegurarse de no insertar triple comillas ''' o ``` al inicio y al final de
  un documento al momento de generar código Latex.
- No modificar los archivos `Dockerfile`, `Makefile` proporcionados.
- La herramienta ImageMagick está disponible para edición de imágenes. Podemos
  usarla para crear los placeholders.
- Usar un comentario que incluya `TODO` para indicar la presencia de un
  placeholder.
- Corregir la mayoría de errores y advertencias de la compilación, para
  garantizar un renderizado correcto. Algunas estrategias son reducir el tamaño
  de las imágenes, separar el contenido en más diapositivas, etc.
- Si al incluir imágenes existen errores de overflow, intentar recortarlos o
  redimensionarlos.

