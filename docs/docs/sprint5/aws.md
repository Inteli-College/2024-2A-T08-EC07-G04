# Deploy na AWS

O projeto Fillmore foi desenvolvido para ser completamente alocado na AWS (Amazon Web Services), aproveitando os serviços e a infraestrutura oferecidos pela plataforma. A AWS oferece uma vasta gama de serviços para garantir a escalabilidade, segurança e eficiência no desenvolvimento de aplicações, permitindo que o projeto evolua de forma robusta e com alta disponibilidade.

## Vantagens de uma aplicação com deploy

A decisão de alocar o projeto na AWS traz diversos benefícios importantes, entre eles:

1. **Escalabilidade**: A AWS permite escalar os recursos de maneira automatizada ou manual, garantindo que a aplicação possa lidar com aumentos de tráfego sem perda de performance.
2. **Alta Disponibilidade**: Através de zonas de disponibilidade (AZs) e regiões geograficamente distribuídas, a AWS garante que a aplicação esteja disponível em diversas regiões do mundo com redundância, o que melhora o tempo de resposta e a continuidade do serviço.
3. **Segurança**: Com uma ampla gama de serviços de segurança, a AWS proporciona criptografia de dados em trânsito e em repouso, políticas de acesso detalhadas e proteção contra ataques DDoS.
4. **Custo-efetividade**: A cobrança de serviços na AWS segue o modelo de "pague pelo que usar", permitindo otimização dos custos de infraestrutura à medida que a demanda cresce.
5. **Ferramentas de Gerenciamento**: A AWS oferece ferramentas poderosas como o CloudWatch e o CloudTrail, que permitem monitorar, rastrear logs e acompanhar métricas de desempenho da infraestrutura.
6. **Backup e Recuperação de Desastres**: Com serviços como S3 e RDS, é possível configurar backups automáticos e ter estratégias de recuperação rápidas em caso de falhas.

## Arquitetura

O projeto está completamente alocado em uma instância EC2 (Elastic Compute Cloud), que é o serviço de computação escalável da AWS. Todo o ambiente de desenvolvimento e produção está centralizado nesta instância, o que proporciona flexibilidade para gerenciar a infraestrutura conforme necessário.

### Instância EC2

A instância EC2 utilizada foi configurada para atender às necessidades do projeto, com os seguintes pontos importantes:

- **Sistema Operacional**: A instância roda uma distribuição Linux Ubuntu.
- **Recursos de Computação**: A quantidade de CPU, memória e armazenamento foi provisionada com base nos requisitos atuais do prova de conceito, garantindo espaço para crescimento futuro.
- **Segurança**: Pelo momento, todos os acessos estão disponiveis, mas isso pode ser mudado para limitar a apenas IPs específicos.
- **Chave SSH**: O acesso à instância é realizado por meio de uma chave SSH segura, permitindo que apenas usuários autorizados possam gerenciar a instância remotamente.

### Docker na Instância EC2

O projeto está utilizando **Docker** para garantir consistência no ambiente de execução, tanto em desenvolvimento quanto em produção. Todos os containers necessários para rodar a aplicação estão configurados e sendo executados diretamente na instância EC2. Com isso, conseguimos:

- **Isolamento**: Cada serviço roda em seu próprio container Docker, evitando conflitos de dependências e garantindo a escalabilidade individual de cada parte do sistema.
- **Facilidade de Deploy**: Com Docker, o processo de deploy se torna mais simples, permitindo que novas versões da aplicação sejam lançadas rapidamente, com controle sobre as versões de cada container.
- **Manutenção e Atualização**: A manutenção e atualização do projeto podem ser realizadas diretamente nos containers Docker, o que facilita o rollback em caso de falhas e reduz o tempo de inatividade.
  
## Conclusão

O deploy na AWS teve como objetivo explorar a escalabilidade da prova de conceito, proporcionando uma visão sobre o comportamento do sistema em infraestrutura de nuvem. A alocação da aplicação em uma instância EC2, utilizando Docker, permitiu avaliar as necessidades de uma implementação real, possibilitando a mensuração mais clara de custos e benefícios de operar a aplicação em um ambiente cloud.