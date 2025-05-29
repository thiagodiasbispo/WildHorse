from itertools import count


def despaginar(function):
    proxima_pagina = count(1)
    todos_os_dados = []
    dados = function(pagina = next(proxima_pagina))

    while dados:
        todos_os_dados.extend(dados)
        dados = function(pagina = next(proxima_pagina))

    return todos_os_dados
