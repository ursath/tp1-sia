

def write_output(method, result, path, iteration, frontier, time, cost, is_uninformed):
    with open(f'{method}_results.txt', 'w') as file:
        file.write(f"Resultado: {result}\n")
        file.write(f"Costo: {cost}\n")
        file.write(f"Cantidad de Nodos Expandidos: {iteration}\n")
        file.write(f"Cantidad de Nodos Frontera: {frontier}\n")
        file.write(f"Solución:\n")
        step = 0
        for node in path:
            if is_uninformed:
                node = node.state
                boxes = node.boxes
            else:
                boxes = list(node.boxes)
            file.write(f"Paso {step}:\n")
            file.write("Estado:\n")
            file.write(f"*  Posición del jugador: ({node.player[0]}, {node.player[1]})\n")
            file.write(f"*  Posición de las cajas: [")
            last_index = len(boxes)-1
            for index in range(last_index):
                file.write(f"({boxes[index][0]}, {boxes[index][1]}),")
            file.write(f"({boxes[last_index][0]}, {boxes[last_index][1]})]\n")
            #push_status = "Si" if node.boxed_moved else "No"
            #file.write(f"*  Empuje: {push_status}\n")
            if step > 0:
                file.write(f"Movimiento previo: ({node.player[0] - previous_node[0]}, {node.player[1] - previous_node[1]})\n\n")
            else:
                file.write(f"\n")
            step += 1
            previous_node = node.player
        file.write(f"Tiempo de procesamiento: {time} ms\n")

def write_output_for_visualization(map, method, execution_time, explored, frontier, steps):
    with open(f'{method}_for_map_{map}.csv', 'w') as file:
        file.write(f'{map},{method},None,{execution_time},{explored},{frontier},{steps}\n')