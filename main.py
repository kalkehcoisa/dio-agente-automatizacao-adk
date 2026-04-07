from src.orchestrator import orchestrator


def main():
    print("🤖 Assistente de Automação de Tarefas (Google ADK)")
    print("Exemplos de comandos:")
    print("- Crie uma tarefa 'Revisar relatório' no ClickUp")
    print("- No Plane, adicione uma issue 'Corrigir bug' ao projeto XYZ")
    print("- Adicione um card 'Estudar ADK' no Wekan")
    print("- Kanboard: nova tarefa 'Testar integração' no projeto 1")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit"]:
            break

        # Executa o agente orquestrador
        response = orchestrator.run(user_input)
        print(f"Assistente: {response}\n")


if __name__ == "__main__":
    main()
