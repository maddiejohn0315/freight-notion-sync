import requests
from bs4 import BeautifulSoup
import json

# ==================== CONFIGURATION ====================
NOTION_TOKEN = "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"
DATABASE_ID = "3f1caba072798067b632d5c72b91ac18"
FREIGHT_URL = "https://devsuniverse.io"
# =======================================================

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def fetch_freight_tasks(url):
    print("Fetching tasks from Freight Dashboard...")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to load dashboard. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tasks = []
    
    task_elements = soup.find_all(['p', 'div', 'li'], class_=lambda x: x and ('task' in x or 'row' in x))
    if not task_elements:
        task_elements = soup.find_all('p')

    for element in task_elements:
        text = element.get_text(strip=True)
        if text and len(text) > 5 and not text.startswith("Continue where you left off"):
            is_done = "[x]" in text or "✓" in text
            clean_text = text.replace("[x]", "").replace("[-]", "").strip()
            
            category = "Today"
            if "Read" in clean_text or "SOP" in clean_text:
                category = "Read first"
            
            tasks.append({
                "name": clean_text,
                "status": is_done,
                "category": category
            })
            
    print(f"Successfully compiled {len(tasks)} tasks.")
    return tasks

def push_to_notion(task):
    url = "https://notion.com"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Task Name": {
                "title": [{"text": {"content": task["name"]}}]
            },
            "Category": {
                "select": {"name": task["category"]}
            },
            "Status": {
                "checkbox": task["status"]
            }
        }
    }
    
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        print(f"✔ Synced task: {task['name'][:30]}...")
    else:
        print(f"❌ Error syncing task: {res.text}")

if __name__ == "__main__":
    extracted_tasks = fetch_freight_tasks(FREIGHT_URL)
    if extracted_tasks:
        print("Paging data over to Notion database...")
        for task in extracted_tasks:
            push_to_notion(task)
        print("🎉 Sync sequence completed successfully!")
    else:
        print("No tasks found to sync.")
