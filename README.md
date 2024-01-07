# Prueba técnica - Desarrollador Fullstack efRouting
En este repositorio se encuentra tood el contenido solicitado en la prueba técnica, en la cual se construyo una base de datos en AWS (Usando RDS), se extrae información de la API de CoinMarketCap mediante una función Lambda escrita en Python, y luego despliegues una página web donde muestres un gráfico con la información extraída utilizando un contenedor Docker y servicios de AWS (RDS y ECS).

Para ver la pagina, dirigirse al siguiente [enlace](http://cryptodev.myddns.me/).

## Descripción de los puntos

  - [RDS][def]
  - [CoinMarketCap][def2]
  - [Lambda][def3]
  - [Despliegue][def4]

## RDS

### Construcción de una base de datos en AWS:

**A tener en cuenta antes de crear todo**

  - **Debe tener cuenta AWS**.

  - **Hay que revisar el tipo de cuenta y que la región sea _´EE.UU. Este (Norte de Virginia) us-east-1´_ para no tener problemas para conectarse posteriormente a la RDS**.

1. **Crear base de datos (RDS)**:
   
   Una vez dentro del panel de servicios de AWS burcar las siglas [RDS](https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#launch-dbinstance:;isHermesCreate=true), escoger la opcion de capa gratuita, seleccionar el tipo de motor de base de datos, asignar un _**user**_ y un _**password**_.
   
3. **Conectividad**:
   
   En las opciones de conectividad asegurar que la casilla de acceso publico se encuetre marcada en _**si**_ para poder ingresar desde fuera de AWS, los demas valores pueden quedar por defecto.

5. **Conexión**:
   
   Una vez creada la base de datos nos dirigimos a las opcionoes del grupo de seguridad y dentro de reglas de entrada nos aseguramos que se permita el trafico desde cualquier ip.

7. **MySQL Workbrench**:
   
   Para manejar la creación, modificación y eliminación de tablas en nuestra base de datos de forma visual utilizamos el software [MySQL worbrench](https://dev.mysql.com/downloads/file/?id=519997).

9. **Acceso**:
   
   Desde la pantalla principal de MySQL Workbrench nos conectamos a la base de datos creando una concexión con: _**user**_, _**password**_ y la _**url**_ de la RDS. Una vez dentro podemos crear las tablas que usaremos para guardar la informacón extraida con la API.
   
10. **Subir datos**:
    
    Al tener todo lo anterior listo solo nos queda crear una función que nos permita conectarnos a la API y que guarde esos datos en nuesta RDS, lo cual se mostrará en los puntos posteriores.

## CoinMarketCap

### Extracción de información desde la API de CoinMarketCap
1. **Validar cuenta en CoinMarketCap:**
   
   Entrar a la pagina principal de [CoinMarketCap](https://pro.coinmarketcap.com/account) iniciar sesión o crear una cuenta según sea el caso.
   
3. **Variables importantes:**
   
   Configurar en un archivo _**.env**_ las variables de conexión importantes que usaremos como variables de entorno:

   La key personal que encontraremos en nuestro panel de control de CoinMarketCap:
   ```cmd
   COIN_APY_KEY:	"YOUR_API_KEY"
   ```
   
   Los datos de conexión a la base de datos que antes mencionamos:
    ```cmd
    DB_HOST:	"YOUR_DB_HOST",
    DB_NAME:	"YOUR_DB_NAME",
    DB_PASSWORD:	"YOUR_DB_PASSWORD",
    DB_USER:	"YOUR_DB_USER",
    ```
5. **Creación de la logica:**
   
   Creamos nuestro código usando la [documentación](https://coinmarketcap.com/api/documentation/v1/#section/Quick-Start-Guide) de la api que nos muestra la forma de extraer los datos de la misma.
   
7. **Envío de información a la RDS:**
   
   Una vez tengamos los datos que queremos, en el mismo código lo enviamos a nuestra RDS usando nuestra sentencia SQL y la conexión explicada en los pasos anteriores.
   
9. **Revisión de los datos enviados en MySQL Workbrench:**
    
    Para validar que todo se encuentre en orden, revisamos tanto la consola de error de nuestro editor de codigo, así como los datos que llegaron a la tabla de la RDS de forma visual por medio de MySQL Workbrench.

## Lambda

1. **AWS Lambda:**

   Dentro de nuestro panel de control de la cuenta AWS buscamos el servicio denominado [Lambda](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions)
   
3. **Crear la función:**

   Una vez dentro, vamos y presionamos donde dice crear función, en el apartado de información básica le damos el nombre de nuestra preferencia y en tiempo de ejecución asignamos _**Python**_ con la versión que allí aparace, el resto de las caracteristicas pueden quedar por defecto.
   
5. **Montar nuestro código:**

   Una vez creada nuestra función añadimos el codigo escrito en anteriores puntos en el espacio señalado por la función.

7. **Manejo de librerias:**
   
   Para un correcto funcionamiento del script suministrado debemos darle un manejo correcto a las librerías usada, creamos una nueva carpeta en el escritorio llamada _**python**_ y una vez dentro instalamos las librerias de la siguiente forma:
   ```cmd
     pip3 install requests -t .
     pip3 install pymysql -t .
    ```
   Una vez terminada, comprimimos la carpeta como un archivo _**ZIP**_
   
9. **Manejo de capas:**
    
    Nos dirigimos al apartado de capas y presionamos [añadir](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/add/layer?function=Datos_pruebaefRouting), le asignamos un nombre, una descripción para saber de que trata y por ultimo subimos el archivo _**zip**_ del paso anterior. Por ultimo, vamos al apartado de funciones seleccionando la función con la que estamos trabajando y en la aprte inferior añadimos la capa, escogemos capa perzonalizada y seleccionamos la que acabamos de crear.

11. **Desencadenador:**

    En el mismo apartado de funciones seleccionamos _**desencadenador**_ y escogemos la opción _**CloudWatch Events**_ que nos permitirá crear una nueva regla, por ultimo en _**Schedule expression**_ le asignamos ```rate(6 hours)``` 
    
13. **Pruebas:**
    Para probar que todo funcione correctamente seleccionamos la opción _**test**_, escogemos la plantilla que se encuentra allí y verificamos que el codigo se ejecute de forma correcta.


## Despliegue

### Docker:

1. **Repositorio:**
   
   Una vez diseñada nuestra página web clonamos el repositorio en nuestro editor local y corremos el siguiente codigo para instalar las dependencias.
   ```script 
     pip install --no-cache-dir -r requirements.txt
   ```
   
3. **Variables de entorno:**
   En la carpeta raiz del proyecto creamos un archivo _**.env** en donde se establecen las variables de conexión a la base datos:
   ```script
    DB_HOST: 'your_host'
    DB_USER: 'your_user'
    DB_PASSWORD: 'your_password'
    DB_NAME: 'your_database'
    ```
4. **Prueba en local:**
   
   Una vez realizado esto ejecutamos usando la siguiente serie de comandos:
   
  - Primero activamos el entorno virtual:
    
    ```script
     \env\Scripts\activate
     ```
  
  - Ejecutamos el proyecto:
    ```script
    \app\python app.py 
    ```

    Todo se ejecutará en en _**[localhost:5000](localhost:5000)**_.

5. **Creación de imagen docker:**

   Una vez verificado el correcto funcionamiento de nuestro proyecto procedemos a crear la imagen docker de la siguiente forma:

- Creamos un archivo _**Dockerfile**_ con las siguientes instrucciones:
     
     ```cmd
      #Usa una imagen de Python
      FROM python:3.9

      #Establece el directorio de trabajo en /app
      WORKDIR /app

      #Copia todo el contenido de la carpeta Pagina_Prueba al contenedor
      COPY . /app

      #Instala las dependencias del proyecto
      RUN pip install -r /app/app/requirements.txt

      #Comando para ejecutar la aplicación Flask cuando el contenedor se inicie
      CMD ["python", "/app/app/app.py"]
    ```

- Usamos el siguiente comando para crear la imagen:
    ```script
    docker build -t "nombre_de_la_imagen" .
    ```
- Probamos la imagen docker:
     ```script
    docker run -it -p 4000:5000 nombre_de_la_imagen 
    ```
### **AWS cli**

- **Antes de:**
  
   Instalar Amazon CLI desde el siguiente [enlace](https://aws.amazon.com/es/cli/)

1. **Credenciales:**
   
   Una cez instalado lo anterior vamos a [AWS](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/security_credentials) para gestionar las credenciales de acceso remoto.

3. **Credenciales en AWS configure:**

   Usando nuestra terminal copiamos:

   ```script 
     aws configure    
    ```
   Y llenamos los datos que nos piden con respecto a las credenciales.

5. **AWS ECR:**

   En el panel de sevicio de AWS escogemos la opción de [ECR](https://us-east-1.console.aws.amazon.com/ecr/create-repository?region=us-east-1) en donde creamos un repositorio para almacenar nuestra imagen docker creada anteriormente. Tenga que en cuenta que durante la ejecución pueden aparecer algunos errores:
   - _**Error saving credentials: error storing credentials - err: exit status 1, out: `The stub received bad data.`**_

   Se solucionas de la siguiente manera:

   - **Entrar en:**

   ```script
    c:\Users\"YOUR_USER"\.docker\config.json  
   ```

   Eliminar la linea que con el valor de _"credsStore"_

   - **Entrar en:**

   ```script
    C:\Program Files\Docker\Docker\resources\bin\  
   ```
   
   Eliminar los archivos: _**docker-credential-desktop.exe**_ y _**docker-credential-wincred.exe**_

7. **AWS ECS:**
   
   En el panel de control de AWS seleccionamos [ECS](https://us-east-1.console.aws.amazon.com/ecs/v2/clusters?region=us-east-1) y cremos nuestro cluster siguiendo las opciones que aparecen allí, hay que tener en cuenta la redirección de puerto del 80 al 5000 y el acceso publico que debe estar habilitado. Por ultimo, le asignamos nuestro contenedor creado en la ECR.

9. **DNS:**
    
    Como paso opcional se le puede asignar una direccion DNS personalizada a la dirección ip publica que nos asigna AWS al crear la ECS en el cual estará ubicada nuestra pagina web realizada para la [prueba](http://cryptodev.myddns.me/). 











[def]: #RDS

[def2]: #CoinMarketCap

[def3]: #Lambda

[def4]: #Despliegue




