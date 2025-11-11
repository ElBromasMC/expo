# Presentación Beamer

Presentar el siguiente trabajo (ubicado en `WORK.txt`) en formato Beamer.

- Comprender y analizar el documento para armar la presentación
- Establecer las secciones que se van a usar en la presentación.
- Debe incluir la siguiente información:
    - Título del trabajo: Debe ser un título llamativo
    - Tener en cuenta el tamaño de las diapositivas al momento de añadir
      información.
    - Incluir imágenes donde sea conveniente en la presentación.
    - Las imágenes deben ser referenciales y simples, no incluir diagramas
      complejos.
    - Considerar la información de los autores, universidad, grupo, etc.
- Se debe incluir la bibliografía usada (las nueve fuentes más importantes) en
  la sección de Referencias. Incluir un enlace a las referencias.
- Definir el header del documento, con los paquetes y estílos que se van a
  usar.
- Incluir lo siguiente en el header

    ```latex
    \usepackage[utf8]{inputenc}
    ```

- Incluir una diapositiva de despedida

- Usar el patrón de nombres breves y nombres detallados para las secciones en
  el documeto `\section[nombre breve]{nombre detallado}`
- Los archivos estáticos como imágenes se van a incluir en la carpeta `./img`
- Dividir la presentación en varios archivos para que esta sea más organizada.
  Usar una secuencia de números al inicio del nombre de cada archivo
  `03-seccion.txt`.
- El documento principal debe ser `presentation.tex` y las secciones deben
  estar en la carpeta `sections`
- Asegurarse de que las letras con tilde (á, é, í, ó, ú) se rendericen
  correctamente.
- Asegurarse de que las comillas (``, '') se rendericen correctamente. No usar
  comillas dobles (") en el código fuente del documento.
- Asegurarse de que se usen caracteres UTF-8 válidos para Latex. Tener cuidado
  con la herramienta `write_file` y las secuencias de escape Unicode.
- Asegurarse de no insertar triple comillas (''') o (```) al inicio y al final
  de un documento al momento de generar código Latex.
- Tomar en cuenta el renderizado de los caracteres del lenguaje Español.
  Incluir paquetes si es necesario.
- La herramienta ImageMagick está disponible para edición de imágenes.
- Usar la extensión de Nano Banana para la generación de imágenes.
- Usar el Makefile proporcionado (`make`) para construir el documento.
- No modificar los archivos `Dockerfile`, `Makefile` proporcionados.
- Intentar corregir los errores de overflow, para garantizar un renderizado
  correcto. Por ejemplo, reducir el tamaño de las imágenes, separar el
  contenido en más diapositivas, etc. No es necesario corregir todos los
  errores de overflow, intentar corregir los que afectan principalmente a las
  partes más importantes de la presentación.
- Si al incluir imágenes existen errores de overflow, intentar recortarlos o
  redimensionarlos. Empezar con un tamaño de height=0.5\textwidth.
- Al terminar de generar las imágenes usar ImageMagick para comprimir los png.

Como primer paso, analizar el documento y plantear la estrucutra de la
presentación. El objetivo es diseñar una presentación interesante y
estructurada.

