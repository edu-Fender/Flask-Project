## -- Script inicial a ser executado --
## Não é necessário alterar nada nesse arquivo

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)