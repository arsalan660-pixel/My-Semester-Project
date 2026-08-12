import tkinter as tk
def scrape_books():
    return [
        {'name': 'Python Basics', 'price': '800'},
        {'name': 'Web Dev 101', 'price': '1200'}
    ]
def save_to_file(data,filename):
    if not data :
        print("no data to save")
    file=open(filename,'a')
    for book in data :
        line=book['name'] + "," + book['price']
        file.write(line + "\n")
    file.close()
    print(f"data save to {filename}")
def scrap_and_save():
    data=scrape_books()
    save_to_file(data,"books.csv")
window=tk.Tk()
window.title("books")
window.geometry("300x200")
label=window.Label(window,text="scrap and save")
label.pack()
button=window.Button(window,text="scrap and save",command=scrap_and_save)
button.pack()
window.mainloop()

