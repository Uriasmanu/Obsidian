
### Comandos Iniciais

```
npm install prisma --save-dev
npm install @prisma/extension-accelerate

npx prisma init
```


O `prisma init`comando também cria um `.env`arquivo na raiz do seu projeto. Esse arquivo é usado para armazenar sua string de conexão com o banco de dados.

### **Gerador do Cliente Prisma**

```
generator client {   
provider = "prisma-client-js" 
}
```

- O Prisma usa **geradores (generators)** para criar um cliente que permite interagir com o banco de dados via código TypeScript/JavaScript.
- Aqui, ele está configurado para usar **`prisma-client-js`**, que é a biblioteca oficial do Prisma para Node.js.

### MongoDB[​](https://www.prisma.io/docs/orm/reference/connection-urls#mongodb "Direct link to MongoDB")

schema.prisma

```
datasource db {  
provider = "mongodb"  
url      = "mongodb+srv://root:<password>@cluster0.ab1cd.mongodb.net/myDatabase?retryWrites=true&w=majority"
}
```

- `taskManargeDb` é o nome do banco de dados dentro do Prisma (pode ser qualquer nome).
- `provider = "mongodb"` indica que o banco de dados usado é o **MongoDB**.
- `url = env("DATABASE_URL")` pega a URL de conexão do banco de uma variável de ambiente (`DATABASE_URL`), o que evita expor informações sensíveis no código.


1. **Gere o Prisma Client:**  
    Execute o comando abaixo para gerar o Prisma Client com base no esquema corrigido:
    
```
npx prisma generate
```
    
2. **Aplique as Migrações (se necessário):**  
    Se você estiver usando um banco de dados novo ou quiser sincronizar o esquema com o banco de dados, execute:
    
```
npx prisma db push
```
    
3. **Use o Prisma Client:**  
    Agora você pode usar o Prisma Client em sua aplicação para interagir com o banco de dados MongoDB.
