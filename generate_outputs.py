

def write_output(method, result, path, iteration, frontier, time, cost):
    with open(f'{method}_results.txt', 'w') as file:
        file.write(f"Resultado: {result}\n")
        file.write(f"Costo: {cost}\n")
        file.write(f"Cantidad de Nodos Expandidos: {iteration}\n")
        file.write(f"Cantidad de Nodos Frontera: {frontier}\n")
        file.write(f"Solución:\n")
        for node in path:
            file.write(f"Paso {node.depth}:\n")
            file.write("Estado:\n")
            file.write(f"*  Posición del jugador: ({node.state.player[0]}, {node.state.player[1]})\n")
            file.write(f"*  Posición de las cajas: [")
            last_index = len(node.state.boxes)-1
            for index in range(last_index):
                file.write(f"({node.state.boxes[index][0]}, {node.state.boxes[index][1]}),")
            file.write(f"({node.state.boxes[last_index][0]}, {node.state.boxes[last_index][1]})]\n")
            push_status = "Si" if node.boxed_moved else "No"
            file.write(f"*  Empuje: {push_status}\n")
            if node.parent:
                file.write(f"Movimiento previo: {node.action}\n\n")
            else:
                file.write(f"\n")
        file.write(f"Tiempo de procesamiento: {time} ms\n")

def write_output_for_visualization(method, current_node):
    with open(f'{method}_visualization.txt', 'w') as file:
        file.write(str(current_node.get_moves()))