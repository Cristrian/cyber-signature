
## Firma digital

#### Firma
Se debe poder firmar cualquier tipo de archivo, debe retornar llave pública y firma.
El archivo que contiene la llave pública debe especificar el algoritmo usado. Ej. JWT
Opción para tipos de archivo distintos.

Se puede especificar el nombre de quien firma y algún mensaje personalizada. 
Guardar Json.

**Opcionales**
Se puede especificar la llave privada a ser usada.
Se puede especificar el algoritmo, entre una lista de algoritmos.

#### Validación
Debe validar firmas digitales, recibiendo llave publica y archivo
Si es PDF

#### Firmas PDF
Firma visible en documentos pdf, en página adicional.
Firma no visible y modificar metadata
