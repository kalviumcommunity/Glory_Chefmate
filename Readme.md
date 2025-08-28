# Chefmate: Your AI-Powered Culinary Assistant

Welcome to **Chefmate**, an intelligent AI application designed to solve the age-old problem of "what to cook?" This project acts as your personal culinary assistant, generating unique, personalized recipes based on what you have in your kitchen, your dietary needs, and your meal preferences.

Chefmate goes beyond a simple recipe search. It uses advanced language model techniques to generate a full recipe—complete with a name, ingredients list, step-by-step instructions, and a detailed nutritional breakdown. It's the perfect tool for getting creative in the kitchen, reducing food waste, and simplifying meal planning.

### **Key Features** 🧠

* **Personalized Generation**: Create recipes tailored to your specific ingredients and dietary requirements.
* **Zero-Shot & One-Shot Prompting**: Get a quick recipe on the fly or ensure a perfect, structured output every time.
* **Chain-of-Thought Reasoning**: Understand why a recipe is considered healthy with a transparent, step-by-step nutritional analysis.
* **Structured Output**: Ensures all generated recipes are returned in a clean, machine-readable JSON format, making them easy to use.
* **Creativity Control**: Adjust the AI's creativity with parameters like **Temperature** to get either a classic dish or a wildly unique culinary invention.
* **Token Logging**: Keep track of API usage and costs by logging token consumption for every request.
* **Top P**: Control the diversity and focus of the generated text.
* **Stop Sequence**: Stop the model's output at a specific point to ensure a clean response.

### **Technical Implementation** ⚙️

Chefmate is built on a robust Python backend that interacts with the OpenAI API. The project architecture is modular, making it easy to expand and maintain.

* **Frontend**: Built with **Streamlit** for a simple, interactive user interface.
* **Backend**: A **Python** application that handles user input and communicates with the LLM.
* **AI Models**: Utilizes **GPT-4o-mini** for efficient and accurate recipe generation.
* **Prompting**: Employs multiple prompting strategies to optimize output:
    * **Zero-Shot**: For generating a basic recipe with minimal instructions.
    * **One-Shot**: To guide the model to follow a precise JSON output format.
    * **Chain-of-Thought**: To enable the model to perform a step-by-step nutritional analysis.
* **API Control**: Fine-tunes the model's behavior using parameters like `temperature`, `top_p`, and `stop_sequence`.
* **Data Handling**: Guarantees a valid JSON response using the `response_format` parameter in the API call.

### **How to Run** 🚀

1.  **Clone the Repository**:
    ```bash
    git clone <your_github_repo_link>
    cd chefmate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set Up Your API Key**:
    The application will automatically load your API key from the `.env` file.
4.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```
    The application will launch in your web browser, ready to generate delicious recipes.