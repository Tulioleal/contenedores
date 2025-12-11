# Preguntas

## ¿Qué diferencia hay entre ```docker stop``` y ```docker rm```?

**``docker stop``** detiene la ejecución de un contenedor, manteniendo su estado y archivos en el disco para poder reiniciarlo; mientras que **``docker rm``** elimina permanentemente el contenedor del sistema, borrando su capa de escritura y liberando recursos.

## ¿Por qué copiamos ```requirements.txt``` antes que ```app.py```? ¿Qué ventaja tiene para el caché de Docker?

Usamos esta estrategia para **aprovechar el caché de Docker**, ya que al instalar las dependencias primero, se reutiliza la capa de instalación (que es lenta) si solo cambia el código de la aplicación, evitando reinstalaciones innecesarias.

## ¿Qué beneficios tiene usar multi-stage builds?

1. **Reducción Drástica del Tamaño de la Imagen Final:** A mi parecer, es el beneficio más significativo. Usando una etapa inicial (builder) para compilar o instalar dependencias, y luego copiar solo los artefactos necesarios a una etapa final (runtime), se eliminan herramientas de desarrollo, librerías innecesarias y archivos temporales, resultando en imágenes mucho más pequeñas.
2. **Aumento de la Seguridad:** Una imagen más pequeña tiene inherentemente una superficie de ataque reducida. Al no incluir compiladores, shells (bash), gestores de paquetes (apt, npm), ni librerías de desarrollo, hay menos binarios y archivos con potenciales vulnerabilidades (CVEs) que explotar.
3. **Separación de Preocupaciones:** Permite mantener un ```Dockerfile``` legible y ordenado, separando claramente las herramientas y dependencias necesarias solo para construir (ej. JDK, Node.js SDK, Go compiler) de las que son necesarias solo para ejecutar la aplicación (ej. JRE, Node.js runtime).

## ¿Cuál es la diferencia entre un Docker Hub público y privado? ¿Cuándo usarías cada uno?

La principal diferencia radica en el acceso y **la seguridad de las imágenes de contenedor.**

Un **Docker Hub público** almacena imágenes accesibles por cualquiera, ideal para proyectos open source, imágenes base oficiales y de prueba.

Un **Docker Hub privado** requiere autenticación para acceder a las imágenes, y se usa obligatoriamente para:

1. Imágenes de producción que contienen código propietario o secretos internos.
2. Imágenes que contienen información sensible.

En conclusión, Se usa el público cuando se quiere compartir libremente; el privado se usa siempre para el entorno empresarial y de producción.
