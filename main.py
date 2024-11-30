from path_solver import find_hamiltonian_from_json

if __name__ == "__main__":
    file_path = "input3.json"
    result = find_hamiltonian_from_json(file_path)

    if result["type"] == "cycle":
        if result["result"]:
            print("Hamiltonian cycle found:", result["result"])
        else:
            print("No Hamiltonian cycle exists")
    elif result["type"] == "path":
        if result["result"]:
            print("Hamiltonian path found:", result["result"])
        else:
            print("No Hamiltonian path exists")
