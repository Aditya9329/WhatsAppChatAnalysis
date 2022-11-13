import base64
from io import BytesIO
import matplotlib.pyplot as plt

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer,format="png")
    buffer.seek(0)
    img_png = buffer.getvalue()
    graph  = base64.b64encode(img_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph



def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,6))
    plt.title("Most Active user in a group")
    plt.barh(x,y,color="green")
    plt.tight_layout()
    graph = get_graph()
    return graph 


def get_plot_bar(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,6))
    plt.title("Most active month")
    plt.bar(x,y,color="tomato")
    plt.grid()
    plt.tight_layout()
    graph = get_graph()
    return graph 

def get_plot_char3(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,6))
    plt.title("Most active day")
    plt.xlabel("Days")
    plt.ylabel("No. of messages")
    plt.plot(x,y,color="black")
    plt.grid()
    plt.grid()
    plt.tight_layout()
    plt.show()
    graph = get_graph()
    return graph 