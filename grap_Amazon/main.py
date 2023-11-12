# main.py
import tkinter as tk
from tkinter import simpledialog
from function import fetch_website, parse_html, save_to_csv

def main():
    url = "https://www.amazon.com/gp/bestsellers/amazon-devices/ref=zg_bs_amazon-devices_sm"
    html_content = fetch_website(url)
    if html_content:
        print(html_content[:100])

def start_scraping():
    # 从输入框获取URL和页面数
    url = url_entry.get()
    num_pages = int(pages_entry.get())

    data = fetch_website(url,num_pages)
    if data:
        save_to_csv(data,'amazon_best_sellers.csv')
        status_label.config(text='data stored succeed')
    else:
        status_label.config(text='data stored fail')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Amazon scrap tool")

    # 创建输入框标签
    tk.Label(root, text="URL:").grid(row=0,column=0)
    tk.Label(root, text="Page numbers:").grid(row=1, column=0)

    # 创建输入框
    url_entry = tk.Entry(root)
    url_entry.grid(row=0,column=1)
    pages_entry = tk.Entry(root)
    pages_entry.grid(row=1,column=1)

    # 创建按钮
    start_button = tk.Button(root, text="Start to scrap", command=start_scraping)
    start_button.grid(row=2,column=0,columnspan=2)

    # 创建状态标签
    status_label = tk.Label(root,text="")
    status_label.grid(row=3,column=0,columnspan=2)

    root.mainloop()


    #url = "https://www.amazon.com/gp/bestsellers/amazon-devices/ref=zg_bs_amazon-devices_sm"
    #data = fetch_website(url,2)
    #if data:
    #    save_to_csv(data,'amazon_best_sellers.csv')
    #    print('DATA saved to CSV file.')
    #else:
    #    print('No data to save.')


