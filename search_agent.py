import ollama
import sys_msgs
import requests
import trafilatura
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from duckduckgo_search import DDGS
from config.config import MODEL_NAME, USE_KEYWORD_EXTRACTION

init(autoreset=True)
# 🗂️ Historique des échanges
assistant_convo = [sys_msgs.assistant_msg]

def search_or_not():
    sys_msg = sys_msgs.search_or_not_msg

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[sys_msg, assistant_convo[-1]]
    )

    content = response['message']['content']
    return 'true' in content.lower()

def query_generator():
    sys_msg = sys_msgs.query_msg
    query_msg = f'Créer une requete composée de mots clés au minimum afin de mener la recherche web de ce prompt: \n{assistant_convo[-1]["content"]}'

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[sys_msg, {'role': 'user', 'content': query_msg}]
    )
    return response['message']['content']

def duckduckgo_search(query, max_results=3):
    results = []

    with DDGS() as ddgs:
        for i, r in enumerate(ddgs.text(query), start=1):
            if i > max_results:
                break

            print(f"[Résultat {i}] {r['title']}")
            results.append({
                'id': i,
                'link': r['href'],
                'search_description': r['body']
            })

    return results

# ⬇️ Search using Google.fr
def google_titles(query):
    url = f'https://www.google.com/search?q={query}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('h3')

    results = []
    for i, title in enumerate(titles, start=1):
        text = title.getText().strip()
        if text:
            results.append({
                "id": i,
                "title": text
            })
    
    for info in titles: 
        print(info.getText()) 
        print("------")

    return results

def scrape_webpage(url):
    try:
        downloaded = trafilatura.fetch_url(url=url)
        return trafilatura.extract(downloaded, include_formatting=True, include_links=True)
    except Exception as e:
        return None

def best_search_result(s_results, query):
    # Message système pour guider le modèle
    sys_msg = sys_msgs.best_search_msg

    # Message utilisateur formaté avec les résultats et la requête
    best_msg = (
        f"SEARCH_RESULTS: {s_results} \n"
        f"USER_PROMPT: {assistant_convo[-1]} \n"
        f"SEARCH_QUERY: {query}"
    )

    # Tentatives de sélection du meilleur résultat via Ollama
    for _ in range(2):
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[
                    {'role': 'system', 'content': sys_msg},
                    {'role': 'user', 'content': best_msg}
                ]
            )
            return int(response['message']['content'])
        except:
            continue
    return 0

import ast

def extract_keywords_from_prompt(user_prompt):
    print(f'{Fore.LIGHTRED_EX} EXTRACT SEMANTIQUE KEY WORD ... {Style.RESET_ALL}')
    sys_msg = "Extract relevant keywords for a web search from this user prompt. Return as a Python list only, no explanation."
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {'role': 'system', 'content': sys_msg},
            {'role': 'user', 'content': user_prompt}
        ]
    )
    raw = response['message']['content']
    try:
        # Nettoyage simple
        cleaned = raw.strip("`\n ").replace("```python", "").replace("```", "")
        semantiq_keywords = ast.literal_eval(cleaned)
        print(f'{Fore.LIGHTYELLOW_EX} EXTRACT SEMANTIQUE KEY WORD : {semantiq_keywords} {Style.RESET_ALL}')
        return ", ".join(semantiq_keywords)
    except Exception as e:
        print("Erreur d’extraction :", e)
        return ""

