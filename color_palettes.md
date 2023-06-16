# Color Palettes

## Usando cor específica

- [Faça uma busca baseada num código de cor](https://www.google.com/search?q=%23FF0B04&oq=%23FF0B04&aqs=chrome..69i57j0i546l4.288j0j7&sourceid=chrome&ie=UTF-8)

Em seguida, você pode definir essa cor na biblioteca Seaborn, por exemplo, a partir de uma lista:

```python3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

minha_paleta = ["#f5d7ce", "#ced5f5"]
sns.violinplot(x=df["gender"], y=df["TotalCharges"], palette=minha_paleta)
```

## Paletas do Seaborn

Este [link](https://seaborn.pydata.org/tutorial/color_palettes.html) da documentação apresenta uma série de definições de paletas.

É possível visualizar no Colab (Jupyter) uma paleta de cores, como especificado no trecho de código a seguir:

```python3
custom_palette = sns.color_palette("Blues", 2)
sns.palplot(custom_palette)
```


### Mais Referências

- [Como usar sua própria paleta de cores no Seaborn](https://towardsdatascience.com/how-to-use-your-own-color-palettes-with-seaborn-a45bf5175146)
