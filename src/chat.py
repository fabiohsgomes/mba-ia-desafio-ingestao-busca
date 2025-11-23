from search import search_prompt

def main():
    print("Faça uma pergunta:\n\n")
    
    question = input("PERGUNTA: ")
    
    response = search_prompt(question=question)

    print(f"RESPOSTA: {response}")

if __name__ == "__main__":
    main()