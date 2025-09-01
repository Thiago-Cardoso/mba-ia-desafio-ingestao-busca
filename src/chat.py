from search import search_prompt

def main():
    print("=== Sistema de Ingestão e Busca Semântica com LangChain ===")
    print("Digite 'sair' para encerrar o chat\n")

    while True:
        try:
            user_input = input("Faça sua pergunta: ").strip()

            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando chat...")
                break

            if not user_input:
                continue

            response = search_prompt(user_input)

            print(f"RESPOSTA: {response}")
            print("---")

        except KeyboardInterrupt:
            print("\nEncerrando chat...")
            break
        except Exception as e:
            print(f"Erro: {str(e)}")
            print("---")

if __name__ == "__main__":
    main()