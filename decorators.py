def decorator(funcao):
    def wrapper(*args, **kwargs):
        print("Estou antes da execução da função passada como argumento")
        print(args)
        print(kwargs)
        result = funcao(*args, **kwargs)
        print("Estou depois da execução da função passada como argumento")
        return result

    return wrapper