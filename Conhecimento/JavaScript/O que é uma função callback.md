# Callback

Uma **callback** é uma função que é passada como argumento para outra função. Essa função será **executada mais tarde**, dentro da função que a recebeu.

## Exemplo com .map()

```
const items = [ 
    { title: "Home", url: "#", icon: Home }
];

{items.map((item) => ( 
    <SidebarMenuItem key={item.title}>
        <SidebarMenuButton asChild>
            <a href={item.url}>
                <item.icon />
                <span>{item.title}</span>
            </a>
        </SidebarMenuButton>
    </SidebarMenuItem>
))}
```

A função callback é **tudo que está dentro do `.map()`**.

O `.map()` percorre o array `items` e para cada objeto, retorna um JSX (`<SidebarMenuItem>...</SidebarMenuItem>`).

## Passo a passo do .map()

1. Pega o primeiro item do array
2. Executa a função de callback nesse item e obtém um novo valor
3. Guarda esse novo valor em um novo array
4. Vai para o próximo item do array original e repete o processo
5. Quando todos os itens forem processados, retorna um novo array com os valores transformados

**IMPORTANTE:** O array original **não** é modificado.