
- No arquivo de estilos global (globals.css), pode criar uma classe reutilizável com o **@apply**:

```
.page-container {
  @apply p-8 w-full;
}
```

- Depois aplique essa classe nas paginas:
  
```
<div className="page-container">
  {/* Conteúdo da página */}
</div>

```