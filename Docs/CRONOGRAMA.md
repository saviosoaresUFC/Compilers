## Opção 1 – Análise Léxica

**OBS**: Linguagem de programação: Python pela facilidade com dicionários/listas para grafos.



### **Fase 1: Entregar dia 26**

**Dia 25:** 

* **Sávio:** Mapear todos os tokens da LangC (palavras reservadas, operadores, identificadores, tipos) e escrever as Regexes. Já monta o .txt.  

* **Samuel e Kauan:** Começam a estruturar as classes/estruturas de dados do Autômato (como representar os estados e arestas: matriz ou dicionário).  

**Dia 26:**

* **Sávio**: Finaliza o gerador de NFA. 

* **Samuel**: Começa a rascunhar a lógica do algoritmo de conversão para DFA.



### **Fase 2: Entregar dia 29**

**Dia 27:** 

* **Sávio**: Entregar o gerador de NFA funcionando pro Samuel.  

* **Samuel**: Focar no algoritmo de NFA -> DFA.  

* **Kauan**: Começa a codificar a estrutura do Driver do Analisador Léxico (leitura de arquivos, loop de caracteres).  

**Dia 28:**

* **Samuel**: Finaliza e testa a conversão para DFA.  

* **Kauan**: Integra o DFA do Samuel no motor do Analisador Léxico.  

**Dia 29:** 

* **Kauan**: Finaliza a lógica de casamento de padrões usando o DFA e a geração das strings de saída (`NUM VAR EQ`... ou `ERRO`).  



### **Fase 3: Entregar dia 01**

**Dia 30:** 

* Juntar as partes dos três em um único fluxo. Rodar o programa usando os exemplos do PDF (como o do slide 6 e 7) para validar o comportamento.  
* Varredura de bugs (edge cases: o que acontece com um identificador com mais de 30 caracteres? E com comentários ou quebras de linha?).  
* Criar as instruções de execução (README) e gerar a pasta .zip com nossos nomes.

&#x20;

**Dia 01/06 (Prazo Final):** Revisão e envio do e-mail para o Ismaily (ismailybf@ufc.br)

