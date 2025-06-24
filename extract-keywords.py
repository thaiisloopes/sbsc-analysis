import nltk
from rake_nltk import Rake

nltk.download('stopwords')
nltk.download('punkt_tab')

texto = "A pandemia do coronavirus trouxe mudanças significativas com a transição para o home office. Esta pesquisa procura entender como o home office compulsório afetou as expectativas para colaboração profissional após a pandemia. Os resultados e a análise trabalham 29 entrevistas em profundidade com os profissionais em home office. Os resultados analisados sob a perspectiva da Teoria da Mudança Organizacional demonstraram que o suporte organizacional e a aceitação do grupo foram fundamentais para mudança. Além disso, daqui para frente, a flexibilidade foi indicada como parâmetro principal a ser incorporado em sistemas de colaboração profissional."
r = Rake()
r.extract_keywords_from_text(texto)

palavras_chave = r.rank_list
print(palavras_chave)
