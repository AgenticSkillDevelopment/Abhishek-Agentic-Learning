from typing_extensions import TypedDict
import random
from typing import Literal
from IPython.display import display, Image
from langgraph.graph import StateGraph, START , END

class State(TypedDict):
    graph_info: str

def start_play(state: State):
    print("Starting the game with state")
    return {"graph_info": state['graph_info']}

def cricket(state: State):
    print("Cricket node has been called")
    return {"graph_info": state['graph_info'] + "cricket"}

def badminton(state: State):
    print("Badminton node has been called")
    return {"graph_info": state['graph_info'] + "Badminton"}

def random_play(state: State) -> Literal['cricket', 'badminton']:
    if random.choice() > 0.5:
        return "cricket"
    else:
        return "badminton"
    
#build graph
graph = StateGraph(State)

# Add nodes to the graph
graph.add_node("start_play", start_play)
graph.add_node("cricket", cricket)
graph.add_node("badminton", badminton)

#scheduling the flow of the graph
graph.add_edge(START, "start_play")
graph.add_conditional_edges("start_play", random_play)
graph.add_edge("cricket", END)
graph.add_edge("badminton", END)

#compiling the graph
compiled_graph = graph.compile()

display(Image(compiled_graph.get_graph().draw_mermaid_png()))
