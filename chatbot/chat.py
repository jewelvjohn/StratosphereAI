import json
import torch
import random

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

class Chatbot():
    def __init__(self, json_file: str, data_file: str):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        with open(json_file, 'r') as json_data:
            self.intents = json.load(json_data)

        FILE = data_file
        data = torch.load(FILE)

        self.input_size = data["input_size"]
        self.hidden_size = data["hidden_size"]
        self.output_size = data["output_size"]
        self.all_words = data['all_words']
        self.tags = data['tags']
        self.model_state = data["model_state"]

        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.model.load_state_dict(self.model_state)
        self.model.eval()

    def get_response(self, msg):
        sentence = tokenize(msg)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])
        
        return "I do not understand..."
    
if __name__ == "__main__":
    chatbot = Chatbot("intents.json", "data.pth")
    print("Chatbot: Hey!")
    
    while True:
        text = input("You: ")
        if text == "quit":
            break
        response = chatbot.get_response(text)
        print("Chatbot: " + response)