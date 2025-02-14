# Requerimiento del SISTEMA XDDXJFLDKX;JFKLDJFSDFASDF;LKASDJFA

1. Requerimiento Funcionales:
    - Recopilar precio de tiendas local de hardware,
    - Actualizacion automatica
    - Guardar los metadatos del producto
    - Visualizacion Historica de un producto de acuerdo a la tienda que se selecione
    - Entregar de forma ascedente los precio de diferente tiendas
    - Tener un carrito de comprar que puede agregar producto de cualquier tienda
    - Dar una pseudo preforma sobre la lista del carrito, incluyento envio en el caso que sea de provincia

2. Requerimiento No Funcionales:
    - Recopilacion de precio utilizando webscraping con Python
    - Guarda la informacion en una base de datos PostgreSQL
    - Contruccion del la apiclacion con Python utilizando cualquier framework
    - Guardar Solo los cambio que hay de precio
    - Utilizar tecnica como cambiar de agente entre otras para evitar que detecte el scraping
    - Session para la creacion del carrito de compra
    - Implementar reitentos en caso de fallos en el scraping
    - Notificar si una tienda cambia su estructura
    - Backup de la base de datos xddxxd

3. Componentes:
    - Base de datos (PostgreSQL)
    - Scraping (Scrapy + proxies)
    - Servicio Api (Django REST Framework)
    <!-- - Pgrogramador de tarea (Celery) -->
    - Carrito (Django REST Framework)
    <!-- - Notificacion? (correo para admins y numero para wsp xddx) -->
    - cache (Redis)

    ``` mermaid
    graph TD
        F[Cliente] --> A
        F --> B
        E[Servicio de Scraping] -->|Actualiza| C
        A[Servicio API] -->|Lee/Escribe| C[(Base de Datos)]
        A -->|Cachea respuestas| D[Caché]
        B -->|Guarda carritos| D
        B[Servicio de Carrito] -->|Valida precios| A
    ```

4. Tener en cuenta:
    - load Balacers
    - sub red, que solo server se conecte a la base de dato y esta solo acepte del webserve, y para que un usuario se conecte, lo hara con el Load Balacers
