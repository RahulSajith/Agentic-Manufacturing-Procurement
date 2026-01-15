import asyncio
import os
import json
import datetime
from playwright.async_api import async_playwright
from pydantic import BaseModel
import ollama

# 1. Professional Data Structure
class ProcurementData(BaseModel):
    material: str
    price: float
    currency: str
    button_id: str

# 2. Audit Logger (Scrap Labs requirement: "Audit trails")
def log_action(data, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] MATERIAL: {data.material} | PRICE: {data.currency}{data.price} | STATUS: {status}\n"
    
    # Ensure logs folder exists
    if not os.path.exists("logs"):
        os.makedirs("logs")
        
    with open("logs/procurement_audit.log", "a") as f:
        f.write(log_entry)

async def run_procurement_agent():
    async with async_playwright() as p:
        # 3. Setup Browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # 4. Load Mock Vendor
        file_path = os.path.abspath("mock_vendor/index.html")
        await page.goto(f"file:///{file_path}")
        
        # 5. Extract Content
        html_content = await page.content()
        print("\n🤖 Agent: Analyzing manufacturing portal...")

        # 6. AI Reasoning Loop
        prompt = f"""
        Analyze this HTML and extract procurement data.
        Return ONLY a JSON object with these EXACT keys:
        - "material": (string)
        - "price": (number only, remove symbols like '$')
        - "currency": (string, e.g., 'USD')
        - "button_id": (string, the ID of the quote button)

        HTML: {html_content}
        """

        response = ollama.generate(
            model='qwen3:8b', 
            prompt=prompt,
            format='json'
        )

        # 7. Validation & Human-in-the-Loop
        try:
            raw_data = json.loads(response['response'])
            data = ProcurementData(**raw_data)
            
            print(f"\n--- 🔔 HUMAN APPROVAL REQUIRED ---")
            print(f"Material: {data.material}")
            print(f"Price:    {data.currency} {data.price}")
            print(f"Action:   Click '{data.button_id}' to send Quote")
            print(f"----------------------------------\n")

            user_input = input("Confirm this order? (y/n): ").lower()

            if user_input == 'y':
                print(f"🖱️ Action Approved. Clicking button...")
                await page.click(f"#{data.button_id}")
                
                # 8. Verifier Loop
                print("🔍 Verifying UI state change...")
                await asyncio.sleep(1)
                button_text = await page.inner_text(f"#{data.button_id}")
                
                if button_text == "Quote Sent!":
                    print("✨ SUCCESS: Procurement loop closed.")
                    log_action(data, "SUCCESS - ORDER VERIFIED")
                else:
                    print(f"⚠️ FAILURE: Button state did not change.")
                    log_action(data, f"FAILURE - UI STATE MISMATCH: {button_text}")
            else:
                print("⛔ Action Cancelled by user.")
                log_action(data, "CANCELLED BY HUMAN")
            
        except Exception as e:
            print(f"❌ System Error: {e}")

        await asyncio.sleep(2)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_procurement_agent())