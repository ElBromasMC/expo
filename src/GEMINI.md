# Presentación Beamer

Presentar el siguiente trabajo (ubicado en `WORK.txt`) en formato Beamer.

- Comprender y analizar el documento para armar la presentación
- La presentación debe estar estructurada (introducción, desarrollo,
  conclusiones)
- Establecer las secciones que se van a usar en la presentación.
- Debe incluir la siguiente información:
    - Título del trabajo: Debe ser un título llamativo
    - Tener en cuenta el tamaño de las diapositivas al momento de añadir
      información.
    - Incluir imágenes donde sea conveniente en la presentación.
    - Las imágenes deben ser referenciales y simples, no incluir diagramas
      complejos.
    - Poner las imágenes en una diapositiva aparte para evitar overflows.
    - Autores: Espinoza H., Diego A.; Linares R., Ander R.
    - Universidad: Universidad Nacional Mayor de San Marcos
    - Grupo: Grupo 10
    - Curso: Redes, Arquitectura y Comunicaciones
- Se debe incluir la bibliografía usada (las seis fuentes más importantes) en
  la sección de Referencias.
- Definir el header del documento, con los paquetes y estílos que se van a
  usar.
- Incluir lo siguiente en el header para los estilos

    ```latex
    \usetheme{Madrid}
    \usepackage{ShanghaiTech}
    ```

- Incluir una diapositiva de despedida

    ```latex
    \begin{frame}
        \vfill
        \centering
        \LARGE\textbf{Thank You!}\\[1em]
        \large Thanks for your attendance.
        \vfill
        \includegraphics[width=0.5\textwidth]{img/dog.png} 
        \vfill
    \end{frame}
    ```

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
- Tomar en cuenta el renderizado de los caracteres del lenguaje Español.
  Incluir paquetes si es necesario.
- La herramienta ImageMagick está disponible para edición de imágenes.
- Usar la extensión de Nano Banana para la generación de imágenes.
- Usar el Makefile (`make`) para construir el documento.
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

