# Relação da Estrutura de Diretórios com SOLID

Abaixo está a explicação de como cada diretório do projeto em `src/` se relaciona com os princípios SOLID, fundamentais para arquitetura de software orientada a objetos.

---

## Estrutura do diretório `src`

```
src/
  config/
  interfaces/
  models/
  services/
  spv_automatico.py
```

---

## Relação dos diretórios com SOLID

### 1. `models/`
- **O que contém:** Classes de domínio, entidades, representações de dados (ex: Cliente, Pesquisa, Serviço).
- **Princípios SOLID:**
  - **Single Responsibility Principle (SRP):** Cada model tem a responsabilidade única de representar e validar uma entidade do domínio.
  - **Open/Closed Principle (OCP):** Models podem ser estendidos (herança, mixins) sem modificar o código original.
- **Resumo:** Representa o núcleo do domínio, focado em dados e regras de negócio básicas.

---

### 2. `services/`
- **O que contém:** Lógica de negócio, orquestração de processos, regras de aplicação (ex: processar pesquisa, gerar relatório).
- **Princípios SOLID:**
  - **Single Responsibility Principle (SRP):** Cada service executa uma ação ou processo específico do negócio.
  - **Dependency Inversion Principle (DIP):** Services dependem de abstrações (interfaces), não de implementações concretas.
  - **Open/Closed Principle (OCP):** Novos serviços podem ser adicionados sem alterar os existentes.
- **Resumo:** Implementa as operações do sistema, separando regras de negócio da infraestrutura e dos dados.

---

### 3. `interfaces/`
- **O que contém:** Definições de contratos, protocolos, interfaces (ex: repositórios, gateways, adaptadores).
- **Princípios SOLID:**
  - **Interface Segregation Principle (ISP):** Interfaces pequenas e específicas para cada tipo de dependência.
  - **Dependency Inversion Principle (DIP):** O código depende de interfaces, facilitando testes e trocas de implementação.
- **Resumo:** Define contratos para dependências, promovendo baixo acoplamento e alta testabilidade.

---

### 4. `config/`
- **O que contém:** Configurações do sistema, variáveis de ambiente, arquivos de setup, parâmetros globais.
- **Princípios SOLID:**
  - **Single Responsibility Principle (SRP):** Centraliza a responsabilidade de configuração do sistema.
- **Resumo:** Mantém a configuração separada do código de negócio, facilitando manutenção e deploy.

---

### 5. `spv_automatico.py`
- **O que contém:** Provavelmente o ponto de entrada ou script principal do sistema.
- **Princípios SOLID:**
  - **SRP:** Deve apenas orquestrar a inicialização e execução do sistema, delegando responsabilidades para services, models, etc.
- **Resumo:** Centraliza a execução, mas deve ser o mais enxuto possível, apenas conectando os componentes.

---

## Tabela-Resumo

| Diretório           | Princípios SOLID Relacionados | Função Principal                                     |
|---------------------|------------------------------|------------------------------------------------------|
| models/             | SRP, OCP                     | Entidades e dados do domínio                         |
| services/           | SRP, OCP, DIP                | Lógica de negócio e orquestração                     |
| interfaces/         | ISP, DIP                     | Contratos e abstrações para dependências             |
| config/             | SRP                          | Configuração e parâmetros globais                    |
| spv_automatico.py   | SRP                          | Ponto de entrada/orquestração                        |

---