#final nato


import asyncio
from pyppeteer import launch
import random
import tkinter as tk
from tkinter import messagebox, font

async def auto_heart_facebook(username, password, page_url, hearts_count):
    try:
        browser = await launch(headless=False, executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                               args=['--disable-blink-features=AutomationControlled'])
        
        page = await browser.newPage()

        await page.setViewport({'width': 1280, 'height': 800})
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        await page.goto('https://www.facebook.com/login/')
        await page.waitForSelector('input[name="email"]')

        await page.type('input[name="email"]', username, {'delay': random.randint(50, 100)})
        await page.type('input[name="pass"]', password, {'delay': random.randint(50, 100)})

        await page.click('button[name="login"]')
        await page.waitForNavigation({'waitUntil': 'networkidle2'})  

        await page.goto(page_url)
        await page.waitForSelector('div[aria-label="Like"]')  

        hearts_done = 0
        while hearts_done < hearts_count:
            like_buttons = await page.querySelectorAll('div[aria-label="Like"]')

            if like_buttons:
                for i in range(min(len(like_buttons), hearts_count - hearts_done)):
                    await page.hover('div[aria-label="Like"]')
                    await asyncio.sleep(2)  

                    heart_button = await page.querySelector('div[aria-label="Love"]')
                    like_button = await page.querySelector('div[aria-label="Like"]')

                    if heart_button:
                        await heart_button.click()
                        print("Hearted a post.")
                    elif like_button:
                        await like_button.click()  
                        print("Liked a post.")

                    hearts_done += 1

                    if hearts_done >= hearts_count:
                        break

                next_button = await page.querySelector('i[style*="background-image: url(https://static.xx.fbcdn.net/rsrc.php/v3/y-/r/2xASrRpIjXi.png)"]')

                if next_button:
                    await page.evaluate('(element) => element.click()', next_button)
                    await page.waitForSelector('div[aria-label="Like"]')  
                    await asyncio.sleep(2)
                else:
                    
                    await page.evaluate('window.scrollBy(0, window.innerHeight)')
                    await asyncio.sleep(2)
            else:
                print("No like button found")
                break

        await browser.close()
        root.after(0, lambda: root.deiconify())
        messagebox.showinfo("Finished", "Finished reacting to posts.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'browser' in locals():
            await browser.close()

def start_reacting():
    username = entry_username.get()
    password = entry_password.get()
    page_url = entry_page_url.get()
    try:
        hearts_count = int(entry_hearts_count.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for hearts count.")
        return

    if not username or not password or not page_url:
        messagebox.showerror("Missing Information", "Please provide all fields.")
        return

    root.withdraw()
    asyncio.get_event_loop().run_until_complete(auto_heart_facebook(username, password, page_url, hearts_count))


root = tk.Tk()
root.title("Heart ko Facebook mo <3")

title_font = font.Font(family='Century', size=24, weight='bold')
label_font = font.Font(family='Century', size=12)
button_font = font.Font(family='Century', size=12, weight='bold')

root.configure(bg='#f0f0f0')

title_label = tk.Label(root, text="Heart ko Facebook mo <3", font=title_font, bg='#f0f0f0', fg='#ff3366')
title_label.pack(pady=20)

tk.Label(root, text="Facebook Username:", font=label_font, bg='#f0f0f0').pack(pady=5)
entry_username = tk.Entry(root, width=50, font=label_font)
entry_username.pack(pady=5)

tk.Label(root, text="Facebook Password:", font=label_font, bg='#f0f0f0').pack(pady=5)
entry_password = tk.Entry(root, show='*', width=50, font=label_font)
entry_password.pack(pady=5)

tk.Label(root, text="Page URL:", font=label_font, bg='#f0f0f0').pack(pady=5)
entry_page_url = tk.Entry(root, width=50, font=label_font)
entry_page_url.pack(pady=5)

tk.Label(root, text="Number of Hearts:", font=label_font, bg='#f0f0f0').pack(pady=5)
entry_hearts_count = tk.Entry(root, width=50, font=label_font)
entry_hearts_count.pack(pady=5)

tk.Button(root, text="Start", command=start_reacting, font=button_font, bg='#ff3366', fg='white').pack(pady=20)

root.mainloop()
