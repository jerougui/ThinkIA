import sys
import os

# 📁 Accès aux modules du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import prompts.sys_msgs as sys_msgs
import requests
import trafilatura
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from ddgs import DDGS
from tools.llm_provider import chat
from config.config import USE_KEYWORD_EXTRACTION, PROVIDER
from tools.ollama_manager import launch_model_if_needed


init(autoreset=True)
# 🗂️ Historique des échanges
assistant_convo = [sys_msgs.assistant_msg]

def search_or_not():
    sys_msg = sys_msgs.search_or_not_msg

    response = chat(
        messages=[sys_msg, assistant_convo[-1]]
    )

    content = response['message']['content']
    return 'true' in content.lower()

def query_generator():
    sys_msg = sys_msgs.query_msg
    query_msg = f'Créer une requete composée de mots clés au minimum afin de mener la recherche web de ce prompt: \n{assistant_convo[-1]["content"]}'

    response = chat(
        messages=[sys_msg, {'role': 'user', 'content': query_msg}]
    )
    return response['message']['content']

def duckduckgo_search(query, max_results=3):
    results = []

    excluded_extensions = ['.pdf', '.json', '.zip', '.diff', '.tar.gz', '.exe']
    excluded_keywords = ['tokenizer', 'ckpt', 'commit', 'download', 'blob', 'raw', 'api']

    with DDGS() as ddgs:
        for i, r in enumerate(ddgs.text(query), start=1):
            if i > max_results:
                break

            link = r['href'].lower()

            # 🔍 Filtrage par extension
            if any(link.endswith(ext) for ext in excluded_extensions):
                print(f"{Fore.YELLOW}⏩ Ignoré (extension non textuelle) : {link}{Style.RESET_ALL}")
                continue

            # 🔍 Filtrage par mot-clé technique
            if any(keyword in link for keyword in excluded_keywords):
                print(f"{Fore.YELLOW}⏩ Ignoré (lien technique) : {link}{Style.RESET_ALL}")
                continue

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

    # Tentatives de sélection du meilleur résultat
    for _ in range(2):
        try:
            response = chat(
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
    response = chat(
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

    if search_query.startswith('"') and search_query.endswith('"'):
        search_query = search_query[1:-1]

    search_results = duckduckgo_search(search_query)
    context_found = False
    max_attempts = 5
    attempts = 0

    if search_results:
        print(f'\n{Fore.LIGHTGREEN_EX}📌 Résultats de recherche pour "{search_query}" :{Style.RESET_ALL}\n')
        for result in search_results:
            print(f"{Fore.LIGHTCYAN_EX}[{result['id']}] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{result['search_description']}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTMAGENTA_EX}🔗 Lien : {result['link']}\n{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}⚠️ Aucun résultat trouvé pour : {search_query}{Style.RESET_ALL}")
        return None

    while not context_found and search_results and attempts < max_attempts:
        print(f'{Fore.LIGHTCYAN_EX} SEARCH FOR BEST ANSWER.... {Style.RESET_ALL}')
        best_result = best_search_result(s_results=search_results, query=search_query)
        attempts += 1

        try:
            page_link = search_results[best_result]['link']
            print(f'{Fore.LIGHTCYAN_EX} BEST LINK FOUND {page_link}. {Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED} FAILED TO SELECT BEST SEARCH RESULT, TRYING AGAIN. {Style.RESET_ALL}')
            continue

        page_text = scrape_webpage(page_link)
        search_results.pop(best_result)

        if page_text and contains_data_needed(search_content=page_text, query=search_query):
            context = page_text
            context_found = True

    if not context_found:
        print(f"{Fore.YELLOW}⚠️ Aucune donnée pertinente trouvée après {max_attempts} tentatives.{Style.RESET_ALL}")

    return context


def contains_data_needed(search_content, query):
    sys_msg = sys_msgs.contains_data_msg

    needed_prompt = (
        f"PAGE_TEXT: {search_content} \n"
        f"USER_PROMPT: {assistant_convo[-1]} \n"
        f"SEARCH_QUERY: {query}"
    )

    #print("Prompt envoyé au modèle :\n", needed_prompt)

    response = chat(
        messages=[
            {'role': 'system', 'content': sys_msg},
            {'role': 'user', 'content': needed_prompt}
        ]
    )

    #print("Réponse du modèle :", response)
    content = response['message']['content']

    if 'true' in content.lower():
        print(f'{Fore.LIGHTRED_EX}SEARCHING DuckDuck FOR : {query} {Style.RESET_ALL}')
        return True
    else:
        print(f'{Fore.LIGHTRED_EX} DATA NOT RELEVENT (stop searching) {Style.RESET_ALL}')
        return False

def stream_assistant_response():
    global assistant_convo
    print('ASSISTANT:')

    complete_response = ''

    if PROVIDER == 'ollama':
        response_stream = chat(messages=assistant_convo, stream=True)
        for chunk in response_stream:
            content = chunk["message"]["content"]
            print(f'{Fore.WHITE}{content}{Style.RESET_ALL}', end='', flush=True)
            complete_response += content

    elif PROVIDER == 'openrouter':
        response_stream = chat(messages=assistant_convo, stream=True)
        for chunk in response_stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                print(f'{Fore.WHITE}{delta.content}{Style.RESET_ALL}', end='', flush=True)
                complete_response += delta.content

    elif PROVIDER == 'gemini':
        # Gemini ne supporte pas le streaming → appel classique
        response = chat(messages=assistant_convo, stream=False)
        content = response["message"]["content"]
        print(f'{Fore.WHITE}{content}{Style.RESET_ALL}', end='', flush=True)
        complete_response = content

    assistant_convo.append({'role': 'assistant', 'content': complete_response})
    print('\n')

def main():
    global assistant_convo

    # ⚙️ Vérifie et lance le modèle Ollama si nécessaire
    launch_model_if_needed()

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

