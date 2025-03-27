# TP1 - Métodos de Búsqueda

## Instalación de las dependencias:

pip install -r requirements.txt

## Graficar el juego sokoban
### Se debe modificar el main de sokoban.py para seleccionar el algoritmo y mapa deseado
```sh
python sokoban.py
```

## Obtener los gráficos y archivos con resultados para todos los métodos
```sh
python stats.py
```

## Observaciones
- Para agregar un mapa, se debe agregar a la carpeta maps.
- Formato de los mapas: si el borde del mapa no es cuadrado, se deben agregar # en los espacios de los costados para completar la pared de forma tal que quede cuadrada (ver mapa Dificil de ejemplo correcto de uso). Un ejemplo incorrecto sería el siguiente:
```
      ###
      #.#
  #####.#####
 ##         ##
##  # # # #  ##
#  ##     ##  #
# ##  # #  ## #
#     $@$     #
####  ###  ####
   #### ####
```
### Parámetros para cambiar de heurística
Dentro de la función `main` del archivo de `sokoban.py` se deberá pasar uno de los siguientes valores como segundo parámetro de las funciones de `get_greedy` o `get_astar`:
- `"manhattan_distance"`
- `"manhattan_improved"`
- `"manhattan_with_deadlock_detection"`
- `"manhattan_with_corral_deadlock_detection"`
- `"player_distance"`
- `"combined"`
- `"combined_with_deadlock_detection"`

Ejemplo:
``` python
result = get_astar(data_map, "manhattan_with_corral_deadlock_detection", valid_box_positions)
game.moves = result['directions']
```