def ai_search():
    context = None
    print(f'{Fore.LIGHTRED_EX}   GENERATING SEARCH QUERY....{Style.RESET_ALL}')
    search_query = query_generator()
    print(f'{Fore.LIGHTBLUE_EX}SEARCHING WEB FOR : {search_query} {Style.RESET_ALL}')

    if search_query[0] == '"':
        search_query = search_query[1:-1]
    
    search_results = duckduckgo_search(search_query)
    context_found = False

    if search_results:
        print(f'\n{Fore.LIGHTGREEN_EX}📌 Résultats de recherche pour "{search_query}" :{Style.RESET_ALL}\n')
        for result in search_results:
            print(f"{Fore.LIGHTCYAN_EX}[{result['id']}] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{result['search_description']}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTMAGENTA_EX}🔗 Lien : {result['link']}\n{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}⚠️ Aucun résultat trouvé pour : {search_query}{Style.RESET_ALL}")

    
    while not context_found and len(search_results) > 0:
        print(f'{Fore.LIGHTCYAN_EX} SEARCH FOR BEST ANSWER.... {Style.RESET_ALL}')
        best_result = best_search_result(s_results=search_results, query=search_query)
        try:
            page_link = search_results[best_result]['link']
            print(f'{Fore.LIGHTCYAN_EX} BEST LINK FOUND {page_link}. {Style.RESET_ALL}')
        except:
            print(f'{Fore.RED} FAILED TO SELECT BEST SEARCH RESULT, TRYING AGAIN. {Style.RESET_ALL}')
            continue

        page_text = scrape_webpage(page_link)
        search_results.pop(best_result)
        context_found = True

        if page_text and contains_data_needed(search_content=page_text, query=search_query):
            context = page_text
            context_found = True
    return context

def contains_data_needed(search_content, query):
    sys_msg = sys_msgs.contains_data_msg

    needed_prompt = (
        f"PAGE_TEXT: {search_content} \n"
        f"USER_PROMPT: {assistant_convo[-1]} \n"
        f"SEARCH_QUERY: {query}"
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {'role': 'system', 'content': sys_msg},
            {'role': 'user', 'content': needed_prompt}
        ]
    )

    content = response['message']['content']

    if 'true' in content.lower():
        print(f'{Fore.LIGHTRED_EX}SEARCHING DuckDuck FOR : {query} {Style.RESET_ALL}')
        return True
    else:
        print(f'{Fore.LIGHTRED_EX} DATA NOT RELEVENT (stop searching) {Style.RESET_ALL}')
        return False


def stream_assistant_response():
    global assistant_convo
    response_stream = ollama.chat( model=MODEL_NAME,
        messages=assistant_convo,
        stream=True
    )

    complete_response = ''
    print('ASSISTANT:')

    for chunk in response_stream:
        print(f'{Fore.WHITE}{chunk["message"]["content"]}{Style.RESET_ALL}', end='', flush=True)
        complete_response += chunk['message']['content']

    # 📝 Mémorisation de la réponse
    assistant_convo.append({'role': 'assistant','content': complete_response})
    print('\n')

def main():
    global assistant_convo

    while True:
        prompt = input(f'{Fore.LIGHTGREEN_EX}USER: \n')
        if USE_KEYWORD_EXTRACTION:
            new_prompt = extract_keywords_from_prompt(prompt)
        else:
            new_prompt = prompt  # Utilisation directe du prompt

        assistant_convo.append({'role': 'user', 'content': prompt})

        if search_or_not():
            print(f'{Fore.LIGHTMAGENTA_EX} [ALERT] User input prompt requires additional web search ... {Style.RESET_ALL}')
            context = ai_search()
            assistant_convo = [assistant_convo[-1]]  # conserve uniquement le dernier prompt

            if context:
                prompt = f"SEARCH RESULT: {context} \nUSER PROMPT: {prompt}"
                print(f'{Fore.LIGHTCYAN_EX} WEB SEARCH PROMPT : {prompt} {Style.RESET_ALL}')
            else:
                print(f'{Fore.LIGHTCYAN_EX} PROMPT WITHOUT WEB SEARCH {Style.RESET_ALL}')
                prompt = (
                    f"USER PROMPT: {prompt} \nFAILED SEARCH \nL'agent IA n’a pas pu extraire de données fiables. "
                    "Explique cela à l’utilisateur et demande s’il souhaite que tu relances une recherche ou que tu répondes "
                    "sans contexte web. Ne réponds en aucun cas directement à la question si une recherche était requise ; "
                    "attends d’avoir l’accord explicite de l’utilisateur."
                )

        print(f'{Fore.LIGHTMAGENTA_EX} FINAL PROMPT: {prompt} {Style.RESET_ALL}')
        assistant_convo.append({'role': 'user', 'content': prompt})
        stream_assistant_response()

if __name__ == '__main__':
    main()

